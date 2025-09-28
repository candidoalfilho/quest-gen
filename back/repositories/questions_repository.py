from services.LLMs.gemini.gemini_service import GeminiLLM
from schemas.questions_schemas import QuestionLLMResponse
from services.LLMs.gemini.prompts import BASE_PROMPT
from typing import List


def create_questions(user_query: str, question_count: int):
    try:
        gemini_model = GeminiLLM()

        question_reponse = gemini_model.generate_response(
            system_prompt=BASE_PROMPT.format(QUESTION_COUNT=question_count),
            user_prompt=user_query,
            response_schema=List[QuestionLLMResponse]
        )

        return question_reponse
    
    except Exception as e:
        raise e