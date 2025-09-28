from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from schemas.questions_schemas import QuestionCreate, QuestionLLMResponse
from repositories.questions_repository import create_questions
from services.LLMs.gemini.gemini_service import GeminiLLM

question_generation_router = APIRouter()

# Instância do serviço Gemini será criada quando necessária
gemini_service = None

def get_gemini_service():
    """
    Cria uma instância do serviço Gemini se não existir
    """
    global gemini_service
    if gemini_service is None:
        gemini_service = GeminiLLM()
    return gemini_service

@question_generation_router.post("/generate/")
async def generate_questions(question: QuestionCreate) -> List[QuestionLLMResponse]:
    """
    Gera uma questão baseada no input fornecido
    """
    try:
        query = f"{question.input}\nDisciplina: {question.discipline}\nTópico: {question.topic}"

        return create_questions(user_query=query, question_count=question.question_count)
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Houve um erro na geração de questões. Erro: {e}')
