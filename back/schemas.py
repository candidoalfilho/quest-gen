"""
QuestGen Backend - Modelos Pydantic
Schemas para validação de dados da API
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum

class DifficultyLevel(str, Enum):
    """Níveis de dificuldade disponíveis"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuestionType(str, Enum):
    """Tipos de questão disponíveis"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    OPEN_ENDED = "open_ended"
    FILL_BLANK = "fill_blank"
    MATCHING = "matching"

class MathSource(str, Enum):
    """Origens/vestibulares de questões de matemática"""
    ENEM = "enem"
    FUVEST = "fuvest"
    UNICAMP = "unicamp"
    UFRJ = "ufrj"
    UFMG = "ufmg"
    UNESP = "unesp"
    UFSC = "ufsc"
    UFRGS = "ufrgs"
    UNIFESP = "unifesp"
    IME = "ime"
    ITA = "ita"
    PERSONALIZADO = "personalizado"
    GENERICO = "generico"

class QuestItem(BaseModel):
    """Modelo para uma questão individual"""
    question: str = Field(..., description="Texto da questão")
    options: List[str] = Field(default=[], description="Opções de resposta (para múltipla escolha)")
    correct_answer: str = Field(..., description="Resposta correta")
    explanation: str = Field(..., description="Explicação da resposta")
    difficulty: str = Field(..., description="Nível de dificuldade")
    type: str = Field(..., description="Tipo da questão")
    source: Optional[MathSource] = Field(default=MathSource.GENERICO, description="Origem/vestibular da questão")
    subject: str = Field(default="matematica", description="Matéria/disciplina da questão")
    
    @validator('question')
    def question_must_not_be_empty(cls, v):
        if not v or len(v.strip()) < 10:
            raise ValueError('Questão deve ter pelo menos 10 caracteres')
        return v
    
    @validator('correct_answer')
    def correct_answer_must_not_be_empty(cls, v):
        if not v or len(v.strip()) < 1:
            raise ValueError('Resposta correta não pode estar vazia')
        return v

class QuestRequest(BaseModel):
    """Modelo para requisição de geração de questões"""
    content: str = Field(..., description="Conteúdo base para gerar questões", min_length=50)
    num_questions: int = Field(default=5, description="Número de questões a gerar", ge=1, le=20)
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM, description="Nível de dificuldade")
    question_type: QuestionType = Field(default=QuestionType.MULTIPLE_CHOICE, description="Tipo de questão")
    language: str = Field(default="português", description="Idioma das questões")
    source: MathSource = Field(default=MathSource.GENERICO, description="Origem/vestibular da questão")
    subject: str = Field(default="matematica", description="Matéria/disciplina da questão")
    
    @validator('content')
    def content_must_be_sufficient(cls, v):
        if len(v.strip()) < 50:
            raise ValueError('Conteúdo deve ter pelo menos 50 caracteres para gerar questões adequadas')
        return v.strip()

class QuestResponse(BaseModel):
    """Modelo para resposta da geração de questões"""
    questions: List[QuestItem] = Field(..., description="Lista de questões geradas")
    total_generated: int = Field(..., description="Total de questões geradas")
    success: bool = Field(..., description="Indica se a geração foi bem-sucedida")
    message: Optional[str] = Field(None, description="Mensagem adicional sobre o resultado")

class HealthResponse(BaseModel):
    """Modelo para resposta de verificação de saúde"""
    status: str = Field(..., description="Status do serviço")
    service: str = Field(..., description="Nome do serviço")
    timestamp: Optional[str] = Field(None, description="Timestamp da verificação")

class ErrorResponse(BaseModel):
    """Modelo para respostas de erro"""
    error: str = Field(..., description="Mensagem de erro")
    detail: Optional[str] = Field(None, description="Detalhes adicionais do erro")
    status_code: int = Field(..., description="Código de status HTTP")
