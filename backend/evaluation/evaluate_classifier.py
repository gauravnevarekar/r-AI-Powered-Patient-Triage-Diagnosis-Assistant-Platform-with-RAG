import os
import csv
from sklearn.metrics import classification_report, confusion_matrix
from backend.app.services.classifier_service import classifier_service

def evaluate():
    print("=" * 70)
    print(" HEALTHBRIDGE AI: MULTI-DISEASE CLASSIFIER EVALUATION METRICS")
    print("=" * 70)

    # Read ground truth dataset rows
    rows = classifier_service.rows
    y_true = []
    y_pred = []
    
    urgent_conditions = [r['condition'] for r in rows if r['urgency'] in ['EMERGENCY_IMMEDIATE', 'URGENT_12_24_HRS']]

    correct_urgent = 0
    false_negatives_urgent = 0

    for r in rows:
        true_cond = r['condition']
        symptoms_input = r['symptoms']
        
        pred_res = classifier_service.predict(symptoms_input)
        pred_cond = pred_res['primary_condition']

        y_true.append(true_cond)
        y_pred.append(pred_cond)

        if true_cond in urgent_conditions:
            if pred_cond == true_cond or pred_res['urgency'] in ['EMERGENCY_IMMEDIATE', 'URGENT_12_24_HRS']:
                correct_urgent += 1
            else:
                false_negatives_urgent += 1

    total_urgent = len(urgent_conditions)
    fnr_urgent = (false_negatives_urgent / total_urgent) * 100 if total_urgent > 0 else 0.0

    report = classification_report(y_true, y_pred, zero_division=0)
    print("\n[Per-Class Classification Performance Report]")
    print(report)

    print("-" * 70)
    print(f" Total Multi-Disease Classes Evaluated : {len(set(y_true))}")
    print(f" Total Urgent Test Samples            : {total_urgent}")
    print(f" Correctly Triaged Urgent Samples     : {correct_urgent}")
    print(f" Urgent False Negatives (FN)          : {false_negatives_urgent}")
    print(f" CRITICAL URGENT FALSE NEGATIVE RATE  : {fnr_urgent:.2f}%")
    print("-" * 70)
    
    if fnr_urgent <= 5.0:
        print(">> CLASSIFIER EVALUATION PASSED: False Negative Rate on Urgent Conditions is within safe clinical limits (< 5%).")
    else:
        print(">> WARNING: High False Negative Rate detected. Retraining feedback required.")

if __name__ == "__main__":
    evaluate()
