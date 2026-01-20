import os
from dotenv import load_dotenv
from google import genai

from prompts import system_prompt;

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def get_files_paths(dir_name_files, source_folder):
    for item in os.listdir(source_folder):
        item_file_path = os.path.join(source_folder, item)
        if(item.startswith(".")):
            # Ignore hidden itens
            continue
        if(os.path.isfile(item_file_path)):
            os.path.basename(item_file_path)
            # Get the last part of the path, so it is the filename
            # Split in whitespace and join _
            # From "recipe name.jpg" it go to "recipe_name"
            name = "_".join(item.split(".",1)[0].split(" "))
            # Remove numbers that can be in the end of the file name
            
            if(name in dir_name_files):
                dir_name_files[name].append(item_file_path)
            else:
                dir_name_files[name] = [item_file_path]
        else:
            get_files_paths(dir_name_files, item_file_path)



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
