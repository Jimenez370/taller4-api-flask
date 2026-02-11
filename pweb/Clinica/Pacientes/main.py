from fastapi import FastAPI
from pydantic import BaseModel  
from typing import List

app = FastAPI(
    title = "Clinica API"
)

class Paciente(BaseModel):
    pacienteId: int
    name: str
    Email: str

pacientes_db: list[Paciente] = []

@app.post("/pacientes/", response_model=Paciente)
def crear_paciente(paciente: Paciente):
    pacientes_db.append(paciente)
    return paciente
@app.get("/pacientes/", response_model=List[Paciente])
def listar_pacientes():
    return pacientes_db
@app.get("/pacientes/{paciente_id}", tags=["Pacientes"])
def obtener_paciente(paciente_id: int):
    for p in pacientes_db:
        if p.pacienteId == paciente_id:
            return p
    return {"error": "Paciente no encontrado"}

@app.delete("/pacientes/{paciente_id}", tags=["Pacientes"])
def eliminar_paciente(paciente_id: int):    
    for i, p in enumerate(pacientes_db):
        if p.pacienteId == paciente_id:
            del pacientes_db[i]
            return {"message": "Paciente eliminado"}
    return {"error": "Paciente no encontrado"}
