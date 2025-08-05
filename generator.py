# generate.py

import os
from pathlib import Path
import typer
from jinja2 import Environment, FileSystemLoader

app = typer.Typer()

BASE_DIR = Path(__file__).parent
TEMPLATE_DIR = BASE_DIR / "templates"

env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))


def render_template(template_name: str, **kwargs) -> str:
    template = env.get_template(template_name)
    return template.render(**kwargs)


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"✔️  Created {path}")


def snake_to_pascal(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_"))


@app.command()
def resource(name: str):
    model_name = snake_to_pascal(name)
    lower_name = name.lower()

    write_file(
        BASE_DIR / f"app/models/{lower_name}.py",
        render_template("model.py.jinja", model_name=model_name, lower_name=lower_name),
    )

    write_file(
        BASE_DIR / f"app/api/routes/{lower_name}.py",
        render_template("route.py.jinja", model_name=model_name, lower_name=lower_name),
    )

    write_file(
        BASE_DIR / f"tests/test_{lower_name}.py",
        render_template("test.py.jinja", model_name=model_name, lower_name=lower_name),
    )


if __name__ == "__main__":
    app()
