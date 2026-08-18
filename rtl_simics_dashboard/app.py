import json
import os
import re
from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    abort,
)

app = Flask(__name__)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def slugify(name):
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_components():
    components = []

    for component_dir in sorted(DATA_DIR.iterdir()):
        if not component_dir.is_dir():
            continue

        metadata = load_json(component_dir / "metadata.json")
        comparison = load_json(component_dir / "comparison_analysis.json")

        components.append(
            {
                "id": component_dir.name,
                "name": metadata.get(
                    "name",
                    component_dir.name,
                ),
                "comparison": comparison,
            }
        )

    return components


@app.route("/")
def index():
    components = get_components()

    return render_template(
        "index.html",
        components=components,
    )


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")

    component_name = request.form.get("component_name", "").strip()

    if not component_name:
        return "Component name is required", 400

    component_id = slugify(component_name)

    if not component_id:
        return "Invalid component name", 400

    component_dir = DATA_DIR / component_id
    component_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        "name": component_name,
        "id": component_id,
    }

    with open(component_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    uploads = {
        "rtl_file": "rtl_analysis.json",
        "simics_file": "simics_analysis.json",
        "comparison_file": "comparison_analysis.json",
    }

    for form_name, output_name in uploads.items():

        uploaded_file = request.files.get(form_name)

        if uploaded_file and uploaded_file.filename:

            try:
                content = json.load(uploaded_file)
            except json.JSONDecodeError:
                return (
                    f"{uploaded_file.filename} "
                    "is not a valid JSON file",
                    400,
                )

            with open(component_dir / output_name, "w") as f:
                json.dump(content, f, indent=2)

    return redirect(
        url_for(
            "component_dashboard",
            component_id=component_id,
        )
    )


@app.route("/component/<component_id>")
def component_dashboard(component_id):

    component_dir = DATA_DIR / component_id

    if not component_dir.exists():
        abort(404)

    metadata = load_json(
        component_dir / "metadata.json"
    )

    rtl = load_json(
        component_dir / "rtl_analysis.json"
    )

    simics = load_json(
        component_dir / "simics_analysis.json"
    )

    comparison = load_json(
        component_dir / "comparison_analysis.json"
    )

    return render_template(
        "component.html",
        metadata=metadata,
        rtl=rtl,
        simics=simics,
        comparison=comparison,
        component_id=component_id,
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
