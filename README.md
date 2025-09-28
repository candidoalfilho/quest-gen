# QuestGen Backend

Sistema de geração de questões usando FastAPI, LangChain e Google Gemini.

## Funcionalidades

- Geração automática de questões baseadas em conteúdo
- Múltiplos tipos de questão (múltipla escolha, verdadeiro/falso, abertas, etc.)
- Diferentes níveis de dificuldade
- Suporte a múltiplos idiomas
- **Especialização em Matemática**: Templates específicos para diferentes vestibulares
- Geração de questões no estilo ENEM, FUVEST, UNICAMP e outros
- API RESTful com documentação automática

## Estrutura do Projeto

```
back/
├── __init__.py          # Pacote Python
├── main.py              # Entrypoint FastAPI
├── routes.py            # Endpoints da API
├── generator.py         # Lógica LangChain
├── schemas.py           # Modelos Pydantic
├── requirements.txt     # Dependências
└── README.md           # Este arquivo
```

## Instalação

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Configurar variáveis de ambiente:
```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar o arquivo .env com suas credenciais
nano .env  # ou use seu editor preferido
```

   Para obter a chave da API do Google Gemini:
   - Acesse: https://makersuite.google.com/app/apikey
   - Faça login com sua conta Google
   - Clique em "Create API Key"
   - Copie a chave gerada
   - Cole no arquivo `.env` na variável `GOOGLE_API_KEY`

### Variáveis de Ambiente Disponíveis

| Variável | Descrição | Padrão |
|----------|-----------|---------|
| `GOOGLE_API_KEY` | Chave da API do Google Gemini | **Obrigatório** |
| `HOST` | Host do servidor | `0.0.0.0` |
| `PORT` | Porta do servidor | `8000` |
| `DEBUG` | Modo debug | `False` |
| `GEMINI_MODEL` | Modelo do Gemini | `gemini-pro` |
| `GEMINI_TEMPERATURE` | Temperatura do modelo | `0.7` |
| `GEMINI_MAX_TOKENS` | Máximo de tokens | `1000` |
| `ALLOWED_ORIGINS` | Origens permitidas CORS | `*` (todas) |
| `LOG_LEVEL` | Nível de log | `INFO` |

3. Executar o servidor:
```bash
python main.py
```

## Uso da API

### Gerar Questões

**POST** `/api/generate`

```json
{
  "content": "Conteúdo base para gerar questões...",
  "num_questions": 5,
  "difficulty": "medium",
  "question_type": "multiple_choice",
  "language": "português",
  "source": "enem",
  "subject": "matematica"
}
```

### Gerar Questões de Matemática por Vestibular

**POST** `/api/generate`

```json
{
  "content": "Funções quadráticas: uma função quadrática f(x) = ax² + bx + c...",
  "num_questions": 3,
  "difficulty": "hard",
  "question_type": "multiple_choice",
  "language": "português",
  "source": "fuvest",
  "subject": "matematica"
}
```

### Verificar Saúde

**GET** `/health`

### Tipos de Questão Disponíveis

**GET** `/api/types`

### Níveis de Dificuldade

**GET** `/api/difficulties`

### Origens/Vestibulares para Matemática

**GET** `/api/sources`

Retorna todas as origens/vestibulares disponíveis para geração de questões de matemática:

- **ENEM**: Exame Nacional do Ensino Médio
- **FUVEST**: Fundação Universitária para o Vestibular (USP)
- **UNICAMP**: Universidade Estadual de Campinas
- **UFRJ**: Universidade Federal do Rio de Janeiro
- **UFMG**: Universidade Federal de Minas Gerais
- **UNESP**: Universidade Estadual Paulista
- **UFSC**: Universidade Federal de Santa Catarina
- **UFRGS**: Universidade Federal do Rio Grande do Sul
- **UNIFESP**: Universidade Federal de São Paulo
- **IME**: Instituto Militar de Engenharia
- **ITA**: Instituto Tecnológico de Aeronáutica
- **Personalizado**: Questões personalizadas
- **Genérico**: Questões de matemática genéricas

## Funcionalidades Especiais para Matemática

### Templates por Vestibular

O sistema inclui templates específicos para diferentes vestibulares brasileiros:

#### ENEM
- Questões contextualizadas com situações do dia a dia
- Abordagem de competências e habilidades
- 5 opções de resposta (A, B, C, D, E)
- Ênfase em interpretação e resolução de problemas reais

#### FUVEST (USP)
- Questões mais teóricas e conceituais
- Ênfase em demonstrações e raciocínio lógico
- 5 opções de resposta (A, B, C, D, E)
- Abordagem mais formal e matemática pura

#### UNICAMP
- Questões criativas e inovadoras
- Ênfase em raciocínio lógico e pensamento matemático
- 5 opções de resposta (A, B, C, D, E)
- Abordagem interdisciplinar e não convencional

#### Outros Vestibulares
Cada vestibular tem seu próprio template personalizado com características específicas do estilo de questões.

## Documentação

Acesse `/docs` para documentação interativa da API (Swagger UI).

## Desenvolvimento

Para executar em modo de desenvolvimento:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testes

```bash
pytest
```
