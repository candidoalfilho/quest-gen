"""
QuestGen Backend - Rotas da API
Endpoints para geração de questões
"""

from fastapi import APIRouter, HTTPException
from generator import QuestGenerator
from modify import generate_modified_question
from schemas import (
    QuestRequest,
    QuestResponse,
    TemplateModifierRequest,
    TemplateModifierResponse,
)

router = APIRouter()

# Instância global do gerador
quest_generator = QuestGenerator()

@router.post("/generate", response_model=QuestResponse)
async def generate_questions(request: QuestRequest):
    """
    Gera questões baseadas no conteúdo fornecido

    Args:
        request: Dados da requisição contendo conteúdo e parâmetros

    Returns:
        Lista de questões geradas
    """
    try:
        questions = await quest_generator.generate_questions(
            content=request.content,
            num_questions=request.num_questions,
            difficulty=request.difficulty,
            question_type=request.question_type,
            language=request.language,
            source=request.source,
            subject=request.subject
        )
        
        return QuestResponse(
            questions=questions,
            total_generated=len(questions),
            success=True
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar questões: {str(e)}"
        )

@router.get("/modify", response_model=TemplateModifierResponse)
async def modify_existing_question(request: TemplateModifierRequest):
    """Gera um template de questão existente aplicando ajustes nos parâmetros."""

    try:
        payload = generate_modified_question(
            year=request.year,
            index=request.index,
            include_original=request.include_original,
            scale_factor=request.scale_factor,
            overrides=request.placeholders,
        )
        return TemplateModifierResponse(**payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/types")
async def get_question_types():
    """Retorna os tipos de questão disponíveis"""
    return {
        "types": [
            "multiple_choice",
            "true_false", 
            "open_ended",
            "fill_blank",
            "matching"
        ]
    }

@router.get("/difficulties")
async def get_difficulties():
    """Retorna os níveis de dificuldade disponíveis"""
    return {
        "difficulties": [
            "easy",
            "medium",
            "hard"
        ]
    }

@router.get("/sources")
async def get_math_sources():
    """Retorna as origens/vestibulares disponíveis para questões de matemática"""
    return {
        "sources": [
            {"value": "enem", "label": "ENEM", "description": "Questões no estilo do Exame Nacional do Ensino Médio"},
            {"value": "fuvest", "label": "FUVEST", "description": "Questões da Fundação Universitária para o Vestibular (USP)"},
            {"value": "unicamp", "label": "UNICAMP", "description": "Questões da Universidade Estadual de Campinas"},
            {"value": "ufrj", "label": "UFRJ", "description": "Questões da Universidade Federal do Rio de Janeiro"},
            {"value": "ufmg", "label": "UFMG", "description": "Questões da Universidade Federal de Minas Gerais"},
            {"value": "unesp", "label": "UNESP", "description": "Questões da Universidade Estadual Paulista"},
            {"value": "ufsc", "label": "UFSC", "description": "Questões da Universidade Federal de Santa Catarina"},
            {"value": "ufrgs", "label": "UFRGS", "description": "Questões da Universidade Federal do Rio Grande do Sul"},
            {"value": "unifesp", "label": "UNIFESP", "description": "Questões da Universidade Federal de São Paulo"},
            {"value": "ime", "label": "IME", "description": "Questões do Instituto Militar de Engenharia"},
            {"value": "ita", "label": "ITA", "description": "Questões do Instituto Tecnológico de Aeronáutica"},
            {"value": "personalizado", "label": "Personalizado", "description": "Questões personalizadas para necessidades específicas"},
            {"value": "generico", "label": "Genérico", "description": "Questões de matemática genéricas"}
        ]
    }
