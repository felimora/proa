from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Ranking en memoria 
leaderboard = []

class ScoreData(BaseModel):
    nombre: str
    puntaje: int

@app.post("/api/score")
def save_score(data: ScoreData):
    leaderboard.append({"nombre": data.nombre, "puntaje": data.puntaje})
    # Ordenar de mayor a menor y guardar solo el Top 10
    leaderboard.sort(key=lambda x: x["puntaje"], reverse=True)
    leaderboard[:] = leaderboard[:10]
    return {"top10": leaderboard}

@app.get("/api/leaderboard")
def get_leaderboard():
    return {"top10": leaderboard}

@app.get("/")
def read_root():
    # Sirve el juego directamente en la ruta principal
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())
