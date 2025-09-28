from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from urllib import error, parse, request

API_BASE_DEFAULT = "https://api.enem.dev/v1"
DISCIPLINE_MATH = "matematica"

@dataclass
class Question:
    """Representação mínima da questão utilizada para montar templates."""

    title: str
    context: str
    alternatives_introduction: str
    alternatives: list
    correct_alternative: str

def get_api_base() -> str:
    return os.getenv("ENEM_API_BASE", API_BASE_DEFAULT).rstrip("/")

def http_get_json(url: str, params: Optional[dict] = None, timeout: int = 30) -> dict:
    if params:
        url = f"{url}?{parse.urlencode(params)}"
    req = request.Request(url, headers={"Accept": "application/json"})
    with request.urlopen(req, timeout=timeout) as resp:  # nosec B310
        payload = resp.read().decode("utf-8")
    return json.loads(payload)

def fetch_single_math_question(year: int, index: int, language: Optional[str]) -> Question:
    if index < 1:
        raise ValueError("Question index must be >= 1 (1-based indexing).")

    base = get_api_base()
    params = {"limit": 1, "offset": index, "discipline": DISCIPLINE_MATH}
    if language:
        params["language"] = language

    payload = http_get_json(f"{base}/exams/{year}/questions", params=params, timeout=60)
    questions = payload.get("questions", [])
    if not questions:
        raise RuntimeError(f"Question {index} not found for year {year}.")

    question = questions[0]
    return Question(
        title=question.get("title", ""),
        context=question.get("context", ""),
        alternatives_introduction=question.get("alternativesIntroduction", ""),
        alternatives=question.get("alternatives", []),
        correct_alternative=question.get("correctAlternative", ""),
    )

APPROX_PATTERNS = (
    re.compile(
        r"(\d[\d.,]*)\s+(?:(?:como|uma|um|a|o|por|para|e|é|eh)\s+){0,2}aprox(?:ima[çc][aã]o)?\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"aprox(?:ima[çc][aã]o)?\b(?:\s+(?:para|de|do|da|ao|a))?\s+(\d[\d.,]*)",
        re.IGNORECASE,
    ),
    re.compile(r"(?:≈|∼|~)\s*(\d[\d.,]*)"),
    re.compile(r"(\d[\d.,]*)\s*(?:≈|∼|~)"),
)


def _collect_spans(patterns: tuple[re.Pattern, ...], text: str) -> set[tuple[int, int]]:
    spans: set[tuple[int, int]] = set()
    for pattern in patterns:
        for match in pattern.finditer(text):
            for index, group in enumerate(match.groups(), start=1):
                if group:
                    spans.add((match.start(index), match.end(index)))
    return spans


def _position_in_spans(position: int, spans: set[tuple[int, int]]) -> bool:
    return any(start <= position < end for start, end in spans)


def parameterize_numbers(text: str) -> Tuple[str, Dict[str, str]]:
    """Substitui números por placeholders, ignorando URLs e aproximações fixas."""

    number_pattern = re.compile(r"(\d+[\d.,]*)")
    url_pattern = re.compile(r"https?://\S+")
    url_spans = [(m.start(), m.end()) for m in url_pattern.finditer(text)]
    approx_spans = _collect_spans(APPROX_PATTERNS, text)

    placeholder_map: Dict[str, str] = {}
    placeholder_index = 1
    cursor = 0
    chunks = []

    for match in number_pattern.finditer(text):
        start, end = match.span()
        literal = match.group(0)

        chunks.append(text[cursor:start])

        if _position_in_spans(start, url_spans) or _position_in_spans(start, approx_spans):
            chunks.append(literal)
        else:
            placeholder = f"{{{{n{placeholder_index}}}}}"
            chunks.append(placeholder)
            placeholder_map[placeholder] = literal
            placeholder_index += 1

        cursor = end

    chunks.append(text[cursor:])
    return "".join(chunks), placeholder_map


def scale_numeric_literal(literal: str, factor: float) -> str:
    literal_norm = literal.replace(".", "").replace(",", ".")
    try:
        value = float(literal_norm)
    except ValueError:
        return literal
    scaled = value * factor
    if scaled.is_integer():
        return str(int(scaled))
    return f"{scaled:.2f}".replace(".", ",")


def transform_placeholders(mapping: Dict[str, str], factor: float) -> Dict[str, str]:
    return {slot: scale_numeric_literal(value, factor) for slot, value in mapping.items()}


def build_template_payload(
    question: Question,
    templated_context: str,
    templated_intro: str,
    placeholder_map: Dict[str, str],
    include_original: bool,
) -> dict:
    payload = {
        "title": question.title,
        "context_template": templated_context,
        "alternatives_introduction_template": templated_intro,
        "alternatives": question.alternatives,
        "correct_alternative": question.correct_alternative,
        "placeholders": placeholder_map,
    }
    if include_original:
        payload["original_question"] = {
            "title": question.title,
            "context": question.context,
            "alternativesIntroduction": question.alternatives_introduction,
            "alternatives": question.alternatives,
            "correctAlternative": question.correct_alternative,
        }
    return payload

def generate_template(
    year: int,
    index: int,
    include_original: bool = False,
) -> dict:
    """Return the template payload for a single ENEM math question.

    Args:
        year: Ano da prova ENEM.
        index: Índice da questão (1-based) dentro da disciplina Matemática.
        limit: Limite de questões a buscar (padrão: None, que busca apenas a questão especificada, maximo 50).
        include_original: Se True, inclui enunciado e alternativas originais no payload final para referência.

    Returns:
        Um dicionário com templates, placeholders e alternativas.

    Raises:
        RuntimeError: Quando há falha em buscar a questão ou gravar o arquivo.
    """

    try:
        question = fetch_single_math_question(year, index, language="ingles")
    except (error.URLError, json.JSONDecodeError, RuntimeError, ValueError) as exc:
        raise RuntimeError(f"Failed to fetch question {index} ({year}): {exc}") from exc

    context_template, context_numbers = parameterize_numbers(question.context or "")
    intro_template, intro_numbers = parameterize_numbers(
        question.alternatives_introduction or ""
    )
    placeholder_map = {**context_numbers, **intro_numbers}

    payload = build_template_payload(
        question=question,
        templated_context=context_template,
        templated_intro=intro_template,
        placeholder_map=placeholder_map,
        include_original=include_original,
    )

    # print(json.dumps(payload, ensure_ascii=False, indent=2))
    return payload

# if __name__ == "__main__":
#     generate_template(year=2023, index=136, include_original=False)
