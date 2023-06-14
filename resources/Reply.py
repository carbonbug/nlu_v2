class Reply:
    def __init__(self, phrases=None, is_bot: bool = True, intent: str = "default"):
        if phrases is None:
            phrases = []
        self.intent = intent
        self.is_bot = is_bot
        self.phrases = phrases



