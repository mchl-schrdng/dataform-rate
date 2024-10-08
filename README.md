# Dataform Rate

[![codecov](https://codecov.io/gh/mchl-schrdng/dataform-rate/main/graph/badge.svg)](https://codecov.io/gh/username/repository)
[![ci](https://github.com/mchl-schrdng/dataform-rate/actions/workflows/ci.yaml/badge.svg)](https://github.com/mchl-schrdng/dataform-rate/actions)
[![dataform-rate](https://github.com/mchl-schrdng/dataform-rate/actions/workflows/dataform-rate.yaml/badge.svg)](https://github.com/mchl-schrdng/dataform-rate/actions)


Dataform Rate is a Python tool that analyzes your Dataform project, evaluates it against best practices, and reports any violations.
It's currently in an early stage, available as a proof of concept 

![image](https://github.com/user-attachments/assets/c2368410-7d3c-429b-a156-2ba646747dce)

## Features

- **Metadata validation**: Ensures models have essential fields like name, description, columns, meta, and tags.
- **Naming conventions**: Verifies that model and column names follow the snake_case convention.
- **SQL best practices**: Discourages the use of `SELECT *` and ensures that SQL code doesn't exceed a certain number of lines.
- **Partitioning**: Ensures that models are correctly partitioned when using BigQuery.
- **Required labels**: Validates the presence of necessary labels (e.g., cost_center) in BigQuery configurations.
- **Comprehensive descriptions**: Encourages detailed descriptions of models and their columns.

## Usage

To run the Dataform Rate Tool, use the following command:

```bash
python main.py --model-path '../definitions/**/*.sqlx' --max-lines 200 --output-format console
```

## Command-Line arguments
- --model-path: Path to .sqlx files using a glob pattern. Defaults to '../models/**/*.sqlx'.
- --max-lines: Maximum allowed number of SQL lines. Default is 200.
- --output-format: Format for the output report. Choices are console or json. Default is console.
- --log-level: Logging level. Choices are DEBUG, INFO, WARNING, ERROR. Default is INFO.

## Example output
Console Output Example:

```bash
============================================================
Summary
============================================================
❌ Total Errors: 6
⚠️ Total Warnings: 3
📂 Total Files Checked: 2
✅ Files Without Issues: 0
============================================================
Detailed Errors
============================================================
📄 File: ./definitions/non_compliant_model.sqlx
  Errors:
Error: ERROR] Missing mandatory metadata fields: description, schema.
Error: ERROR] Model is missing partitioning information.
Error: ERROR] Missing required labels: env, team.
  Warnings:
Warning: ARNING] Columns missing descriptions: user_id.
Warning: ARNING] Description is too short; provide a more comprehensive description.
------------------------------------------------------------
📄 File: ./definitions/compliant_model.sqlx
  Errors:
Error: ERROR] Missing mandatory metadata fields: schema, tags.
Error: ERROR] Model is missing partitioning information.
Error: ERROR] Missing required labels: env, team.
  Warnings:
Warning: ARNING] Description is too short; provide a more comprehensive description.
------------------------------------------------------------
Completed validation
```

JSON output example:
```json
[
  {
    "model": "model_1",
    "file_path": "../definitions/model_1.sqlx",
    "rule": "has_mandatory_metadata",
    "message": "Missing mandatory metadata fields: description, tags.",
    "severity": "ERROR"
  },
  {
    "model": "model_2",
    "file_path": "../definitions/model_2.sqlx",
    "rule": "sql_line_limit",
    "message": "SQL code exceeds 200 lines.",
    "severity": "WARNING"
  }
]
```

## How to add new rules
To add a new rule, define a function in rules.py that accepts a model and returns a RuleViolation if the model violates the rule. Add the function to the RULES list.

```python
def new_rule(model):
    # Rule logic
    return RuleViolation(message="Violation example", severity="ERROR")
```

## How to setup a GitHub actions

If you want to implement these checks in your pipeline (and you are using GitHub), you can add a .yml file in the .github/workflows folder by following this example.

```yaml
name: Dataform Best Practice Check

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jjobs:
  run-dataform-rate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Dataform repo (where the action is running)
        uses: actions/checkout@v3

      - name: Checkout dataform-rate repository (pinned version)
        uses: actions/checkout@v3
        with:
          repository: mchl-schrdng/dataform-rate
          path: dataform-rate
          ref: v0.1.0  # Use the version you want to use.

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r dataform-rate/requirements.txt

      - name: Run Dataform Rate Check
        run: |
          python dataform-rate/src/main.py --model-path './definitions/**/*.sqlx' --output-format console
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue if you have suggestions or bug reports.
