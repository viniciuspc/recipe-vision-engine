from google.genai import types
from functions.tools.write_file import schema_write_file, write_file
from functions.tools.move_image_file import schema_move_image_file, move_image_file

available_functions = types.Tool(
    function_declarations=[
        schema_write_file,
        schema_move_image_file
        ],
)

def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
        
    function_map = {
        "write_file": write_file,
        "move_image_file": move_image_file,
    }
    
    function_name = function_call.name or ""
    
    # Check if the it is a valid function_name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Handle arguments and include working_directory argument.
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./recipes"
    
    # Call the function
    function_result = function_map[function_call.name](**args)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
    