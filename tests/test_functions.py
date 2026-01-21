import unittest

from functions.utils.sanitize_recipe_name import sanitize_recipe_name

class TestSanitizeRecipeName(unittest.TestCase):
  def test_name_with_whitespaces(self):
    item = "bife de frango"
    name = sanitize_recipe_name(item)
    
    self.assertEqual("bife_de_frango", name)
    
  def test_name_with_whitespaces_and_3_numbers(self):
    item = "Esfirra 001"
    name = sanitize_recipe_name(item)
    
    self.assertEqual("Esfirra", name)
    
  def test_name_with_single_number(self):
    item = "Esfirra2"
    name = sanitize_recipe_name(item)
    
    self.assertEqual("Esfirra2", name)