import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from resources.Reply import Reply
from resources.Message import Message

from handlers.IntentHandler import IntentHandler

from addition import OwnResponseCodes
from handlers.NluException import NluException

router = APIRouter()


class ConversationHandler:
    def __init__(self, intent_handler: IntentHandler):
        self.intent_handler = intent_handler

    @staticmethod
    def begin_conversation_with_bot(self, conversation):
        i = 0
        for n, message in enumerate(conversation):
            if message["is_bot"]:
                i = n
                break
        if i == len(conversation):
            NluException.raise_nlu_exception(OwnResponseCodes.ONLY_BOT_IS_IN_CONVERSATION)

        if i == 0:
            NluException.raise_nlu_exception(OwnResponseCodes.ONLY_HUMAN_IS_IN_CONVERSATION)

        return conversation[i:]

    @staticmethod
    def form_conversation_array_into_reply_flow(self, conversation_array: list[list[Message]]):
        array_of_conversations = []
        for conversation in conversation_array:  # TODO things with rasing exceptions
            if len(conversation) > 0:
                continue
            _conversation_as_reply_flow = self.form_conversation_into_reply_flow(conversation)
            array_of_conversations.append(_conversation_as_reply_flow)

        return array_of_conversations

    @staticmethod
    def form_conversation_into_reply_flow(self, conversation: list[Message]):
        conversation_reply_flow: list[Reply] = []
        _conversation = self.form_conversation_into_message_flow(conversation)
        _bot_begins_conversation = self.begin_conversation_with_bot(_conversation)

        _first_message = conversation[0]
        _first_reply = Reply(
            is_bot=_first_message.is_bot,
            phrases=[_first_message.text]
        )
        conversation_reply_flow.append(_first_reply)

        for _reply in conversation[1:]:
            _text = f' {_reply.text} '.lower()
            if bool(_reply.is_bot) == conversation_reply_flow[-1].is_bot:
                conversation_reply_flow[-1].phrases.append(_text)
            else:
                r = Reply(is_bot=_reply.is_bot, phrases=[_text])
                conversation_reply_flow.append(r)

        return conversation_reply_flow

    @staticmethod
    def form_conversation_into_message_flow(self, conversation):
        message_flow = []
        for r_message in conversation:
            _ = Message(is_bot=r_message["is_bot"], text=r_message["text"])
            message_flow.append(_)
        return message_flow

    def parse_intent_in_each_reply_in_conversation(self, conversation_as_reply_flow):
        for conversation in conversation_as_reply_flow:
            for reply in conversation:
                self.intent_handler.parse_intent(reply)

        return conversation_as_reply_flow

    @staticmethod
    def form_conversation_array_from_intent_replies(self, conversation_array):

        conversation_as_reply_flow = self.form_conversation_array_into_reply_flow(conversation_array)
        conversation_as_intent_replies_flow = self.parse_intent_in_each_reply_in_conversation(
            conversation_as_reply_flow)
        return conversation_as_intent_replies_flow


