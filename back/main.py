"""
QuestGen Backend - FastAPI Entrypoint
Sistema de geração de questões usando LangChain
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do servidor a partir do .env
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "8000"))
debug = os.getenv("DEBUG", "False").lower() == "true"

# Inicializar aplicação FastAPI
app = FastAPI(
    title="QuestGen API",
    description="API para geração de questões usando LangChain e Google Gemini",
    version="1.0.0",
    debug=debug
)

# Configurar CORS - aceitar todas as origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Aceitar todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(router, prefix="/api")

@app.get("/api")
async def root():
    """Endpoint raiz da API"""
    return {"message": "QuestGen API está funcionando!"}

@app.get("/api/health")
async def health_check():
    """Endpoint de verificação de saúde da API"""
    return {
        "status": "healthy",
        "service": "questgen-backend",
        "version": "1.0.0",
        "features": {
            "math_questions": True,
            "multiple_sources": True,
            "custom_templates": True
        },
        "endpoints": {
            "generate": "/api/generate",
            "types": "/api/types",
            "difficulties": "/api/difficulties",
            "sources": "/api/sources"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=host, port=port)
