import os
import pathlib
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.tools.call_function import available_functions, call_function
from functions.utils.get_files_paths import get_files_paths
from functions.utils.call_ai_batch import call_ai_batch

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Recipe-vision-engine")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

def call_ai_agent(files):
    contents = []
    for file in files:
        filepath = pathlib.Path(file)
        part = types.Part.from_bytes(
            data=filepath.read_bytes(),
            mime_type="image/jpeg"
        )
    
    contents.append(part)
    
    for _ in range(20):
        try:
            generated_content = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=contents,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                )
            )
            
            cadidates = generated_content.candidates
            if cadidates:
                for candidate in cadidates:
                    contents.append(candidate.content)
                    
            usage_metadata = generated_content.usage_metadata    
            if usage_metadata:
                if args.verbose:
                    print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
                    print(f"Response tokens: {usage_metadata.candidates_token_count}")
                
                function_calls = generated_content.function_calls
                
                if function_calls:
                    function_results = []
                    for function_call in function_calls:
                        function_call_result = call_function(function_call, args.verbose)
                        
                        if not function_call_result.parts:
                            raise Exception("function_call_result.parts does not exists ")
                        
                        function_call_result_part = function_call_result.parts[0]
                        
                        if not function_call_result_part.function_response or not function_call_result_part.function_response.response:
                            raise Exception("function_call_result response does not exists")
                        
                        function_results.append(function_call_result_part)
                        
                        if args.verbose:
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                            
                    contents.append(types.Content(role="user", parts=function_results))
                else:
                    print(generated_content.text)
                    return
            else:
                raise RuntimeError("Failed to connect to Gemini API")
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue
    
    print("Model could not produce a result with 20 interation. Exiting with code 1")
    
    


def main():
    source_folder = os.path.abspath("recipes/src/")
    dir_name_files = {}
    get_files_paths(dir_name_files, source_folder)
    for name in dir_name_files:
        files = dir_name_files[name]
        print(f"Recipe: {name}, files: {files}")
    print(f"Will generate {len(dir_name_files)} recipes.")
    
    # call_ai_batch(client)
    
    for name in dir_name_files:
        files = dir_name_files[name]
        print(f">>>>>>> Processing Recipe: {name}, files: {files}")
        call_ai_agent(files)
    


if __name__ == "__main__":
    main()
