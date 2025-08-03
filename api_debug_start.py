from alembic import command
from alembic.config import Config
from api import get_app


app = get_app()

if __name__ == "__main__":
    alembic_config = Config("alembic.ini")
    command.upgrade(alembic_config, "head")
    import uvicorn
    uvicorn.run(
        "api_debug_start:app",
        host="0.0.0.0",
        workers=1,
        port=8081,
        reload=False,
    )