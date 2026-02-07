import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.call_function import available_functions, call_function
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

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

    for _ in range(20):
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

        if len(gemini_content.candidates) != 0:
            for candidate in gemini_content.candidates:
                messages.append(candidate.content)
    
        if gemini_content.function_calls:
            for function_call in gemini_content.function_calls:
                #print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call, args.verbose)
                if len(function_call_result.parts) == 0:
                    raise Exception("Empty parts list")
                if not function_call_result.parts[0].function_response:
                    raise Exception("Missing function response")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Missing response")
                
                #We have a valid response!
                function_results = []
                function_results.append(function_call_result.parts[0])
                messages.append(types.Content(role="user", parts=function_results))

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(gemini_content.text)
            return
        
    print("Maximum number of loops reached.")
    exit(1)


if __name__ == "__main__":
    main()

