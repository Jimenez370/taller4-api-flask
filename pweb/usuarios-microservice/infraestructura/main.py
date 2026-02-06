import uvicorn
from infraestructura.adapters.database import init_db

if __name__ == "__main__":
    init_db()

    uvicorn.run(
        "infraestructura.api.usuario_controller:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
