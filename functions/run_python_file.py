import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path.split(".")[-1] != "py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args:
            command.extend(args)

        cmd_result = subprocess.run(command, capture_output=True, text=True, timeout=30)

        result_string = ""
        if cmd_result.returncode != 0:
            result_string += f"Process exited with code {cmd_result.returncode}\n"
        if len(cmd_result.stdout) == 0 and len(cmd_result.stderr) == 0:
            result_string += "No output produced\n"
        else:
            result_string += f"STDOUT: {cmd_result.stdout}\n"
            result_string += f"STDERR: {cmd_result.stderr}\n"
        
        return result_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file along with any necessary arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments to pass to the python file you are running",
                items=types.Schema(type=types.Type.STRING)
            )
        },
        required=["file_path"]
    )
)