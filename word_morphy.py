import re
import pymorphy2
from collections import Counter, defaultdict

morph = pymorphy2.MorphAnalyzer()

def get_morphological_info(text):
    
    lines = text.splitlines()
    total_counts = Counter()
    line_counts = []

    for line in lines:
        words = re.findall(r'\w+', line.lower())
        lemmas = []

        for word in words:
            lemma = morph.parse(word)[0].normal_form
            lemmas.append(lemma)
        counter = Counter(lemmas)
        line_counts.append(counter)
        total_counts.update(counter)

    result = {}

    for lemma in total_counts:
        result[lemma] = {
            "total_count": total_counts[lemma],
            "line_counts": [line_count.get(lemma, 0) for line_count in line_counts]
        }
    return result