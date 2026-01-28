import re

def sanitize_recipe_name(item):
  """
  Get the last part of the path, so it is the filename
  
  Split in whitespace and join _
  
  From "recipe name.jpg" it go to "recipe_name"
  Args:
      item (string): The unsinized file name of a recipe.
  Returns:
      string: The sanitized name of the recipe file.
  """
  name = "_".join(item.lower().split(".",1)[0].split(" "))
  
  matches = re.findall(r"^(.*?)(?:_\d{3})?$", name)
  
  return matches[0]