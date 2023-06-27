
import json
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient


import test_utils
from NluServer import app


client = TestClient(app)

path = Path(os.getcwd())
path_to_conversations = f"{path}/dialogs"
conversations = test_utils.load_all_conversations(path_to_conversations)


def test_1():
    _data = json.dumps(conversations)
    _json_conversation_tree = client.post("/form_conversation_tree", data=_data, headers={'Content-Type': 'application/json'})
    pass

if __name__ == "__main__":
    test_1()
