import os
from functions.utils.sanitize_recipe_name import sanitize_recipe_name

def get_files_paths(dir_name_files, source_folder):
    for item in os.listdir(source_folder):
        item_file_path = os.path.join(source_folder, item)
        if(item.startswith(".")):
            # Ignore hidden itens
            continue
        if(os.path.isfile(item_file_path)):
            os.path.basename(item_file_path)
            
            name = sanitize_recipe_name(item)
            # Remove numbers that can be in the end of the file name
            
            if(name in dir_name_files):
                dir_name_files[name].append(item_file_path)
            else:
                dir_name_files[name] = [item_file_path]
        else:
            get_files_paths(dir_name_files, item_file_path)