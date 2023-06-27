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

        _ln = len(messages_conversation)

        if i == _ln:  # TODO handle all exceptions as a exception stack trace
            NluException.raise_nlu_exception(OwnResponseCodes.ONLY_BOT_IS_IN_CONVERSATION)

        if i - _ln == 0:
            NluException.raise_nlu_exception(OwnResponseCodes.ONLY_HUMAN_IS_IN_CONVERSATION)

        return messages_conversation[i:]

    def form_bot_started_conversations_array(self, messages_conversation_array: List[List[Message]]):
        _: List[List[Message]] = []
        for messages_conversation in messages_conversation_array:
            bot_started_conversation = self.begin_conversation_with_bot(messages_conversation)
            _.append(bot_started_conversation)
        return _

    # <reply based conversation array>

    def form_reply_based_conversation(self, messages_conversation: List[Message]) -> Reply:
        _first_message = messages_conversation[0]
        _first_reply: Reply = Reply(is_bot=_first_message.is_bot, phrases=[_first_message.text])
        _current_reply: Reply = _first_reply

        for message in messages_conversation:
            _text = f" {message.text} ".lower()
            if message.is_bot == _current_reply.is_bot:
                _current_reply.phrases.append(_text)
            else:
                _new_reply = Reply(is_bot=message.is_bot, phrases=[message.text])
                _current_reply.next_reply = _new_reply
                _current_reply = _new_reply

        return _first_reply

    def form_reply_based_conversation_array(self,
                                            bot_started_messages_conversation_array: List[List[Message]]) \
            -> List[Reply]:

        _: List[Reply] = []

        for messages_conversation in bot_started_messages_conversation_array:
            reply_conversation = self.form_reply_based_conversation(messages_conversation)
            _.append(reply_conversation)

        return _

    # </reply based conversation array>

    # <parse intent reply>

    def parse_each_reply_intent_in_conversation_array(self, reply_based_conversation_array: List[Reply]) -> List[Reply]:
        for reply in reply_based_conversation_array:
            self.parse_reply_intent_in_deep(reply)

        return reply_based_conversation_array

    def parse_reply_intent_in_deep(self, reply: Reply):

        if (self.intent_handler.intent_matrix is None) or (self.intent_handler.word_intent_pairs is None):
            self.intent_handler._intent_matrix, self.intent_handler._word_intent_pairs = self.intent_handler.get_intent_matrix()

        if self.intent_handler.intent_weights is None:
            self.intent_handler._intent_weights = self.intent_handler.get_intent_weights()

        _next_reply = reply
        reply.intent = self.intent_handler.parse_reply_intent(reply)

        while _next_reply.next_reply is not None:
            _next_reply = _next_reply.next_reply
            _next_reply.intent = self.intent_handler.parse_reply_intent(_next_reply)

        # return _init_reply

    # </parse intent reply>

    # <conversation tree builder>
    def form_conversation_tee(self, reply_conversation_array):
        # 1. Find collection of replies with unique intention and place them in the array
        # 2. For each reply with unique intent create a branch in current json with it's intent
        # 3. If there is one more reply in linked list take next reply and for to #1

        _init_reply = reply_conversation_array[0]
        _jsn = {
            "is_bot": _init_reply.is_bot,
            "intent": _init_reply.intent,
            "phrases": [],
            "replies": []
        }  # json.dumps({})

        for reply in reply_conversation_array:
            _jsn["phrases"].extend(reply.phrases)

        for reply in reply_conversation_array:
            self.conversation_tree_add_intent_branch(_jsn["replies"], reply)

        return [_jsn]

    def conversation_tree_add_intent_branch(self, _jsn_replies_arr, reply: Reply):
        # function that will be called recursively
        _reply = {
            "is_bot": reply.is_bot,
            "intent": reply.intent,
            "phrases": reply.phrases,
            "replies": []
        }
        _jsn_replies_arr.append(_reply)

        if reply.next_reply is not None:
            self.conversation_tree_add_intent_branch(_reply["replies"], reply.next_reply)

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

        reply_conversation_array = self.form_reply_based_conversation_array(
            bot_started_messages_conversation_array)

        #  4. parse intent of each reply

        self.parse_each_reply_intent_in_conversation_array(reply_conversation_array)

        #  5. form intent based three

        return self.form_conversation_tee(reply_conversation_array)
# </conversation tree builder>
