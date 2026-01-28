import sys
import os
sys.path.append(os.path.abspath('src')) # Allow importing from src
from model import get_rag_chain

# Define expected "Ground Truth"
test_cases = [
    {"q": "What happens if a pilot is TMU?", "expected_page": "442"},
    {"q": "What is the GENERAL sick leave policy for ground staff?", "expected_page": "425"},
    {"q": "Who is covered under POSH policy?", "expected_page": "488"}
]

def run_accuracy_check():
    chain = get_rag_chain()
    passed = 0
    print("\n--- Starting RAG Accuracy Test ---")
    
    for case in test_cases:
        response = chain.invoke({"input": case['q']})
        if case['expected_page'] in response:
            print(f"✅ PASS | Q: {case['q'][:30]}... | Cited: Page {case['expected_page']}")
            passed += 1
        else:
            print(f"❌ FAIL | Q: {case['q'][:30]}... | Expected: Page {case['expected_page']}")

    print(f"\nFinal Accuracy: {(passed/len(test_cases))*100}%")

if __name__ == "__main__":
    run_accuracy_check()