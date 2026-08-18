from flask import (
    Flask,
    request,
    render_template_string,
    redirect,
    url_for
)
from markupsafe import escape
from pathlib import Path
from datetime import datetime
import json
import uuid
import re


app = Flask(__name__)

RESULTS_ROOT = Path("results")
RESULTS_ROOT.mkdir(exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


# =====================================================================
# HTML
# =====================================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>RTL vs Simics Complexity Fidelity Assessment</title>

<style>

:root {

    --background: #f3f5f8;

    --card: #ffffff;

    --text: #18212f;

    --muted: #687386;

    --border: #e2e8f0;

    --blue: #0068b5;
    --blue-dark: #004f8a;

    --green: #16a34a;
    --green-bg: #dcfce7;

    --yellow: #ca8a04;
    --yellow-bg: #fef9c3;

    --red: #dc2626;
    --red-bg: #fee2e2;

    --gray-bg: #f1f5f9;
}


* {
    box-sizing: border-box;
}


body {

    margin: 0;

    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Arial,
        sans-serif;

    background: var(--background);

    color: var(--text);
}


.container {

    max-width: 1400px;

    margin: 0 auto;

    padding: 34px 24px 80px;
}


/* ================================================================
   Top
================================================================ */

.topbar {

    display: flex;

    justify-content: space-between;

    align-items: flex-start;

    gap: 30px;

    margin-bottom: 28px;
}


.title h1 {

    margin: 0 0 6px;

    font-size: 31px;
}


.title p {

    margin: 0;

    color: var(--muted);
}


.nav-links a {

    text-decoration: none;

    background: white;

    border: 1px solid var(--border);

    color: var(--text);

    padding: 10px 15px;

    border-radius: 8px;

    font-size: 14px;

    display: inline-block;
}


.nav-links a:hover {

    background: #f8fafc;
}


/* ================================================================
   Panels
================================================================ */

.panel {

    background: var(--card);

    border: 1px solid var(--border);

    border-radius: 12px;

    padding: 26px;

    margin-bottom: 24px;

    box-shadow:
        0 1px 2px rgba(0,0,0,.03),
        0 6px 18px rgba(0,0,0,.025);
}


.panel h2 {

    margin: 0 0 8px;

    font-size: 21px;
}


.panel-description {

    color: var(--muted);

    margin-bottom: 22px;

    font-size: 14px;
}


/* ================================================================
   Forms
================================================================ */

.form-grid {

    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(250px, 1fr));

    gap: 18px;
}


.form-item {

    border: 1px solid var(--border);

    background: #fafbfc;

    padding: 17px;

    border-radius: 9px;
}


.form-item label {

    display: block;

    font-weight: 700;

    margin-bottom: 6px;
}


.form-help {

    color: var(--muted);

    font-size: 12px;

    min-height: 34px;

    margin-bottom: 10px;
}


input[type=text],
input[type=file],
select,
textarea {

    width: 100%;

    border: 1px solid #cbd5e1;

    border-radius: 7px;

    padding: 10px 11px;

    font: inherit;

    background: white;
}


textarea {

    min-height: 400px;

    font-family: monospace;

    font-size: 13px;
}


button,
.button {

    border: 0;

    display: inline-block;

    background: var(--blue);

    color: white;

    padding: 11px 20px;

    border-radius: 7px;

    text-decoration: none;

    font-weight: 600;

    cursor: pointer;

    font-size: 14px;
}


button:hover,
.button:hover {

    background: var(--blue-dark);
}


.button-secondary {

    background: #475569;
}


.button-danger {

    background: #b91c1c;
}


.actions {

    margin-top: 20px;

    display: flex;

    flex-wrap: wrap;

    gap: 10px;
}


/* ================================================================
   Report heading
================================================================ */

.report-header {

    background:
        linear-gradient(
            135deg,
            #ffffff 0%,
            #f4f9fc 100%
        );

    border: 1px solid var(--border);

    border-radius: 12px;

    padding: 28px;

    margin-bottom: 22px;
}


.report-header h2 {

    margin: 0 0 12px;

    font-size: 27px;
}


