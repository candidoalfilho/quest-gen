"""Helper utilities to ajustar parâmetros de questões pré-existentes."""

from typing import Any, Dict, Optional

from get_questions import generate_template, transform_placeholders


def _render_template(text: str, placeholder_values: Dict[str, str]) -> str:
    """Substitui placeholders pelo valor informado sem usar str.format."""

    rendered = text
    for placeholder, value in placeholder_values.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def generate_modified_question(
    *,
    year: int,
    index: int,
    include_original: bool = False,
    scale_factor: Optional[float] = None,
    overrides: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Gera um template parametrizado e aplica ajustes nos placeholders.

    Args:
        year: Ano da prova no banco ENEM.
        index: Índice da questão (base 1).
        include_original: Retorna enunciado original para referência.
        scale_factor: Multiplicador aplicado aos números encontrados.
        overrides: Mapeamento de placeholders para valores específicos.

    Returns:
        Estrutura com template, placeholders ajustados e versões renderizadas.
    """

    payload = generate_template(year=year, index=index, include_original=include_original)

    base_placeholders: Dict[str, str] = payload.get("placeholders", {})
    adjusted_placeholders = dict(base_placeholders)

    if scale_factor is not None:
        adjusted_placeholders.update(transform_placeholders(base_placeholders, scale_factor))

    if overrides:
        adjusted_placeholders.update(overrides)

    rendered_context = _render_template(
        payload.get("context_template", ""), adjusted_placeholders
    )
    rendered_intro = _render_template(
        payload.get("alternatives_introduction_template", ""), adjusted_placeholders
    )

    response: Dict[str, Any] = {
        "title": payload.get("title"),
        "context_template": payload.get("context_template", ""),
        "alternatives_introduction_template": payload.get(
            "alternatives_introduction_template", ""
        ),
        "alternatives": payload.get("alternatives", []),
        "correct_alternative": payload.get("correct_alternative"),
        "placeholders": adjusted_placeholders,
        "rendered": {
            "context": rendered_context,
            "alternatives_introduction": rendered_intro,
        },
    }

    if include_original and "original_question" in payload:
        response["original_question"] = payload["original_question"]

    return response
