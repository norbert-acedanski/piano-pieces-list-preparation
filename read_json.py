import json


def read_json(file_path: str) -> list:
    json_file = open(file_path, "r")
    file_content = json.load(json_file)
    json_file.close()
    return file_content["all piano pieces"]
