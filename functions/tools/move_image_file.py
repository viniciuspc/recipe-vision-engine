import os
import shutil
from google.genai import types

def move_image_file(working_directory, file_path, dest_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        src_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        validate_file_dir(src_dir, file_path, working_dir_abs)
        
        dest_dir = os.path.normpath(os.path.join(working_dir_abs, dest_path))
        
        validate_file_dir(dest_dir, dest_path, working_dir_abs)
        
        
        # Make sure all parent directory exists
        os.makedirs(working_dir_abs, exist_ok=True)
        
        shutil.move(src_dir, dest_dir)
        
        return f'Successfully copy from "{file_path}" to "{dest_path}"'
    except Exception as e:
        return f"Error: {e}"
    
def validate_file_dir(file_dir, file_path, working_dir_abs):
    if os.path.isdir(file_dir):
        return f'Error: Cannot open "{file_path}" as it is a directory'

    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, file_dir]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot open "{file_path}" as it is outside the permitted working directory'

schema_move_image_file = types.FunctionDeclaration(
    name="move_image_file",
    description="Move an image file from the file path to the specified dest path relative to the working directory, providing a Successfull message if it was able to move it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the image to move from, relative to the working directory",
            ),
            "dest_path": types.Schema(
                type=types.Type.STRING,
                description="Desr path to move the image into, relative to the working directory",
            ),
        },
        required=["file_path", "dest_path"]
    ),
)