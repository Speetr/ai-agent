import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    contents = ""
    try:
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            contents = contents + f"- {item}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}\n"
    except Exception as e:
        return f'Error: {e}'
    return contents.rstrip("\n")