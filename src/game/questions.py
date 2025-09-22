"""Gerenciamento de banco de perguntas.

Gera pools de 100 perguntas por tema (math, logic, python) se não existirem e fornece loaders.
Formato simples para permitir testes e prototype.
"""
import json
from pathlib import Path
from typing import List, Dict

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)

THEMES = ["math", "logic", "python"]


def _ensure_pool(theme: str, total: int = 100):
    path = DATA_DIR / f"questions_{theme}.json"
    if path.exists():
        return
    pool = []
    for i in range(1, total + 1):
        if theme == "math":
            q = f"Quanto é {i} + {i}?"
            a = str(i + i)
            expl = f"Soma básica: {i}+{i}"
            difficulty = 1 + (i - 1) * 4 // (total - 1)  # espalha dificuldade 1..5
        elif theme == "logic":
            q = f"Se A implica B e B implica C, então A implica C? (sim/não) [{i}]"
            a = "sim"
            expl = "Transitividade lógica"
            difficulty = 1 + (i - 1) * 4 // (total - 1)
        else:  # python
            q = f"Qual expressão Python resulta em {i}: ' {i} ' ? (responda com {i})"
            a = str(i)
            expl = "Conversão simples/string"
            difficulty = 1 + (i - 1) * 4 // (total - 1)
        pool.append({"id": i, "question": q, "answer": a, "explanation": expl, "difficulty": difficulty})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pool, f, ensure_ascii=False, indent=2)


def load_questions(theme: str) -> List[Dict]:
    theme = theme.lower()
    if theme not in THEMES:
        raise ValueError("Tema desconhecido: %s" % theme)
    _ensure_pool(theme)
    path = DATA_DIR / f"questions_{theme}.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sample_questions(theme: str, rng, count: int = 3, min_difficulty: int = 1):
    pool = [q for q in load_questions(theme) if q.get("difficulty", 1) >= min_difficulty]
    if not pool:
        return []
    rng.shuffle(pool)
    selected = pool[:count]
    # construir choices (três opções) preservando 'answer'
    out = []
    for q in selected:
        correct = str(q.get("answer"))
        choices = [correct]
        # gerar dois distractors simples dependendo do tema
        if theme == "math":
            try:
                val = int(correct)
            except Exception:
                val = None
            if val is not None:
                # +/- small offsets
                d1 = str(val + rng.randint(1, 5))
                d2 = str(max(0, val - rng.randint(1, 5)))
            else:
                d1 = correct + "?"
                d2 = "0"
            choices.extend([d1, d2])
        elif theme == "logic":
            # corret answer is usually 'sim' or 'não'
            alt = "não" if correct.strip().lower() == "sim" else "sim"
            choices.extend([alt, "talvez"])
        else:  # python
            try:
                val = int(correct)
                choices.extend([str(val + rng.randint(1, 3)), str(max(0, val - rng.randint(1, 3)))])
            except Exception:
                choices.extend([correct + " ", "None"])
        # shuffle choices but remember which is correct
        rng.shuffle(choices)
        q2 = q.copy()
        q2["choices"] = choices
        out.append(q2)
    return out
