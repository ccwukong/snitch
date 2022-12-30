import json


def generate_config_json_template(file: str) -> None:
    try:
        with open(file, 'w') as f:
            content = {"postmanCollection": {"version": "", "filePath": "", "metadata": {
            }}, "openApi": {"version": "", "filePath": "", "metadata": {}}}

            json.dump(content, f, indent=2)
    except Exception as e:
        raise e
