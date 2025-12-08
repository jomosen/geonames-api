import typer

from geonames.presentation.cli.commands.api_server_command import api_server_cli
from geonames.presentation.cli.commands.geonames_command import geonames_import_cli

app = typer.Typer()

app.add_typer(api_server_cli, name="api")
app.add_typer(geonames_import_cli, name="geonames")


def main():
    app()

if __name__ == "__main__":
    main()