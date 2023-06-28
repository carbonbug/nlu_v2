import os
import json

import pytest
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient



import test_utils
from NluServer import app


client = TestClient(app)

path = Path(os.getcwd())
path_to_conversations = f"{path}/dialogs"
conversations = test_utils.load_all_conversations(path_to_conversations)



def test_build_conversation_tree():
    _data = json.dumps(conversations)
    response = client.post("/form_conversation_tree", data=_data, headers={'Content-Type': 'application/json'})

    _json_conversation_tree = response.text

    test_utils.dict_to_json(_json_conversation_tree, "dialogs_tree")


def test_parse_text_intent():
    phrase_intent = {
        "привет": "greeting",
        "да здравствуйте": "greeting",
        "алло": "greeting",
        "допустим да": "agreement",
        "я не ничего не знаю, не звоните сюда больше": "farewell",
        "да буду рад с вами поговорить": "agreement"
    }

    phrases = [*phrase_intent.keys()]

    for phrase in phrases:
        response = client.get(f"/parse?q={phrase}")
        parsed_intent = json.loads(response.text)

        print(phrase)
        assert parsed_intent["message"] == phrase_intent[phrase]
