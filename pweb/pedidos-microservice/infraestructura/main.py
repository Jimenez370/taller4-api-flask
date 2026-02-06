import uvicorn
from infraestructura.api.pedido_controller import app
from infraestructura.adapters.database import init_db

if __name__ == "__main__":
    # Inicializar la base de datos
    init_db()
    
    # Ejecutar la aplicación
    uvicorn.run(
        "infraestructura.api.pedido_controller:app",
        host="0.0.0.0",
        port=8002,
        reload=True
    )