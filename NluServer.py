import os
import uvicorn
from typing import List

from fastapi import FastAPI
from fastapi import Query
from fastapi import Body

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from token_throttler import TokenBucket, TokenThrottler
from token_throttler.storage import RuntimeStorage

from handlers.IntentHandler import IntentHandler
from handlers.ConverstaionHandler import ConversationHandler

from handlers.router import router as handler_router
from handlers.NluException import NluException

throttler: TokenThrottler = TokenThrottler(cost=1, storage=RuntimeStorage())
throttler.add_bucket(identifier="user_id", bucket=TokenBucket(replenish_time=10, max_tokens=5))

_path = os.path.dirname(__file__)
_conversations_path = f"{_path}/dialogs"
_intent_matrix_path = f"{_path}/addition/intent_info/intent_matrix.txt"
_intent_weights_path = f"{_path}/addition/intent_info/intent_weights.txt"

_intent_handler = IntentHandler(_intent_matrix_path, _intent_weights_path)
_conversation_handler = ConversationHandler(_intent_handler)

app = FastAPI()
app.include_router(handler_router)


@app.post("/form_conversation_tree")
def form_conversation_tree(conversations_arr: List[List[dict]]):
    '''
    :param conversations_arr: is a array of converstaions
    :return:

    json like conversation tree where branches are formed from different intents

    1. convert each raw conversation into message flor conversation
    2. start each message based conversataion with bot message
    3. convert conversation into reply based structure
    4. parse intent of each reply
    5. form intent based three

    '''

    try:

        _json_tree = _conversation_handler.form_intent_branched_conversation_three(conversations_arr)

        return JSONResponse(status_code=200, content={"message": _json_tree})
    except NluException as nlu_ex:
        return JSONResponse(status_code=nlu_ex.code, content={"message": nlu_ex.message})

    except Exception as ex:
        print(ex)
        JSONResponse(status_code=500, content={"message": "Internal unexpected exception. Ask a administrator"})


@app.get("/parse")
def parse_phrase_intent(q: str):
    try:
        r = _intent_handler.parse_intent(q)
        return JSONResponse(status_code=200, content={"message": r})
    except NluException as nlu_ex:
        return JSONResponse(status_code=nlu_ex.code, content={"message": nlu_ex.message})

    except Exception as ex:
        JSONResponse(status_code=400, content={"message": "Internal unexpected exception. Ask a administrator"})


if __name__ == "__main__":

    uvicorn.run(app)

