import click
from pathlib import Path

@click.group()
@click.version_option(version="1.0.0", prog_name="La-Split", package_name="lasplit")
def cli():
    """A CLI tool for splitting files."""
    pass



@click.command()
@click.option("--split")
@click.argument("path", type=click.Path(exists=True))
@click.argument("train", type=click.STRING)
@click.argument("valid", type=click.STRING)
@click.argument("test", type=click.STRING)
def split (path, train, valid, test):
    click.echo("split")


cli.add_command(name=split,cmd="--split")

if __name__ == '__main__':
    split()
