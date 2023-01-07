import codecs
import json


def read_json(file_path: str) -> list:
    with codecs.open(file_path, "r", "utf-8") as json_file:
        file_content = json.load(json_file)
    return file_content["all piano pieces"]
