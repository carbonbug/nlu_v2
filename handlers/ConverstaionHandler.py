import json
from typing import List

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


    # into messages funcs

    def form_conversation_into_message_flow(self, dict_arr_conversation: List[dict]) -> List[Message]:

        """
        :param dict_arr_conversation:
        :return: convert json object into Message object
        """

        messages_array = []
        for r_message in dict_arr_conversation:
            _ = Message(is_bot=r_message["is_bot"], text=r_message["text"])
            messages_array.append(_)
        return messages_array

    def form_message_flow_conversation_array(self, raw_conversation_array: List[List[dict]]) -> List[List[Message]]:
        _: List[List[Message]] = []
        for raw_conversation in raw_conversation_array:
            messages_based_conversation = self.form_conversation_into_message_flow(raw_conversation)
            _.append(messages_based_conversation)
        return _

    # start with bot func
    def begin_conversation_with_bot(self, messages_conversation: List[Message]) -> List[Message]:
        i = 0
        for n, message in enumerate(messages_conversation):
            if message.is_bot:
                i = n
                break

        if i == len(messages_conversation):  # TODO handle all exceptions as a exception stack trace
            NluException.raise_nlu_exception(OwnResponseCodes.ONLY_BOT_IS_IN_CONVERSATION)

        if i == 0:
            NluException.raise_nlu_exception(OwnResponseCodes.ONLY_HUMAN_IS_IN_CONVERSATION)

        return messages_conversation[i:]

    def form_bot_started_conversations_array(self, messages_conversation_array: List[List[Message]]):
        _: List[List[Message]] = []
        for messages_conversation in messages_conversation_array:
            bot_started_conversation = self.begin_conversation_with_bot(messages_conversation)
            _.append(bot_started_conversation)
        return _

    # conversation based on replies

    def form_reply_based_conversation(self, messages_conversation: List[Message]) -> Reply:

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

    def form_reply_based_conversation_array(self,
                                            bot_started_messages_conversation_array: List[List[Message]]) \
        -> List[Reply]:

        _: List[Reply] = []

        for messages_conversation in bot_started_messages_conversation_array:
            reply_conversation = self.form_reply_based_conversation(messages_conversation)
            _.append(reply_conversation)

        return _


















    def form_conversation_array_into_reply_flow(self, conversation_array: List[List[Message]]):
        array_of_conversations = []
        for conversation in conversation_array:  # TODO things with rasing exceptions
            if len(conversation) > 0:
                continue
            _conversation_as_reply_flow = self.form_conversation_into_reply_flow(conversation)
            array_of_conversations.append(_conversation_as_reply_flow)

        return array_of_conversations


    def parse_intent_in_each_reply_in_conversation(self, conversation_as_reply_flow):
        for conversation in conversation_as_reply_flow:
            for reply in conversation:
                if not reply.is_bot:
                    self.intent_handler.parse_intent(reply)
                else:
                    reply.intent = "default"

        return conversation_as_reply_flow

    # def form_conversation_array_from_intent_replies(self, conversation_array):
    #
    #     conversation_as_messages_flow = self.form_conversation_into_message_flow(conversation_array)
    #     conversation_as_reply_flow = self.form_conversation_array_into_reply_flow(conversation_as_messages_flow)
    #     conversation_as_intent_replies_flow = self.parse_intent_in_each_reply_in_conversation(conversation_as_reply_flow)
    #     return conversation_as_intent_replies_flow

    def form_intent_branched_conversation_three(self, conversations_arr):
        """
            1. convert each raw conversation into message flor conversation
            2. start each message based conversation with bot message
            3. convert conversation into reply based structure
            4. parse intent of each reply
            5. form intent based three
        """
        #  1. convert each raw conversation into message flor conversation
        messages_conversation_array = self.form_message_flow_conversation_array(conversations_arr)

        #  2. start each message based conversation with bot message
        bot_started_messages_conversation_array = self.form_bot_started_conversations_array(messages_conversation_array)

        #  3. convert conversation into reply based structure

        reply_based_conversation_array = self.form_reply_based_conversation_array(bot_started_messages_conversation_array)