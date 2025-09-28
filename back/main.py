from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from uuid import uuid4

from routes.question_generation_route import question_generation_router
from routes.healthcheck_route import healthcheck_router

app = FastAPI(
    title="API de geração de questões para simulados de vestibulares e concursos",
    summary="A API tem por objetivo facilitar geração de questões para simulados de vestibulares e concursos, usando-se de IA generativa para construir questões didáticas, complexas e nos mesmos moldes dos maiores vestibulares do Brasil.",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_request_id_middleware(request: Request, call_next):
    try:
        request_id = str(uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise e

app.include_router(question_generation_router, prefix="/api", tags=["Question Generation"])
app.include_router(healthcheck_router, prefix="/api", tags=["Healthcheck"])