import os
from dotenv import load_dotenv
from google import genai

from prompts import system_prompt;
from functions.utils.get_files_paths import get_files_paths

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main():
    source_folder = os.path.abspath("recipes_source/")
    dir_name_files = {}
    get_files_paths(dir_name_files, source_folder)
    
    print(dir_name_files)
    
    
    #generated_content = client.models.generate_content(
    #    model="gemini-3-flash-preview",
    #    contents="Explain how AI works in a few words"
    #)
    
    #print(generated_content.text)
    


if __name__ == "__main__":
    main()
