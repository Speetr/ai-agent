import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("API key not found.")

    client = genai.Client(api_key=api_key)
    gemini_content = client.models.generate_content(model="gemini-2.5-flash", contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    if gemini_content.usage_metadata == None:
        raise RuntimeError("Failed API request.")
    else:
        print(f"Prompt tokens: {gemini_content.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {gemini_content.usage_metadata.candidates_token_count}")
    print(f"Response: {gemini_content.text}")


if __name__ == "__main__":
    main()

