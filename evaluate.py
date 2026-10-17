import json
import time
from classifier import classify_ticket


def load_examples(path):
    try:
        with open(file=path, encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(e)

def evaluate(examples, delay = 2):
    results = []
    for example in examples:
        try:
            answer = classify_ticket(example["text"])
        except Exception as e:
            print(f"API Error: {e}")
            answer = None

        predicted = answer["category"] if answer else None
        results.append({"text": example["text"],"expected":example["category"],"predicted": predicted})
        time.sleep(delay)
    return results

def print_report(results):
    total = len(results)
    correct = 0
    unusable = 0
    per_category = {}

    for result in results:
        category = result["expected"]
        if category not in per_category:
            per_category[category] = {"total": 0, "correct": 0}
        per_category[category]["total"] += 1

        if result["expected"] == result["predicted"]:
            per_category[category]["correct"] += 1
            correct += 1
        elif  result["predicted"] is None:
            unusable += 1

    print("=== Evaluation ===")
    print(f"Accuracy: {correct}/{total} ({correct / total * 100:.1f}%)")
    print(f"Unusable answers: {unusable}")
    print()

    for category, counts in per_category.items():
        print(f"{category}: {counts['correct']}/{counts['total']}")

    print("\nMistakes")
    for result in results:
        if result["expected"] != result["predicted"]:
            print(f"expected: {result['expected']}, got {result['predicted']}: {result['text']}")

def main():
    examples = load_examples("examples.json")
    results = evaluate(examples)
    print_report(results)

if __name__ == "__main__":
    main()

        