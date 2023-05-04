import ast

def extract_functions_with_content(code):
    """
    Extract all functions and their contents from a given code string.

    Args:
        code (str): A string containing Python code.

    Returns:
        Dict[str, str]: A dictionary mapping function names to their contents.
    """
    functions = {}

    # Parse the code using the ast module
    parsed = ast.parse(code)

    # Visit each node in the parsed code
    for node in ast.walk(parsed):

        # Check if the node is a function definition
        if isinstance(node, ast.FunctionDef):

            # Get the function name and its content
            function_name = node.name
            function_content = ast.get_source_segment(code, node)

            # Add the function to the dictionary
            functions[function_name] = function_content

    return functions


