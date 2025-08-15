import os
import re
import gensim.downloader as api

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.abspath(os.path.join(CURR_DIR, "../../"))
OUTPUT_FILE = os.path.join(CURR_DIR, "eng-uum.embeddings.tsv")

command = f"cd {PATH} && lt-print -H uum-eng.autobil.bin | hfst-txt2fst | hfst-invert | hfst-expand -c0"
output = os.popen(command).read()

english_words = []

for line in output.strip().split("\n"):
    if ":" in line:
        eng = line.split(":")[0]
        
        word = re.sub(r"<.*?>", "", eng)
        match = re.search(r"<[^>]+>", eng)
        if match:
            first_tag = match.group(0)
            combined = f"{word}{first_tag}"
        else:
            combined = word
        
        combined = combined.strip()
        if combined and len(word) > 1:
            english_words.append(combined)

english_words = list(set(english_words))

print("loading model")

model = api.load('fasttext-wiki-news-subwords-300')

print("loaded model")

threshold = 0.2
topn = 10

def helper(word):
    match = re.match(r"^(.*?)(<.*?>)?$", word)
    if match:
        base = match.group(1)
        tag = " " + match.group(2) if match.group(2) else ""
    else:
        base = word
        tag = ""
    spaced_word = " ".join(base)
    return spaced_word + tag, tag

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for word in english_words:
        base_word = re.sub(r"<.*?>", "", word)
        if base_word not in model.key_to_index:
            continue
        for sim_word, score in model.most_similar(base_word, topn=topn):
            if score < threshold or len(sim_word) <= 1:
                continue
            spaced_word, tag_word = helper(word)
            spaced_candidate, tag_candidate = helper(sim_word)
            if tag_word.strip() == "<num>" or tag_candidate.strip() == "<num>":
                continue

            f.write(f"{spaced_candidate}:{spaced_word}\t{score}\n")