from fastapi import APIRouter

healthcheck_router = APIRouter()

@healthcheck_router.get("/health/")
def healthcheck():
    return {'status': 'ok'}