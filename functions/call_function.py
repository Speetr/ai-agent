from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info

available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)