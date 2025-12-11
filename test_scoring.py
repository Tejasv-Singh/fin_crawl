from app.services.scoring import scoring_service

def test_scoring():
    print("Testing Scoring Service...")
    
    low_risk = "This is a normal annual report. Revenue is good."
    score_low = scoring_service.calculate_score(low_risk)
    print(f"Low Risk Score: {score_low} (Expected ~0)")

    high_risk = "The company is facing bankruptcy and litigation. There is a material weakness in controls."
    score_high = scoring_service.calculate_score(high_risk)
    print(f"High Risk Score: {score_high} (Expected >0)")
    
    if score_high > 0:
        print("PASS: Scoring logic works.")
    else:
        print("FAIL: Scoring logic returned 0 for high risk text.")

if __name__ == "__main__":
    test_scoring()
