import re

class ScoringService:
    RISK_KEYWORDS = [
        "bankruptcy", "default", "material weakness", "going concern",
        "investigation", "litigation", "subpoena", "restatement",
        "adverse opinion", "fraud", "resignation",
        # Benign but scorable terms for MVP/Demo sensitivity
        "risk", "debt", "uncertainty", "loss", "challenges", "volatility",
        "decline", "negative", "fail", "difficult"
    ]

    @staticmethod
    def calculate_score(text: str) -> int:
        """
        Calculates a risk score (0-100) based on heuristic keywords.
        Higher score = Higher Risk.
        """
        if not text:
            return 0
            
        text_lower = text.lower()
        risk_count = 0
        
        for kw in ScoringService.RISK_KEYWORDS:
            # Simple count of occurrences
            count = len(re.findall(r'\b' + re.escape(kw) + r'\b', text_lower))
            risk_count += count

        # Heuristic formula: 10 points per keyword occurrence, capped at 100
        score = min(100, risk_count * 10)
        
        # Base logic: If "going concern" or "material weakness" is present, min score is 75
        if "going concern" in text_lower or "material weakness" in text_lower:
            score = max(score, 75)

        return score

scoring_service = ScoringService()
