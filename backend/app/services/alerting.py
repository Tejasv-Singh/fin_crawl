class AlertService:
    def send_alert(self, doc_title: str, score: int, reason: str = ""):
        """
        Sends an alert if risk score is high.
        For MVP, this logs to stdout.
        """
        if score >= 75:
            # In a real app, this would send to Slack/Email
            alert_msg = f"🚨 [ALERT] High Risk Detected! doc='{doc_title}' score={score} reason='{reason}'"
            print("\n" + "="*50)
            print(alert_msg)
            print("="*50 + "\n")
            return True
        return False

alert_service = AlertService()
