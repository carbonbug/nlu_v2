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

        # 1. Start with init_reply
        # 2. create array of messages consisted from sub_arrays with same message is_bot statuses
        # 3. for each sub_array create array of replies with unique intents
        _init_message = messages_conversation[0]
        _init_reply: Reply = Reply(is_bot=_init_message.is_bot, phrases=[_init_message.text])
        _text = f" {_init_message.text} ".lower()
        _init_reply.intent = self.intent_handler.parse_intent(_text)



        _bot_status_arr = []
        _sub_status_arr = [_init_message]
        for message in messages_conversation[1: ]:
            if _sub_status_arr[-1].is_bot == message.is_bot:
                _sub_status_arr.append(message)
            else:
                _bot_status_arr.append(_sub_status_arr)
                _sub_status_arr = [message]

        del _sub_status_arr

        _same_bot_status_diff_intent_replies_arr = []
        for _sub_messages in _bot_status_arr:
            _sub_messages_intents = {}

            # collect all replies with same bot statuses and unique intent in one dict
            for _sub_message in _sub_messages:
                _intent = self.intent_handler.parse_intent(_sub_message.text)
                if _intent in _sub_messages_intents.keys():
                    _sub_messages_intents[_intent].append(
                        Reply(phrases=[_sub_message.text],
                              is_bot=_sub_message.is_bot,
                              intent=_intent))

                else:
                    _sub_messages_intents[_intent] = [Reply(phrases=[_sub_message.text],
                                                                is_bot=_sub_message.is_bot,
                                                                intent=_intent)]

            for _sub_message in _sub_messages:
            # join all replies with same intent
            # put all phrases into first reply in the array
                for _intent in _sub_messages_intents:
                    if len(_sub_messages_intents[_intent]) > 0:
                        for _ in _sub_messages_intents[_intent][1:]:
                            _sub_messages_intents[_intent][0].phrases.extend(_.phrases)

                    _same_bot_status_diff_intent_replies_arr.append(_sub_messages_intents[_intent])



        # create a d
        _init_reply = _same_bot_status_diff_intent_replies_arr[0][0] # it will be the first bot reply and its unique
        _next_reply = _init_reply
        for _bunch_reply in _same_bot_status_diff_intent_replies_arr[1:]:
            for _reply in _bunch_reply:
                _next_reply.next_replies.append(_reply)

            _next_reply = _next_reply.next_replies[-1]


        return _init_reply

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

        _next_replies = reply.next_replies
        reply.intent = self.intent_handler.parse_intent(reply.phrase)

        while len(_next_replies) > 0:
            self.intent_handler.parse_each_reply_intent(_next_replies)
            _next_replies = _next_replies[-1].next_replies

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
            self.conversation_tree_add_unque_intent_reply_branch(_jsn["replies"], reply)

        return [_jsn]

    def conversation_tree_add_unque_intent_reply_branch(self, _jsn_replies_arr, reply: Reply):
        # function that will be called recursively
        for _reply in reply.next_replies:
            _sub_reply = {
                "is_bot": reply.is_bot,
                "intent": reply.intent,
                "phrases": reply.phrases,
                "replies": []

            }
            _jsn_replies_arr.append(_sub_reply)

        if len(reply.next_replies) > 0:
            self.conversation_tree_add_unque_intent_reply_branch(_jsn_replies_arr[-1]["replies"], reply.next_replies[-1])



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

        #  3. parse each message intent and convert messages flow into replies linked list
        #
        #  convert conversation into reply based structure

        reply_conversation_array = self.form_reply_based_conversation_array(
            bot_started_messages_conversation_array)

        # NO NEEDED anymore
        #  4. parse intent of each reply
        # self.parse_each_reply_intent_in_conversation_array(reply_conversation_array)

        #  5. form intent based three

        return self.form_conversation_tee(reply_conversation_array)
# </conversation tree builder>
