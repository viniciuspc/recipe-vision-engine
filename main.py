import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt;
from functions.tools.call_function import available_functions, call_function
from functions.utils.get_files_paths import get_files_paths

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def call_ai_agent():
    generated_content = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents="Which tools do you have available?",
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    
    print(generated_content.text)
    


def main():
    source_folder = os.path.abspath("recipes/src/")
    dir_name_files = {}
    get_files_paths(dir_name_files, source_folder)
    print(dir_name_files)
    
    call_ai_agent()
    


if __name__ == "__main__":
    main()
