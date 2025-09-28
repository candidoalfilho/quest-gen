from typing import List, Optional
from pydantic import BaseModel

from models.enums import DisciplinesEnum, ExamsEnum

class QuestionAlternative(BaseModel):
    statement:  str
    is_correct: bool
    explanation: str

class QuestionCreate(BaseModel):
    input: str
    discipline: DisciplinesEnum
    topic: str
    question_count: int = 1  # Valor padrão para compatibilidade

class QuestionLLMResponse(BaseModel):
    exam: ExamsEnum
    discipline: DisciplinesEnum
    topic: str
    statement: str
    source: Optional[str]
    alternatives: List[QuestionAlternative]

class Question:
    input: str
    question: QuestionLLMResponse