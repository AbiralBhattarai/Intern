from src.ports.input.CampaignAnalyzerPort import CampaignAnalyzerPort


class RuleBasedCampaignAnalyzer(CampaignAnalyzerPort):

    def __init__(self,sentiment_analyzer,hook_words,cta_words):
        self.sentiment_analyzer = sentiment_analyzer
        self.hook_words = hook_words
        self.cta_words = cta_words


    def _analyze_sentiment(self,script: str):
        return self.sentiment_analyzer.polarity_scores(
            script
        )


    def _analyze_hook(self,script: str):
        script = script.lower()
        return sum(
            script.count(word.lower())
            for word in self.hook_words
        )


    def _analyze_cta(self,script: str):
        script = script.lower()
        last_20_percent = script[int(0.8 * len(script)):]
        return sum(last_20_percent.count(word.lower()) for word in self.cta_words)


    def _analyze_pacing(self,script: str,duration: int):
        words = len(script.split())
        if words == 0:
            return 0
        return words/duration


    def analyze(self,campaign_data: dict) -> dict:
        script = campaign_data.get("video_script","")
        duration = campaign_data.get("video_duration_seconds",0)
        return {"sentiment": self._analyze_sentiment(script),
            "hook_score": self._analyze_hook(
                script
            ),
            "cta_score": self._analyze_cta(
                script
            ),
            "pacing": self._analyze_pacing(
                script,
                duration
            )
        }