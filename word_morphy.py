import re
import asyncio
import pymorphy2
from collections import Counter

morph = pymorphy2.MorphAnalyzer()


def collect_morphological_info(lines):
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


async def get_morphological_info(text):
    return await asyncio.to_thread(collect_morphological_info, text.splitlines())


def collect_morphological_info_from_file(file_path: str, encoding: str = "utf-8"):
    with open(file_path, "r", encoding=encoding) as source_file:
        return collect_morphological_info(source_file)


async def get_morphological_info_from_file(file_path: str, encoding: str = "utf-8"):
    return await asyncio.to_thread(collect_morphological_info_from_file, file_path, encoding)