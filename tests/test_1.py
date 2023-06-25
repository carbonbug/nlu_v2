
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
    info = {"payload": "value1", "test2": "value2"}
    _data = json.dumps(conversations)
    client.post("/form_conversation_graph", data=_data, headers={'Content-Type': 'application/json'})



if __name__ == "__main__":
    test_1()
