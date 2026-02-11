from fastapi import FastAPI
from pydantic import BaseModel  
from typing import List

app = FastAPI(
    title = "Clinica API"
)

class doctor(BaseModel):
    doctorId: int
    name: str
    specialty: str

doctores_db: list[doctor] = []

@app.post("/doctores/", response_model=doctor)
def crear_doctor(doctor: doctor):
    doctores_db.append(doctor)
    return doctor
@app.get("/doctores/", response_model=List[doctor])
def listar_doctores():
    return doctores_db
@app.get("/doctores/{doctor_id}", tags=["Doctores"])
def obtener_doctor(doctor_id: int):
    for d in doctores_db:
        if d.doctorId == doctor_id:
            return d
    return {"error": "Doctor no encontrado"}
@app.delete("/doctores/{doctor_id}", tags=["Doctores"])
def eliminar_doctor(doctor_id: int):    
    for i, d in enumerate(doctores_db):
        if d.doctorId == doctor_id:
            del doctores_db[i]
            return {"message": "Doctor eliminado"}
    return {"error": "Doctor no encontrado"}
