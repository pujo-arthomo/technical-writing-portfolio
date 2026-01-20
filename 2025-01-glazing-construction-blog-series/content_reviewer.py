import re
from collections import Counter

def load_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return ""

def word_count(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def readability_score(text):
    # Simple Flesch-Kincaid approximation
    sentences = len(re.split(r'[.!?]+', text))
    words = word_count(text)
    syllables = sum(len(re.findall(r'[aeiouy]+', word.lower())) for word in re.findall(r'\b\w+\b', text))
    if sentences == 0 or words == 0:
        return 0
    score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
    return round(score, 1)

def keyword_check(text, keywords):
    found = {kw: text.lower().count(kw.lower()) for kw in keywords}
    return found

if __name__ == "__main__":
    filename = input("Enter markdown file to review: ").strip()
    text = load_file(filename)
    
    if text:
        print(f"\nReview for {filename}")
        print(f"Word count: {word_count(text)}")
        print(f"Approximate Flesch reading ease: {readability_score(text)} (higher = easier)")
        
        keywords = ["glazing", "energy", "construction", "glass", "coating"]
        found = keyword_check(text, keywords)
        print("\nKeyword frequency:")
        for kw, count in found.items():
            print(f"  {kw}: {count}")
        
        print("\nReview complete. Use this to guide modifications.")
