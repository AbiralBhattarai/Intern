from src.ports.input.CampaignAnalyzerPort import CampaignAnalyzerPort
from src.domain.contract.SentimentAnalyzer import SentimentAnalyzer

class RuleBasedCampaignAnalyzer(CampaignAnalyzerPort):
    """Simple rule-based campaign analyzer implementation. Analyzes video scripts for sentiment, hooks, CTAs, and pacing."""
    def __init__(self,sentiment_analyzer:SentimentAnalyzer,hook_words: list,cta_words: list):
        """Initialize with dependencies."""
        self.sentiment_analyzer = sentiment_analyzer
        self.hook_words = hook_words
        self.cta_words = cta_words


    def _analyze_sentiment(self,script: str):
        """Use sentiment analyzer to get polarity scores for the script."""
        return self.sentiment_analyzer.polarity_scores(
            script
        )


    def _analyze_hook(self,script: str):
        """Count occurrences of hook words in the script to evaluate the strength of the hook."""
        script = script.lower()
        return sum(
            script.count(word.lower())
            for word in self.hook_words
        )


    def _analyze_cta(self,script: str):
        """Count occurrences of CTA words in the script to evaluate the strength of the call-to-action."""
        script = script.lower()
        last_20_percent = script[int(0.8 * len(script)):]
        return sum(last_20_percent.count(word.lower()) for word in self.cta_words)


    def _analyze_pacing(self,script: str,duration: int):
        """Calculate words per second to evaluate pacing of the video script."""
        words = len(script.split())
        if words == 0:
            return 0
        return words/duration


    def analyze(self,campaign_data: dict) -> dict:
        """Main method to analyze campaign data and return metrics."""
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