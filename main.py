import os
import argparse
from functions.utils.get_files_paths import get_files_paths
from functions.gemini.call_ai_agent import call_ai_agent

parser = argparse.ArgumentParser(description="Recipe-vision-engine")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
    


def main():
    verbose = args.verbose
    source_folder = os.path.abspath("recipes/src/")
    dir_name_files = {}
    get_files_paths(dir_name_files, source_folder)
    if(verbose):
        for name in dir_name_files:
            files = dir_name_files[name]
            print(f"Recipe: {name}, files: {files}")
    
    print(f"Will generate {len(dir_name_files)} recipes.")
    
    # call_ai_batch(client)
    
    for name in dir_name_files:
        files = dir_name_files[name]
        if(verbose):
            print(f">>>>>>> Processing Recipe: {name}, files: {files}")
        call_ai_agent(name, files, verbose)
    


if __name__ == "__main__":
    main()