.metadata {

    display: flex;

    flex-wrap: wrap;

    gap: 20px;

    color: var(--muted);

    font-size: 13px;
}


.metadata strong {

    color: var(--text);
}


/* ================================================================
   KPI cards
================================================================ */

.cards {

    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(195px, 1fr));

    gap: 16px;

    margin-bottom: 24px;
}


.card {

    background: white;

    border: 1px solid var(--border);

    border-radius: 11px;

    padding: 20px;

    position: relative;

    overflow: hidden;
}


.card::before {

    content: "";

    position: absolute;

    left: 0;

    top: 0;

    bottom: 0;

    width: 5px;

    background: #94a3b8;
}


.card.good::before {
    background: var(--green);
}

.card.medium::before {
    background: var(--yellow);
}

.card.bad::before {
    background: var(--red);
}


.card-label {

    text-transform: uppercase;

    letter-spacing: .05em;

    color: var(--muted);

    font-size: 11px;

    font-weight: 700;

    margin-bottom: 9px;
}


.card-value {

    font-size: 27px;

    font-weight: 750;

    overflow-wrap: anywhere;
}


.card.good .card-value {
    color: var(--green);
}

.card.medium .card-value {
    color: var(--yellow);
}

.card.bad .card-value {
    color: var(--red);
}


/* ================================================================
   Status badges
================================================================ */

.status {

    display: inline-block;

    padding: 5px 10px;

    border-radius: 999px;

    font-size: 12px;

    font-weight: 700;
}


.status-good {

    color: #166534;

    background: var(--green-bg);
}


.status-medium {

    color: #854d0e;

    background: var(--yellow-bg);
}


.status-bad {

    color: #991b1b;

    background: var(--red-bg);
}


.status-neutral {

    color: #475569;

    background: var(--gray-bg);
}


/* ================================================================
   Progress bar
================================================================ */

.progress {

    height: 10px;

    background: #e5e7eb;

    border-radius: 999px;

    overflow: hidden;

    margin-top: 11px;
}


.progress-bar {

    height: 100%;
}


.progress-bar.good {
    background: var(--green);
}

.progress-bar.medium {
    background: var(--yellow);
}

.progress-bar.bad {
    background: var(--red);
}


/* ================================================================
   Tables / JSON rendering
================================================================ */

.section-title {

    border-bottom: 1px solid var(--border);

    padding-bottom: 12px;

    margin-bottom: 18px !important;
}


table {

    width: 100%;

    border-collapse: collapse;

    margin: 8px 0 15px;
}


th,
td {

    padding: 11px 13px;

    border-bottom: 1px solid var(--border);

    text-align: left;

    vertical-align: top;
}


th {

    background: #f8fafc;

    font-size: 12px;

    text-transform: uppercase;

    color: #475569;
}


.field-name {

    width: 30%;

    font-weight: 650;

    color: #334155;
}


.json-item {

    padding: 14px;

    margin: 10px 0;

    background: #fafafa;

    border: 1px solid var(--border);

    border-radius: 8px;
}


.item-number {

    font-size: 11px;

    font-weight: 700;

    color: var(--muted);

    margin-bottom: 7px;
}


ul {

    padding-left: 22px;
}


li {

    margin: 6px 0;
}


/* ================================================================
   History
================================================================ */

.history-table a {

    color: var(--blue);

    text-decoration: none;

    font-weight: 600;
}


.history-table a:hover {

    text-decoration: underline;
}


/* ================================================================
   Raw JSON
================================================================ */

details {

    border: 1px solid var(--border);

    border-radius: 8px;

    padding: 13px 15px;

    margin-top: 12px;

    background: #fafafa;
}


summary {

    cursor: pointer;

    font-weight: 600;
}


pre {

    background: #111827;

    color: #e5e7eb;

    border-radius: 8px;

    padding: 17px;

    overflow-x: auto;

    white-space: pre-wrap;

    word-break: break-word;

    font-size: 12px;
}


/* ================================================================
   Messages
================================================================ */

