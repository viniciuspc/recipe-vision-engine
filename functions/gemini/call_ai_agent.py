import os
import pathlib
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from prompts import system_prompt
from functions.tools.call_function import available_functions, call_function
from functions.gemini.exponetial_backoff import call_with_retry

MODEL_ID = "gemini-3-flash-preview"

def generate_content(client, contents):
    return client.models.generate_content(
              model=MODEL_ID,
              contents=contents,
              config=types.GenerateContentConfig(
                  tools=[available_functions], system_instruction=system_prompt
              )
          )


def ai_agent_loop(client, name, contents, verbose):
  for _ in range(20):
      try:
          generate_content_args = {
              "client": client,
              "contents": contents
          }
          generated_content = call_with_retry(generate_content, generate_content_args)
          
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
    
    if(verbose):
        print(f"Requested Contents: {len(contents)}")

    ai_agent_loop(client, name, contents, verbose)
