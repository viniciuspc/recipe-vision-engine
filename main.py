import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main():
    generated_content = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents="Explain how AI works in a few words"
    )
    
    print(generated_content.text)
    


if __name__ == "__main__":
    main()
