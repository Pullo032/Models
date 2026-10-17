import csv
import glob
import json
import re
import sys
from collections import Counter
from pathlib import Path

BASE = Path(__file__).parent
TONES = {"Professionnel", "Chaleureux", "Neutre", "Amical", "Persuasif", "Enthousiaste"}
STYLES = {"Concis", "Détaillé", "Commercial", "Informatif", "Descriptif"}
COLUMNS = ["input_text", "tone", "style", "target_text"]
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF]")
NUM_RE = re.compile(r"\d+(?:[.,]\d+)?")

rows, errors = [], []
for path in sorted(glob.glob(str(BASE / "batch_*.jsonl"))):
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"{Path(path).name}:{lineno} JSON invalide ({e})")
                continue
            if set(obj) != set(COLUMNS):
                errors.append(f"{Path(path).name}:{lineno} clés inattendues {sorted(obj)}")
                continue
            if any(not isinstance(obj[c], str) or not obj[c].strip() for c in COLUMNS):
                errors.append(f"{Path(path).name}:{lineno} valeur vide ou non textuelle")
                continue
            if obj["tone"] not in TONES:
                errors.append(f"{Path(path).name}:{lineno} tone invalide '{obj['tone']}'")
                continue
            if obj["style"] not in STYLES:
                errors.append(f"{Path(path).name}:{lineno} style invalide '{obj['style']}'")
                continue
            rows.append({c: obj[c].strip() for c in COLUMNS} | {"_src": f"{Path(path).name}:{lineno}"})

print(f"Lignes lues : {len(rows)}")
for e in errors:
    print("ERREUR", e)

# Contrôles de cohérence
kept, seen_exact = [], set()
issues = Counter()
for r in rows:
    src = r["_src"]
    if r["target_text"] == r["input_text"]:
        issues["target identique à input"] += 1
        errors.append(f"{src} target identique à input")
        continue
    if EMOJI_RE.search(r["target_text"]) or EMOJI_RE.search(r["input_text"]):
        issues["emoji"] += 1
        errors.append(f"{src} emoji détecté")
        continue
    missing = [n for n in NUM_RE.findall(r["input_text"]) if n not in r["target_text"]]
    if missing:
        issues["chiffre absent du target"] += 1
        errors.append(f"{src} chiffres absents du target : {missing}")
        continue
    key = tuple(r[c] for c in COLUMNS)
    if key in seen_exact:
        issues["doublon exact"] += 1
        continue
    seen_exact.add(key)
    kept.append(r)

print(f"Lignes conservées après contrôles : {len(kept)}")
print("Problèmes :", dict(issues) or "aucun")

dup_target = sum(v - 1 for v in Counter(r["target_text"] for r in kept).values() if v > 1)
print(f"target_text dupliqués (même texte) : {dup_target}")
print("Répartition tone :", dict(Counter(r["tone"] for r in kept)))
print("Répartition style :", dict(Counter(r["style"] for r in kept)))
print("Annonces source distinctes :", len({r["input_text"] for r in kept}))

out = BASE.parent / "annonces_reformulation_dataset.csv"
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLUMNS, quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    for r in kept:
        w.writerow({c: r[c] for c in COLUMNS})
print("Écrit :", out)

if errors:
    print("\nDétail des erreurs (premières 30) :")
    for e in errors[:30]:
        print(" -", e)
