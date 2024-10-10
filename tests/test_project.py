import pytest
from src.rules import has_mandatory_metadata, naming_conventions, RuleViolation
from src.parser import parse_model
from src.evaluator import evaluate_models
from src.reporter import report_violations

def test_has_mandatory_metadata_missing_metadata():
    model = {
        'name': 'test_model',
        'description': 'A test model',
        'schema': 'test_schema',
        'columns': {
            'id': {'description': 'Identifier'},
            'name': {'description': 'Name of the entity'}
        },
        'meta': {},
        'tags': []
    }
    result = has_mandatory_metadata(model)
    assert isinstance(result, RuleViolation), f"Expected RuleViolation but got {result}."

def test_has_mandatory_metadata_success():
    model = {
        'name': 'test_model',
        'description': 'A test model',
        'schema': 'test_schema',
        'columns': {
            'id': {'description': 'Identifier'},
            'name': {'description': 'Name of the entity'}
        },
        'tags': ['important']
    }
    result = has_mandatory_metadata(model)
    assert result is None, f"Expected None but got {result.message}."

def test_naming_conventions():
    valid_model = {'name': 'valid_name', 'columns': {'valid_column': 'Valid column'}}
    assert naming_conventions(valid_model) is None, "Expected None for valid model names."

    invalid_model = {'name': 'InvalidName', 'columns': {'InvalidColumn': 'Invalid column'}}
    result = naming_conventions(invalid_model)
    assert isinstance(result, RuleViolation), "Expected RuleViolation for invalid model names."
    assert "snake_case" in result.message, f"Expected snake_case violation, got {result.message}."

def test_parse_model_violation():
    content = '''model {name: "invalid_model"}'''
    model = parse_model(content, "path/to/model.sqlx")
    assert model is None, "Expected None for invalid model parsing."

def test_parse_model_success():
    content = '''model {name: "valid_model", description: "A valid model"}'''
    model = parse_model(content, "path/to/model.sqlx")
    assert model is not None, "Expected parsed model object."

def test_evaluate_models_no_violations():
    model = {
        'name': 'test_model',
        'file_path': 'path/to/model.sqlx',
        'description': 'Test model'
    }
    violations = evaluate_models([model])
    assert len(violations) == 0, f"Expected no violations, got {len(violations)}."

def test_evaluate_models_with_violations():
    model = {
        'name': 'Invalid_Model',
        'file_path': 'path/to/model.sqlx',
        'description': ''
    }
    violations = evaluate_models([model])
    assert len(violations) > 0, "Expected some violations, but found none."

def test_report_violations_console(capsys):
    violations = [
        {
            'model': 'test_model',
            'message': 'Test violation',
            'severity': 'ERROR',
            'file_path': 'test_path.sqlx'
        }
    ]
    report_violations(violations, output_format='console')
    captured = capsys.readouterr()
    assert "Test violation" in captured.out, "Expected violation message in console output."

def test_report_violations_json(capsys):
    violations = [
        {
            'model': 'test_model',
            'message': 'Test violation',
            'severity': 'ERROR',
            'file_path': 'test_path.sqlx'
        }
    ]
    report_violations(violations, output_format='json')
    captured = capsys.readouterr()
    assert '"message": "Test violation"' in captured.out, "Expected JSON formatted violation in output."