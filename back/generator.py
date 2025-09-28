"""
QuestGen Backend - Gerador de Questões
Lógica principal usando LangChain com Google Gemini para gerar questões
"""

import os
from typing import List, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from schemas import QuestItem, MathSource

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class QuestGenerator:
    """Classe responsável por gerar questões usando LangChain"""
    
    def __init__(self):
        """Inicializa o gerador com configurações do LangChain e Google Gemini"""
        # Configurar API key do Google Gemini
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente. Verifique o arquivo .env")
        
        # Configurações do Gemini a partir do .env
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("GEMINI_MAX_TOKENS", "1000"))
        
        # Inicializar LLM do Gemini
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=self.api_key,
            model=self.model,
            temperature=self.temperature,
            max_output_tokens=self.max_tokens
        )
        
        # Templates específicos para matemática por vestibular
        self.math_templates = {
            MathSource.ENEM: """
            Você é um especialista em questões de matemática do ENEM. Baseado no conteúdo fornecido,
            gere {num_questions} questões de {question_type} com dificuldade {difficulty} em {language}.

            ESTILO ENEM - MATEMÁTICA:
            - Questões contextualizadas com situações do dia a dia
            - Abordagem de competências e habilidades
            - Integração com outras áreas do conhecimento quando relevante
            - Ênfase em interpretação e resolução de problemas reais
            - Cálculos que envolvam números reais e situações práticas

            CONTEÚDO BASE:
            {content}

            FORMATO DE RESPOSTA (JSON):
            {{
                "questions": [
                    {{
                        "question": "Texto da pergunta aqui",
                        "options": ["Opção A", "Opção B", "Opção C", "Opção D", "Opção E"],
                        "correct_answer": "Opção A",
                        "explanation": "Explicação detalhada da resposta correta",
                        "difficulty": "{difficulty}",
                        "type": "{question_type}",
                        "source": "enem",
                        "subject": "matematica"
                    }}
                ]
            }}

            REGRAS ESPECÍFICAS ENEM:
            - Para múltipla escolha: sempre 5 opções (A, B, C, D, E)
            - Questões devem ter contexto real ou interdisciplinar
            - Foque em: Álgebra, Geometria, Estatística, Probabilidade, Análise Combinatória
            - Use linguagem acessível mas academicamente rigorosa
            """,

            MathSource.FUVEST: """
            Você é um especialista em questões de matemática da FUVEST (USP). Baseado no conteúdo fornecido,
            gere {num_questions} questões de {question_type} com dificuldade {difficulty} em {language}.

            ESTILO FUVEST - MATEMÁTICA:
            - Questões mais teóricas e conceituais
            - Ênfase em demonstrações e raciocínio lógico
            - Abordagem mais formal e matemática pura
            - Questões que exigem conhecimento sólido de conceitos
            - Menos contextualização, mais matemática abstrata

            CONTEÚDO BASE:
            {content}

            FORMATO DE RESPOSTA (JSON):
            {{
                "questions": [
                    {{
                        "question": "Texto da pergunta aqui",
                        "options": ["Opção A", "Opção B", "Opção C", "Opção D", "Opção E"],
                        "correct_answer": "Opção A",
                        "explanation": "Explicação detalhada da resposta correta",
                        "difficulty": "{difficulty}",
                        "type": "{question_type}",
                        "source": "fuvest",
                        "subject": "matematica"
                    }}
                ]
            }}

            REGRAS ESPECÍFICAS FUVEST:
            - Para múltipla escolha: sempre 5 opções (A, B, C, D, E)
            - Questões mais analíticas e menos práticas
            - Foque em: Cálculo, Álgebra Linear, Geometria Analítica
            - Use linguagem matemática formal
            """,

            MathSource.UNICAMP: """
            Você é um especialista em questões de matemática da UNICAMP. Baseado no conteúdo fornecido,
            gere {num_questions} questões de {question_type} com dificuldade {difficulty} em {language}.

            ESTILO UNICAMP - MATEMÁTICA:
            - Questões criativas e inovadoras
            - Ênfase em raciocínio lógico e pensamento matemático
            - Abordagem interdisciplinar
            - Questões que fogem do padrão tradicional
            - Ênfase em compreensão de conceitos

            CONTEÚDO BASE:
            {content}

            FORMATO DE RESPOSTA (JSON):
            {{
                "questions": [
                    {{
                        "question": "Texto da pergunta aqui",
                        "options": ["Opção A", "Opção B", "Opção C", "Opção D", "Opção E"],
                        "correct_answer": "Opção A",
                        "explanation": "Explicação detalhada da resposta correta",
                        "difficulty": "{difficulty}",
                        "type": "{question_type}",
                        "source": "unicamp",
                        "subject": "matematica"
                    }}
                ]
            }}

            REGRAS ESPECÍFICAS UNICAMP:
            - Para múltipla escolha: sempre 5 opções (A, B, C, D, E)
            - Questões originais e não convencionais
            - Foque em: Lógica, Raciocínio, Conceitos Avançados
            - Use abordagem criativa e interdisciplinar
            """,

            MathSource.GENERICO: """
            Você é um especialista em criação de questões de matemática. Baseado no conteúdo fornecido,
            gere {num_questions} questões de {question_type} com dificuldade {difficulty} em {language}.

            CONTEÚDO BASE:
            {content}

            FORMATO DE RESPOSTA (JSON):
            {{
                "questions": [
                    {{
                        "question": "Texto da pergunta aqui",
                        "options": ["Opção A", "Opção B", "Opção C", "Opção D"],
                        "correct_answer": "Opção A",
                        "explanation": "Explicação detalhada da resposta correta",
                        "difficulty": "{difficulty}",
                        "type": "{question_type}",
                        "source": "generico",
                        "subject": "matematica"
                    }}
                ]
            }}

            REGRAS GERAIS:
            - Para múltipla escolha: sempre 4 opções (A, B, C, D)
            - Para verdadeiro/falso: apenas ["Verdadeiro", "Falso"]
            - Para questões abertas: deixe options como array vazio []
            - Sempre forneça explicação clara e educativa
            - Questões devem ser relevantes ao conteúdo fornecido
            - Mantenha o nível de dificuldade {difficulty}
            - Use linguagem clara e objetiva
            """
        }

        # Template padrão para geração de questões otimizado para Gemini
        self.question_template = PromptTemplate(
            input_variables=["content", "num_questions", "difficulty", "question_type", "language", "source"],
            template="""
            Você é um especialista em criação de questões educacionais. Com base no conteúdo fornecido,
            gere exatamente {num_questions} questões do tipo {question_type} com nível de dificuldade {difficulty}
            em {language}.

            CONTEÚDO BASE:
            {content}

            IMPORTANTE: Responda APENAS com o JSON válido, sem texto adicional.

            FORMATO DE RESPOSTA (JSON):
            {{
                "questions": [
                    {{
                        "question": "Texto da pergunta aqui",
                        "options": ["Opção A", "Opção B", "Opção C", "Opção D"],
                        "correct_answer": "Opção A",
                        "explanation": "Explicação detalhada da resposta correta",
                        "difficulty": "{difficulty}",
                        "type": "{question_type}",
                        "source": "{source}",
                        "subject": "matematica"
                    }}
                ]
            }}

            REGRAS OBRIGATÓRIAS:
            - Para múltipla escolha: sempre 4 opções (A, B, C, D)
            - Para verdadeiro/falso: apenas ["Verdadeiro", "Falso"]
            - Para questões abertas: deixe options como array vazio []
            - Sempre forneça explicação clara e educativa
            - Questões devem ser relevantes ao conteúdo fornecido
            - Mantenha o nível de dificuldade {difficulty}
            - Use linguagem clara e objetiva
            """
        )
        
        # Criar chain
        self.question_chain = LLMChain(
            llm=self.llm,
            prompt=self.question_template
        )
    
    async def generate_questions(
        self,
        content: str,
        num_questions: int = 5,
        difficulty: str = "medium",
        question_type: str = "multiple_choice",
        language: str = "português",
        source: str = "generico",
        subject: str = "matematica"
    ) -> List[QuestItem]:
        """
        Gera questões baseadas no conteúdo fornecido

        Args:
            content: Conteúdo base para gerar questões
            num_questions: Número de questões a gerar
            difficulty: Nível de dificuldade (easy, medium, hard)
            question_type: Tipo de questão
            language: Idioma das questões
            source: Origem/vestibular da questão (para matemática)
            subject: Matéria/disciplina da questão

        Returns:
            Lista de questões geradas
        """
        try:
            # Verificar se é matemática para usar template específico
            if subject.lower() == "matematica":
                # Usar template específico para matemática
                math_template = self.math_templates.get(source, self.math_templates[MathSource.GENERICO])

                # Criar prompt personalizado para matemática
                from langchain.prompts import PromptTemplate

                math_prompt = PromptTemplate(
                    input_variables=["content", "num_questions", "difficulty", "question_type", "language"],
                    template=math_template
                )

                # Criar chain temporária para matemática
                math_chain = LLMChain(llm=self.llm, prompt=math_prompt)

                # Executar chain para matemática
                result = await math_chain.arun(
                    content=content,
                    num_questions=num_questions,
                    difficulty=difficulty,
                    question_type=question_type,
                    language=language
                )
            else:
                # Usar template padrão para outras matérias
                result = await self.question_chain.arun(
                    content=content,
                    num_questions=num_questions,
                    difficulty=difficulty,
                    question_type=question_type,
                    language=language,
                    source=source
                )
            
            # Parsear resultado JSON
            import json
            parsed_result = json.loads(result)
            
            # Converter para QuestItem
            questions = []
            for q in parsed_result.get("questions", []):
                quest_item = QuestItem(
                    question=q.get("question", ""),
                    options=q.get("options", []),
                    correct_answer=q.get("correct_answer", ""),
                    explanation=q.get("explanation", ""),
                    difficulty=q.get("difficulty", difficulty),
                    type=q.get("type", question_type)
                )
                questions.append(quest_item)
            
            return questions
            
        except json.JSONDecodeError:
            # Fallback: gerar questão simples se JSON falhar
            return self._generate_fallback_question(content, difficulty, question_type, source, subject)
        
        except Exception as e:
            raise Exception(f"Erro na geração de questões: {str(e)}")
    
    def _generate_fallback_question(
        self,
        content: str,
        difficulty: str,
        question_type: str,
        source: str = "generico",
        subject: str = "matematica"
    ) -> List[QuestItem]:
        """Gera uma questão simples como fallback"""
        return [
            QuestItem(
                question=f"Com base no conteúdo fornecido, qual é a informação principal?",
                options=["Opção A", "Opção B", "Opção C", "Opção D"] if question_type == "multiple_choice" else [],
                correct_answer="Opção A",
                explanation="Esta é uma questão gerada automaticamente como fallback.",
                difficulty=difficulty,
                type=question_type,
                source=source,
                subject=subject
            )
        ]
