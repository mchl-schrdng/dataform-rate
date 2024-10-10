import pytest
from src.rules import has_mandatory_metadata, naming_conventions, RuleViolation
from src.parser import parse_model
from src.evaluator import evaluate_models
from src.reporter import report_violations

def test_has_mandatory_metadata():
    model = {
        'name': 'test_model',
        'columns': {'id': {'description': 'Identifier'}},
        'tags': []
    }
    assert isinstance(has_mandatory_metadata(model), RuleViolation)

    model['tags'] = ['important']
    assert has_mandatory_metadata(model) is None

def test_naming_conventions():
    assert naming_conventions({'name': 'valid_name'}) is None
    result = naming_conventions({'name': 'InvalidName'})
    assert isinstance(result, RuleViolation)
    assert "snake_case" in result.message

def test_parse_model():
    content = '''config { name: "valid_model" }'''
    assert parse_model(content, "path/to/model.sqlx") is not None

def test_evaluate_models():
    model = {'name': 'valid_model', 'schema': 'schema', 'columns': {}, 'tags': ['important']}
    assert len(evaluate_models([model])) == 0

def test_report_violations_console(capsys):
    violations = [{'model': 'test_model', 'message': 'Test violation'}]
    report_violations(violations, output_format='console', all_checked_files=[])
    assert "Test violation" in capsys.readouterr().out

def test_report_violations_json(capsys):
    violations = [{'model': 'test_model', 'message': 'Test violation'}]
    report_violations(violations, output_format='json', all_checked_files=[])
    assert '"message": "Test violation"' in capsys.readouterr().out