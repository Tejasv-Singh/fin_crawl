import sys
import os

# Add backend to path so we can import services
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.scoring import scoring_service

TEST_CASES = [
    {
        "text": "The company reported solid revenue growth. Auditor issued a standard unqualified opinion.",
        "expected_risk": "LOW",
        "label": "Normal Report"
    },
    {
        "text": "We have received a subpoena from the DOJ regarding potential fraud. Our auditor resigned last week.",
        "expected_risk": "HIGH",
        "label": "Fraud Case"
    },
    {
        "text": "There is substantial doubt about our ability to continue as a going concern due to default on debt covenants.",
        "expected_risk": "HIGH",
        "label": "Bankruptcy Risk"
    },
    {
        "text": "New product launch was successful. Market share increased by 5%.",
        "expected_risk": "LOW",
        "label": "Growth News"
    },
     {
        "text": "Material weakness identified in internal controls over financial reporting.",
        "expected_risk": "HIGH",
        "label": "Material Weakness"
    }
]

def run_backtest():
    print("Running Backtest on Scoring Engine...")
    print("-" * 60)
    print(f"{'Label':<20} | {'Score':<10} | {'Predicted':<10} | {'Expected':<10} | {'Result':<10}")
    print("-" * 60)
    
    passed = 0
    total = len(TEST_CASES)
    
    for case in TEST_CASES:
        score = scoring_service.calculate_score(case['text'])
        predicted = "HIGH" if score >= 75 else "LOW"
        
        is_pass = predicted == case['expected_risk']
        if is_pass:
            passed += 1
            
        result_icon = "✅ PASS" if is_pass else "❌ FAIL"
        
        print(f"{case['label']:<20} | {score:<10} | {predicted:<10} | {case['expected_risk']:<10} | {result_icon:<10}")

    print("-" * 60)
    accuracy = (passed / total) * 100
    print(f"Accuracy: {accuracy:.2f}% ({passed}/{total})")
    
    if accuracy >= 80:
        print("\n✅ Backtest PASSED (Threshold: 80%)")
        sys.exit(0)
    else:
        print("\n❌ Backtest FAILED")
        sys.exit(1)

if __name__ == "__main__":
    run_backtest()
