# function that takes in a raw string from GPT output and returns the python code extracted code.
'''
sample prompt:

{
  "user": "I will provide you a code , write unit test cases using unittest library and end with if name=='main' block function is def sum(a,b):\\n      return a+b"
}

'''
def codeExtractor(inputString):
    # Seperates each line of code.
    list_lines = inputString.splitlines()
    idxs=[]

    # interate over splitted lines and look for indexes where import statement and if __name__ == "__main__" is found and add it to idxs
    for i in range(len(list_lines)):
        if "import unittest" in list_lines[i]:
            idxs.append(i)
        elif "if __name__ == '__main__':" in list_lines[i]:
            idxs.append(i+1)

    # slice the splitted String in range idxs to get the code.
    extract_lines=list_lines[idxs[0]:idxs[1]+1]


    extractedCode = ""
    
    # join each line of code to string to return with proper indentation.
    for i in extract_lines:
        i = i + "\n"
        extractedCode = extractedCode + i

    return extractedCode




