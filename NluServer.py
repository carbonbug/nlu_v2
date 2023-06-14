import os
import uvicorn
from fastapi import FastAPI
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

_path = os.path.abspath(os.getcwd())
_conversations_path = f"{_path}/dialogs"
_intent_matrix_path = f"{_path}/resources/intent_matrix.txt"
_intent_weights_path = f"{_path}/resources/intent_weights.txt"

_intent_handler = IntentHandler(_intent_matrix_path, _intent_weights_path)
_conversation_handler = ConversationHandler(_conversations_path, _intent_handler)

app = FastAPI()
app.include_router(handler_router)


@app.get("/")
async def root():
    if throttler.consume(identifier="user_id"):
        return JSONResponse(status_code=200, content={"message": "Hello User, you have access!"})
    return JSONResponse(status_code=429, content={"message": "You've reached the limit!"})


@app.post("/form_conversation_graph")
async def form_conversation_graph(conversation_array):
    try:
        # get intent matrix
        # get intent weights

        # load converstaion
        # start converstaions with bot messages
        # convert messages in replies flow
        # form intent based conversation three


        conversation_as_intent_replies_flow = _conversation_handler.form_conversation_array_from_intent_replies(conversation_array)


        return JSONResponse(status_code=200, content={"message": None})
    except NluException as nlu_ex:
        return JSONResponse(status_code=nlu_ex.code, content={"message": nlu_ex.message})

    except Exception as ex:
        JSONResponse(status_code=500, content={"message": "Internal unexpected exception. Ask a administrator"})
    pass





@app.get("intent/get_intent_matrix")
async def get_intent_matrix():
    try:
        r = _intent_handler.get_intent_matrix()
        return JSONResponse(status_code=200, content={"message": r})
    except NluException as ex:
        return JSONResponse(status_code=ex.code, content={"message": ex.message})

    except Exception as ex:
        JSONResponse(status_code=500, content={"message": ex.__cause__})


@app.get("intent/get_intent_weights")
async def get_intent_weights():
    try:
        r = _intent_handler.get_intent_weights()
        return JSONResponse(status_code=200, content={"message": r})
    except NluException as nlu_ex:
        return JSONResponse(status_code=nlu_ex.code, content={"message": nlu_ex.message})

    except Exception as ex:
        JSONResponse(status_code=400, content={"message": "Internal unexpected exception. Ask a administrator"})


@app.post("/parse_phrase_intent")
async def parse_phrase_intent(message_object):
    try:
        r = _intent_handler.get_intent_weights()
        return JSONResponse(status_code=200, content={"message": r})
    except NluException as nlu_ex:
        return JSONResponse(status_code=nlu_ex.code, content={"message": nlu_ex.message})

    except Exception as ex:
        JSONResponse(status_code=400, content={"message": "Internal unexpected exception. Ask a administrator"})


@app.post("/make_conversation_starts_with_bot")
async def make_conversation_starts_with_bot():
    pass


@app.post("/form_conversations_into_replies_flow")
async def form_conversations_into_replies_flow(conversation_array):
    pass


if __name__ == "__main__":
    # start the application
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # read all files manually
    # put files into api and get conversation three
    # save conversation three into files

# CONVERATION FILES

# load conversations 
# convert into dialog


# INTENTS

# load intent matrix 
# load intent weights 


# parse intent