.error {

    background: var(--red-bg);

    color: #991b1b;

    border: 1px solid #fecaca;

    border-radius: 8px;

    padding: 14px 17px;

    margin-bottom: 20px;
}


.success {

    background: var(--green-bg);

    color: #166534;

    border: 1px solid #bbf7d0;

    border-radius: 8px;

    padding: 14px 17px;

    margin-bottom: 20px;
}


@media(max-width: 650px) {

    .topbar {
        display: block;
    }

    .nav-links {
        margin-top: 15px;
    }

}

</style>

</head>


<body>

<div class="container">


<!-- ================================================================
     TOP
================================================================ -->

<div class="topbar">

    <div class="title">

        <h1>
            RTL vs Simics Complexity Fidelity Assessment
        </h1>

        <p>
            Repository and visualization of LLM-generated
            complexity and fidelity assessments.
        </p>

    </div>

    <div class="nav-links">

        <a href="{{ url_for('index') }}">
            New Assessment
        </a>

        <a href="{{ url_for('history') }}">
            Assessment History
        </a>

    </div>

</div>


{% if error %}

<div class="error">
    {{ error }}
</div>

{% endif %}


{% if success %}

<div class="success">
    {{ success }}
</div>

{% endif %}


<!-- ================================================================
     NEW ASSESSMENT
================================================================ -->

{% if page == "new" %}

<div class="panel">

    <h2>Create Assessment</h2>

    <div class="panel-description">
        Store the RTL analysis, Simics analysis, and the final
        LLM-generated fidelity assessment under a component.
    </div>


    <form
        method="POST"
        enctype="multipart/form-data"
    >

        <div class="form-grid">


            <div class="form-item">

                <label>
                    Component
                </label>

                <div class="form-help">
                    Example: Core, Memory Controller, PCIe,
                    UPI, Power Management, BIOS.
                </div>

                <input
                    type="text"
                    name="component"
                    placeholder="Example: Memory Controller"
                    required
                >

            </div>


            <div class="form-item">

                <label>
                    Assessment Name
                </label>

                <div class="form-help">
                    Optional human-readable name for this run.
                </div>

                <input
                    type="text"
                    name="assessment_name"
                    placeholder="Example: DMR Memory Controller v1"
                >

            </div>


            <div class="form-item">

                <label>
                    RTL Analysis JSON
                </label>

                <div class="form-help">
                    Output generated by the RTL complexity prompt.
                </div>

                <input
                    type="file"
                    name="rtl_file"
                    accept=".json"
                    required
                >

            </div>


            <div class="form-item">

                <label>
                    Simics Analysis JSON
                </label>

                <div class="form-help">
                    Output generated by the Simics analysis prompt.
                </div>

                <input
                    type="file"
                    name="simics_file"
                    accept=".json"
                    required
                >

            </div>


            <div class="form-item">

                <label>
                    Final Assessment JSON
                </label>

                <div class="form-help">
                    Final RTL-vs-Simics comparison produced
                    previously by the LLM.
                </div>

                <input
                    type="file"
                    name="assessment_file"
                    accept=".json"
                    required
                >

            </div>

        </div>


        <div class="actions">

            <button type="submit">
                Save and Generate Dashboard
            </button>

        </div>

    </form>

</div>

{% endif %}


<!-- ================================================================
     HISTORY
================================================================ -->

{% if page == "history" %}

<div class="panel">

    <h2>Assessment History</h2>

    <div class="panel-description">
        Open any previous assessment to review or revise it.
    </div>


    {% if history_items %}

    <table class="history-table">

        <thead>

        <tr>
            <th>Component</th>
            <th>Assessment</th>
            <th>Created</th>
            <th>Updated</th>
            <th>Run ID</th>
            <th></th>
        </tr>

        </thead>


        <tbody>

        {% for item in history_items %}

        <tr>

            <td>
                {{ item.component }}
            </td>

            <td>
                {{ item.assessment_name }}
            </td>

            <td>
                {{ item.created }}
            </td>

            <td>
                {{ item.updated }}
            </td>

            <td>
                {{ item.run_id }}
            </td>

            <td>

                <a href="{{ url_for(
                    'view_assessment',
                    component=item.component_slug,
                    run_id=item.run_id
                ) }}">
                    Open
                </a>

            </td>

        </tr>

        {% endfor %}

        </tbody>

    </table>

    {% else %}

    <p>No saved assessments yet.</p>

    {% endif %}

