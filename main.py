import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.call_function import available_functions
from functions.get_files_info import get_files_info, schema_get_files_info

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("API key not found.")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    gemini_content = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
            )
        )

    if gemini_content.usage_metadata == None:
        raise RuntimeError("Failed API request.")
    else:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {gemini_content.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {gemini_content.usage_metadata.candidates_token_count}")

    if gemini_content.function_calls:
        for function_call in gemini_content.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(gemini_content.text)


if __name__ == "__main__":
    main()

