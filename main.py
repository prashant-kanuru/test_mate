from fastapi import FastAPI, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse 
import os
import openai
from pydantic import BaseModel
import config
import extractor
import fileAccept


'''
config.py is a self made file that contains the credentials for azure for open ai api the format of file is

name: config.py

contents:

api_type="azure"
api_base= base url to azure user.
api_version= version
api_key= api key

'''


# Get the credentials 

openai.api_type= config.api_type

openai.api_base=config.api_base

openai.api_version=config.api_version

openai.api_key=config.api_key


class prompt(BaseModel):
    user: str
app=FastAPI()


# api for to response from chat GPT after sending a prompt
@app.post("/gpt_output")
async def root(input:prompt):   
    """response=openai.ChatCompletion.create(model="gpt-35-turbo",
                                          messages=[{'role':'system','content':'system'},
                                                    {'role':'user','content':input.user}],
                                                    temperature=0.8,
                                                    top_p=0.9)
    result=response['choices'][0]['message']['content']"""
    
    response = openai.ChatCompletion.create(engine = "gpt-35-turbo",
                                            messages = [{'role' : 'system', 'content': 'system'},
                                            {'role' : 'user', 'content' : input.user}],
                                            temperature = 0.8,
                                            top_p = 0.9)
    result = response['choices'][0]['message']['content']


    processed_result = extractor.codeExtractor(result)
    
    return processed_result


# Takes a file as input and reads the content
# to make a request use postman post request, body = form data, key file, value select file.

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    print(type(file))
    # read the file the contents var is bytes type
    contents = await file.read()
    print(contents)
    # convert byte to string
    resolved_contents = contents.decode()
    
    # get extracted functions
    extracted_functions = fileAccept.extract_functions_with_content(resolved_contents)

    # base propmt to which required functions are added later
    promptBase = "I will provide you a code , write unit test cases using unittest library and end with if name=='main' block the function is "
    testFunctions = []

    # for each function in the dict of all functions call the api
    # and store the value output to a list which will be returned
    for function in extracted_functions.keys():
        to_be_sent_prompt = promptBase + extracted_functions[function]
        response = openai.ChatCompletion.create(engine = "gpt-35-turbo",
                                            messages = [{'role' : 'system', 'content': 'system'},
                                            {'role' : 'user', 'content' : to_be_sent_prompt}],
                                            temperature = 0.8,
                                            top_p = 0.9)
        result = response['choices'][0]['message']['content']
    
        # generated output is cleaned.
        processed_result = extractor.codeExtractor(result)
        testFunctions.append(processed_result)
        

    return {"TestFunctions" : testFunctions}
        

    