</div>

{% endif %}


<!-- ================================================================
     DASHBOARD
================================================================ -->

{% if page == "view" and assessment %}


<div class="report-header">

    <h2>
        {{ assessment_name }}
    </h2>

    <div class="metadata">

        <span>
            Component:
            <strong>{{ component }}</strong>
        </span>

        <span>
            Run:
            <strong>{{ run_id }}</strong>
        </span>

        <span>
            Created:
            <strong>{{ created }}</strong>
        </span>

        <span>
            Updated:
            <strong>{{ updated }}</strong>
        </span>

    </div>

</div>


<!-- KPI CARDS -->

{% if kpis %}

<div class="cards">

    {% for item in kpis %}

    <div class="card {{ item.status }}">

        <div class="card-label">
            {{ item.label }}
        </div>

        <div class="card-value">
            {{ item.value }}
        </div>


        {% if item.percentage is not none %}

        <div class="progress">

            <div
                class="progress-bar {{ item.status }}"
                style="width: {{ item.percentage }}%"
            ></div>

        </div>

        {% endif %}

    </div>

    {% endfor %}

</div>

{% endif %}


<!-- FINAL REPORT -->

<div class="panel">

    <h2 class="section-title">
        Final Assessment
    </h2>

    {{ render_json(assessment) | safe }}

</div>


<!-- UPDATE -->

<div class="panel">

    <h2>
        Revise Final Assessment
    </h2>

    <div class="panel-description">
        Replace the final LLM-generated assessment while preserving
        the original RTL and Simics analysis.
    </div>


    <form
        action="{{ url_for(
            'update_assessment',
            component=component_slug,
            run_id=run_id
        ) }}"
        method="POST"
        enctype="multipart/form-data"
    >

        <div class="form-grid">


            <div class="form-item">

                <label>
                    Replace Final Assessment JSON
                </label>

                <div class="form-help">
                    Upload a newer LLM-generated comparison.
                </div>

                <input
                    type="file"
                    name="assessment_file"
                    accept=".json"
                    required
                >

            </div>


            <div class="form-item">

                <label>
                    Assessment Name
                </label>

                <div class="form-help">
                    You can also rename this assessment.
                </div>

                <input
                    type="text"
                    name="assessment_name"
                    value="{{ assessment_name }}"
                >

            </div>

        </div>


        <div class="actions">

            <button type="submit">
                Save Revision
            </button>

        </div>

    </form>

</div>


<!-- SOURCE JSON -->

<div class="panel">

    <h2 class="section-title">
        Stored Source Data
    </h2>


    <details>

        <summary>
            RTL Analysis JSON
        </summary>

        <pre>{{ rtl_raw }}</pre>

    </details>


    <details>

        <summary>
            Simics Analysis JSON
        </summary>

        <pre>{{ simics_raw }}</pre>

    </details>


    <details>

        <summary>
            Final Assessment JSON
        </summary>

        <pre>{{ assessment_raw }}</pre>

    </details>

</div>


{% endif %}


</div>

