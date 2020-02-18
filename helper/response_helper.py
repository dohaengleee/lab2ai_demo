from flask import make_response
import json
from helper.np_encoder import NpEncoder


class ResponseHelper:
    def __init__(self):
        self.ensure_ascii = False
        self.indent = "\t"
        self.cls = NpEncoder
        self.content_type = "application/json"

    def write(self, dictionary_result):
        json_data = json.dumps(dictionary_result, ensure_ascii=self.ensure_ascii, indent=self.indent, cls=self.cls)
        res = make_response(json_data)
        res.headers['Content-Type'] = self.content_type

        return res
