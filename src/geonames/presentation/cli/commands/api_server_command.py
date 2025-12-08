import uvicorn
import typer

api_server_cli = typer.Typer()

@api_server_cli.command("start")
def start(
    host: str = typer.Option("127.0.0.1", help="Host for the API server"),
    port: int = typer.Option(8080, help="Port for the API server"),
    reload: bool = typer.Option(True, help="Enable auto-reload"),
):
    
    print(f"Starting API server on http://{host}:{port}")

    uvicorn.run(
        "geonames.presentation.api.main:app",
        host=host,
        port=port,
        reload=reload,
    )

