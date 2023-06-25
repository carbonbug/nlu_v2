import os
import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from addition import OwnResponseCodes
from handlers.NluException import NluException

from resources import Reply

router = APIRouter(
    prefix="/intent",
    tags=["Intent"],
    responses={404: {"description": "Intent handler: not found"}},
)


class IntentHandler:
    def __init__(self, intent_matrix_path=None, intent_weights_path=None):
        self._intent_matrix_path = intent_matrix_path
        self._intent_weights_path = intent_weights_path

        self._intent_matrix = None
        self._intent_weights = None
        self._word_intent_pairs = None

    # @router.get("/get_intent_matrix")
    def get_intent_matrix(self):
# TODO переделать считываение файла с распознаванием матриц
        if self._intent_matrix_path is None:
            nlu_exception = OwnResponseCodes.INTENT_MATRIX_FILE_PATH_IS_NONE
            raise NluException(message=nlu_exception["message"], code=nlu_exception["code"])

        if not os.path.exists(self._intent_matrix_path):
            nlu_exception = OwnResponseCodes.INTENT_MATRIX_FILE_PATH_IS_NONE
            raise NluException(message=nlu_exception["message"], code=nlu_exception["code"])

        file = open(self._intent_matrix_path)
        lines = file.readlines()
        file.close()

        lines = [l for l in lines if l != "\n"]
        word_intent_pairs = {}
        for l in lines:
            splited = l.split("*")
            intent = splited[0]
            intent_word = splited[1]
            word_intent_pairs[intent.strip()] = intent_word.strip()

        intent_words = {x for x in word_intent_pairs.keys()}
        intents = set([word_intent_pairs[x] for x in intent_words])
        return dict.fromkeys(intents, 0), word_intent_pairs

    def get_intent_weights(self):
        if self._intent_weights_path is None:
            nlu_exception = OwnResponseCodes.INTENT_MATRIX_WEIGHTS_FILE_PATH_IS_NONE
            raise NluException(message=nlu_exception["message"], code=nlu_exception["code"])

        if not os.path.exists(self._intent_weights_path):
            nlu_exception = OwnResponseCodes.INTENT_MATRIX_WEIGHTS_FILE_PATH_IS_NONE
            raise NluException(message=nlu_exception["message"], code=nlu_exception["code"])

        file = open(self._intent_weights_path)
        lines = file.readlines()
        file.close()

        lines = [l for l in lines if l != "\n"]
        _intent_weights = {}
        for l in lines:
            splited = l.split("=")
            intent = splited[0]
            intent_coef = splited[1]
            _intent_weights[intent.strip()] = float(intent_coef.strip())
        return _intent_weights

    # @router.post("/parse_intent")

    # @router.post("/parse")
    def parse_intent(self, text: str):
        if (self._intent_matrix is None) or (self._word_intent_pairs is None):
            self._intent_matrix, self._word_intent_pairs = self.get_intent_matrix()

        if self._intent_weights is None:
            self._intent_weights = self.get_intent_weights()

        _intent_matrix = self._intent_matrix.copy()

        for intent_word in self._word_intent_pairs:
            if f" {intent_word} " in f" {text} " :
                intent = self._word_intent_pairs[intent_word]
                _intent_matrix[intent] += self._intent_weights[intent]

        v = list(_intent_matrix.values())
        k = list(_intent_matrix.keys())
        if max(v) == 0:
            _intent = "default"
        else:
            _intent = k[v.index(max(v))]
        return _intent
        # return JSONResponse(status_code=200, content={"intent": _intent})
