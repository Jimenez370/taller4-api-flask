Comando para ejecutar microservicios de Pacienetes es
cd Clinica/Pacientes
uvicorn main:app --reload --port 8001
http://127.0.0.1:8001/docs

Comando para ejecutar microservicios de Doctores es
cd Clinica/Doctores
uvicorn main:app --reload --port 8002
http://127.0.0.1:8002/docs