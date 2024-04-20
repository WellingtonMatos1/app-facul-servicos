from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as fornecedor_router
from routes_servico import router as servico_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"], 
)

app.include_router(fornecedor_router)
app.include_router(servico_router)