</body>
</html>
"""


# =====================================================================
# Utility
# =====================================================================

def slugify(text):

    text = text.strip().lower()

    text = re.sub(
        r"[^a-z0-9]+",
        "-",
        text
    )

    return text.strip("-") or "unknown-component"


def humanize_key(key):

    return (
        str(key)
        .replace("_", " ")
        .replace("-", " ")
        .strip()
        .title()
    )


def format_scalar(value):

    if value is None:
        return "Not specified"

    if isinstance(value, bool):
        return "Yes" if value else "No"

    if isinstance(value, float):

        if value.is_integer():
            return str(int(value))

        return f"{value:.3f}".rstrip("0").rstrip(".")

    return str(value)


# =====================================================================
# Coverage Status
# =====================================================================

def percentage_from_value(value):

    if isinstance(value, (int, float)):

        number = float(value)

        # 0.82 -> 82%
        if 0 <= number <= 1:
            return number * 100

        if 0 <= number <= 100:
            return number

        return None


    if isinstance(value, str):

        candidate = value.strip().replace("%", "")

        try:

            number = float(candidate)

            if "%" not in value and 0 <= number <= 1:
                return number * 100

            if 0 <= number <= 100:
                return number

        except ValueError:
            pass

    return None


def status_from_percentage(value):

    percentage = percentage_from_value(value)

    if percentage is None:
        return "neutral"

    # Change these thresholds if methodology changes.
    if percentage >= 80:
        return "good"

    if percentage >= 50:
        return "medium"

    return "bad"


def status_from_text(value):

    text = str(value).lower().strip()

    good_terms = [
        "matched",
        "well covered",
        "fully covered",
        "high",
        "adequate",
        "supported",
        "complete",
        "good"
    ]

    medium_terms = [
        "partial",
        "partially",
        "medium",
        "moderate",
        "limited",
        "conditionally adequate"
    ]

    bad_terms = [
        "missing",
        "not covered",
        "low",
        "inadequate",
        "unsupported",
        "absent",
        "poor"
    ]

    for term in bad_terms:

        if term in text:
            return "bad"

    for term in medium_terms:

        if term in text:
            return "medium"

    for term in good_terms:

        if term in text:
            return "good"

    return "neutral"


def status_for_value(value):

    percentage = percentage_from_value(value)

    if percentage is not None:
        return status_from_percentage(value)

    return status_from_text(value)


def render_scalar(value):

    formatted = escape(
        format_scalar(value)
    )

    status = status_for_value(value)

    if status != "neutral":

        return (
            f'<span class="status status-{status}">'
            f'{formatted}'
            '</span>'
        )

    return str(formatted)


# =====================================================================
# JSON -> HTML Renderer
# =====================================================================

def render_json_html(data):

    if isinstance(data, dict):

        html = "<table>"

        for key, value in data.items():

            html += "<tr>"

            html += (
                '<td class="field-name">'
                + str(escape(humanize_key(key)))
                + "</td>"
            )

            html += "<td>"

            html += render_json_html(value)

            html += "</td>"

            html += "</tr>"

        html += "</table>"

        return html


    if isinstance(data, list):

        if not data:
            return "<span>None</span>"

        if all(
            isinstance(item, dict)
            for item in data
        ):

            html = ""

            for index, item in enumerate(
                data,
                start=1
            ):

                html += '<div class="json-item">'

                html += (
                    '<div class="item-number">'
                    f"ITEM {index}"
                    "</div>"
                )

                html += render_json_html(item)

                html += "</div>"

            return html


        html = "<ul>"

        for item in data:

            html += "<li>"

            html += render_json_html(item)

            html += "</li>"

        html += "</ul>"

        return html


    return render_scalar(data)


# =====================================================================
# KPI Extraction
# =====================================================================

KPI_NAMES = {

    "rtl_complexity":
        "RTL Complexity",

    "complexity":
        "RTL Complexity",

    "simics_fidelity":
        "Simics Fidelity",

    "simics_level":
        "Simics Fidelity",

    "fidelity_level":
        "Simics Fidelity",

    "fidelity_coverage":
        "Fidelity Coverage",

    "coverage":
        "Fidelity Coverage",

    "coverage_score":
        "Fidelity Coverage",

    "gap_score":
        "Gap Score",

    "fidelity_gap":
        "Gap Score",

    "adequacy":
        "Adequacy",

    "adequacy_level":
        "Adequacy",

    "overall_adequacy":
        "Adequacy"
}


def extract_kpis(data):

    found = {}

    def walk(value):

        if isinstance(value, dict):

            for key, child in value.items():

                normalized = (
                    key
                    .lower()
                    .strip()
                    .replace(" ", "_")
                    .replace("-", "_")
                )

                if normalized in KPI_NAMES:

                    label = KPI_NAMES[normalized]

                    if label not in found:

                        scalar = None

                        if not isinstance(
                            child,
                            (dict, list)
                        ):
                            scalar = child

                        elif isinstance(child, dict):

                            for candidate in [
                                "level",
                                "value",
                                "score",
                                "classification",
                                "status"
                            ]:

                                if candidate in child:

                                    scalar = child[candidate]
                                    break

                        if scalar is not None:

                            found[label] = scalar

                walk(child)


        elif isinstance(value, list):

            for item in value:
                walk(item)


    walk(data)


    order = [
        "RTL Complexity",
        "Simics Fidelity",
        "Fidelity Coverage",
        "Gap Score",
        "Adequacy"
    ]


    cards = []

    for label in order:

        if label not in found:
            continue

        value = found[label]

        percentage = percentage_from_value(value)

        status = status_for_value(value)


        # Gap Score uses inverse semantics:
        # LOW gap = GOOD.
        if label == "Gap Score" and percentage is not None:

            if percentage <= 20:
                status = "good"

            elif percentage <= 50:
                status = "medium"

            else:
                status = "bad"


        cards.append({
            "label": label,
            "value": format_scalar(value),
            "percentage": percentage,
            "status": status
        })


    return cards


# =====================================================================
# JSON files
# =====================================================================

def read_json_upload(file):

    if file is None or file.filename == "":
        raise ValueError("JSON file was not provided.")

    try:

        return json.load(file)

    except json.JSONDecodeError as exc:

        raise ValueError(
            f"{file.filename} is not valid JSON: {exc}"
        )


def save_json(path, data):

    with path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


def load_json(path):

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# =====================================================================
# Metadata
# =====================================================================

def load_metadata(run_dir):

    path = run_dir / "metadata.json"

    if not path.exists():
        return {}

    return load_json(path)


def save_metadata(run_dir, metadata):

    save_json(
        run_dir / "metadata.json",
        metadata
    )


# =====================================================================
# History
# =====================================================================

def get_history():

    history_items = []

    for component_dir in RESULTS_ROOT.iterdir():

        if not component_dir.is_dir():
            continue

        for run_dir in component_dir.iterdir():

            if not run_dir.is_dir():
                continue

            metadata_path = (
                run_dir /
                "metadata.json"
            )

            if not metadata_path.exists():
                continue

            try:

                metadata = load_json(
                    metadata_path
                )

                history_items.append(
                    metadata
                )

            except Exception:
                continue


    history_items.sort(
        key=lambda item:
            item.get("updated", ""),
        reverse=True
    )

    return history_items


# =====================================================================
# Jinja
# =====================================================================

@app.context_processor
def template_helpers():

    return {
        "render_json": render_json_html
    }


# =====================================================================
# New Assessment
# =====================================================================

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET":

        return render_template_string(
            HTML_TEMPLATE,
            page="new",
            error=None,
            success=None
        )


    try:

        component = (
            request.form
            .get("component", "")
            .strip()
        )

        if not component:
            raise ValueError(
                "Component name is required."
            )


        assessment_name = (
            request.form
            .get("assessment_name", "")
            .strip()
        )


        rtl = read_json_upload(
            request.files.get(
                "rtl_file"
            )
        )

        simics = read_json_upload(
            request.files.get(
                "simics_file"
            )
        )

        assessment = read_json_upload(
            request.files.get(
                "assessment_file"
            )
        )


        component_slug = slugify(
            component
        )


        component_dir = (
            RESULTS_ROOT /
            component_slug
        )

        component_dir.mkdir(
            parents=True,
            exist_ok=True
        )


        run_id = uuid.uuid4().hex[:8]

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        run_dir = (
            component_dir /
            run_id
        )

        run_dir.mkdir(
            parents=True,
            exist_ok=False
        )


        if not assessment_name:

            assessment_name = (
                f"{component} Assessment"
            )


        save_json(
            run_dir /
            "rtl_analysis.json",
            rtl
        )

        save_json(
            run_dir /
            "simics_analysis.json",
            simics
        )

        save_json(
            run_dir /
            "fidelity_assessment.json",
            assessment
        )


        metadata = {

            "component":
                component,

            "component_slug":
                component_slug,

            "assessment_name":
                assessment_name,

            "run_id":
                run_id,

            "created":
                timestamp,

            "updated":
                timestamp
        }


        save_metadata(
            run_dir,
            metadata
        )


        return redirect(
            url_for(
                "view_assessment",
                component=component_slug,
                run_id=run_id
            )
        )


    except Exception as exc:

        return render_template_string(
            HTML_TEMPLATE,
            page="new",
            error=str(exc),
            success=None
        )


# =====================================================================
# History
# =====================================================================

@app.route("/history")
def history():

    return render_template_string(
        HTML_TEMPLATE,
        page="history",
        history_items=get_history(),
        error=None,
        success=None
    )


# =====================================================================
# View existing assessment
# =====================================================================

@app.route(
    "/assessment/<component>/<run_id>"
)
def view_assessment(
    component,
    run_id
):

    run_dir = (
        RESULTS_ROOT /
        component /
        run_id
    )


    if not run_dir.exists():

        return (
            "Assessment not found.",
            404
        )


    try:

        rtl = load_json(
            run_dir /
            "rtl_analysis.json"
        )

        simics = load_json(
            run_dir /
            "simics_analysis.json"
        )

        assessment = load_json(
            run_dir /
            "fidelity_assessment.json"
        )

        metadata = load_metadata(
            run_dir
        )


        return render_template_string(

            HTML_TEMPLATE,

            page="view",

            error=None,
            success=request.args.get(
                "success"
            ),

            rtl=rtl,
            simics=simics,
            assessment=assessment,

            rtl_raw=json.dumps(
                rtl,
                indent=2,
                ensure_ascii=False
            ),

            simics_raw=json.dumps(
                simics,
                indent=2,
                ensure_ascii=False
            ),

            assessment_raw=json.dumps(
                assessment,
                indent=2,
                ensure_ascii=False
            ),

            kpis=extract_kpis(
                assessment
            ),

            component=metadata.get(
                "component",
                component
            ),

            component_slug=component,

            assessment_name=metadata.get(
                "assessment_name",
                "Assessment"
            ),

            run_id=run_id,

            created=metadata.get(
                "created",
                ""
            ),

            updated=metadata.get(
                "updated",
                ""
            )
        )


    except Exception as exc:

        return (
            f"Unable to load assessment: {exc}",
            500
        )


# =====================================================================
# Update final LLM assessment
# =====================================================================

@app.route(
    "/assessment/<component>/<run_id>/update",
    methods=["POST"]
)
def update_assessment(
    component,
    run_id
):

    run_dir = (
        RESULTS_ROOT /
        component /
        run_id
    )


    if not run_dir.exists():

        return (
            "Assessment not found.",
            404
        )


    try:

        assessment = read_json_upload(
            request.files.get(
                "assessment_file"
            )
        )


        #
        # Keep previous version
        #

        current_file = (
            run_dir /
            "fidelity_assessment.json"
        )


        if current_file.exists():

            revision_dir = (
                run_dir /
                "revisions"
            )

            revision_dir.mkdir(
                exist_ok=True
            )


            revision_timestamp = (
                datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )
            )


            old_assessment = load_json(
                current_file
            )


            save_json(
                revision_dir /
                (
                    "fidelity_assessment_"
                    f"{revision_timestamp}.json"
                ),
                old_assessment
            )


        #
        # Save new assessment
        #

        save_json(
            current_file,
            assessment
        )


        #
        # Update metadata
        #

        metadata = load_metadata(
            run_dir
        )


        assessment_name = (
            request.form
            .get(
                "assessment_name",
                ""
            )
            .strip()
        )


        if assessment_name:

            metadata[
                "assessment_name"
            ] = assessment_name


        metadata["updated"] = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )


        save_metadata(
            run_dir,
            metadata
        )


        return redirect(

            url_for(
                "view_assessment",

                component=component,

                run_id=run_id,

                success=(
                    "Assessment revision "
                    "saved successfully."
                )
            )
        )


    except Exception as exc:

        return (
            f"Unable to update assessment: {exc}",
            400
        )


# =====================================================================
# Run
# =====================================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
