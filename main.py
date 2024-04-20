from fastapi import FastAPI
from routes import router as fornecedor_router
from routes_servico import router as servico_router


app = FastAPI()

app.include_router(fornecedor_router)
app.include_router(servico_router)
