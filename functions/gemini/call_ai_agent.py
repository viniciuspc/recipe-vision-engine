import os
import pathlib
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from prompts import system_prompt
from functions.tools.call_function import available_functions, call_function

def ai_agent_loop(client, name, contents, verbose):
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
              if verbose:
                  print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
                  print(f"Response tokens: {usage_metadata.candidates_token_count}")
              
              function_calls = generated_content.function_calls
              
              if function_calls:
                  function_results = []
                  for function_call in function_calls:
                      function_call_result = call_function(function_call, verbose)
                      
                      if not function_call_result.parts:
                          raise Exception("function_call_result.parts does not exists ")
                      
                      function_call_result_part = function_call_result.parts[0]
                      
                      if not function_call_result_part.function_response or not function_call_result_part.function_response.response:
                          raise Exception("function_call_result response does not exists")
                      
                      function_results.append(function_call_result_part)
                      
                      if verbose:
                          print(f"-> {function_call_result.parts[0].function_response.response}")
                          
                  contents.append(types.Content(role="user", parts=function_results))
              else:
                  print(generated_content.text)
                  return
          else:
              raise RuntimeError("Failed to connect to Gemini API")
      except ClientError as e:
          print(f"Error processing recipe {name}: {e}")
          return
  
  print("Model could not produce a result with 20 interation. Exiting with code 1")

def call_ai_agent(name, files, verbose):
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    contents = []
    for file in files:
        filepath = pathlib.Path(file)
        part = types.Part.from_bytes(
            data=filepath.read_bytes(),
            mime_type="image/jpeg"
        )
    
    contents.append(part)

    ai_agent_loop(client, name, contents, verbose)
    
#def test():
    # for _ in range(20):
  #     try:
  #         generated_content = client.models.generate_content(
  #             model="gemini-3-flash-preview",
  #             contents=contents,
  #             config=types.GenerateContentConfig(
  #                 tools=[available_functions], system_instruction=system_prompt
  #             )
  #         )

  #         if verbose:
  #            print(f"Generate content: {generated_content}")

  #         usage_metadata = generated_content.usage_metadata    
  #         if usage_metadata:
  #           if verbose:
  #             print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
  #             print(f"Response tokens: {usage_metadata.candidates_token_count}")
          
  #           cadidates = generated_content.candidates
  #           if cadidates:
  #               for candidate in cadidates:
  #                   parts = candidate.content.parts
  #                   function_results = []
  #                   if parts:
  #                     for part in parts:
                          
  #                         function_call = part.function_call

  #                         if function_call:

  #                           function_call_result = call_function(function_call, verbose)
                          
  #                           if not function_call_result.parts:
  #                               raise Exception("function_call_result.parts does not exists ")
                            
  #                           function_call_result_part = function_call_result.parts[0]
                            
  #                           if not function_call_result_part.function_response or not function_call_result_part.function_response.response:
  #                               raise Exception("function_call_result response does not exists")
                            
  #                           function_results.append(function_call_result_part)
                            
  #                           if verbose:
  #                               print(f"-> {function_call_result.parts[0].function_response.response}")
  #                         else:
  #                           print(part.generated_text)
  #                           return

  #                   contents.append(candidate.content)
  #                   if(function_results):
  #                     contents.append(types.Content(role="user", parts=function_results))

  #           else:
  #             raise RuntimeError("Failed to connect to Gemini API")