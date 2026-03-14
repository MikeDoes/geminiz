"""
AI4Privacy Demo - Verifies the ai4privacy model loads and works correctly.
Uses ai4privacy/llama-ai4privacy-multilingual-categorical-anonymiser-openpii from HuggingFace.
"""

from ai4privacy import protect

def main():
    with open("input.txt", "r") as f:
        text = f.read().strip()

    print(f"Input: {text}")

    result = protect(text, verbose=True, multilingual=True, classify_pii=True)

    print(f"Output: {result}")

    with open("output.txt", "w") as f:
        f.write(f"Input: {text}\n")
        f.write(f"Output: {result}\n")

    print("\nModel loaded and ran successfully. Results saved to output.txt")

if __name__ == "__main__":
    main()
