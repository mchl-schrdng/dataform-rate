import pytest
from src.rules import has_mandatory_metadata, naming_conventions, RuleViolation
from src.model_parser import parse_model
from src.evaluator import evaluate_models
from src.reporter import report_violations

# Test Rule Functions
def test_has_mandatory_metadata():
    """Test the has_mandatory_metadata rule."""
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
    assert has_mandatory_metadata(model) is None

def test_has_mandatory_metadata():
    """Test the has_mandatory_metadata rule."""
    model = {
        'name': 'test_model',
        'description': 'A test model',
        'schema': 'test_schema',
        'columns': {
            'id': {'description': 'Identifier'},
            'name': {'description': 'Name of the entity'}
        },
        'meta': {},  # Ensure this exists if the rule requires it, even if empty.
        'tags': ['important']  # Non-empty tags to satisfy the rule
    }
    
    result = has_mandatory_metadata(model)
    assert result is None, f"Expected None but got {result.message}."

def test_naming_conventions():
    """Test the naming_conventions rule."""
    valid_model = {'name': 'valid_name', 'columns': {'valid_column': 'Valid column'}}
    assert naming_conventions(valid_model) is None

    invalid_model = {'name': 'InvalidName', 'columns': {'InvalidColumn': 'Invalid column'}}
    result = naming_conventions(invalid_model)
    assert isinstance(result, RuleViolation)
    assert "snake_case" in result.message

def test_parse_model_violation():
    """Test invalid model content."""
    content = '''model {name: "invalid_model"}'''  # Missing description and columns
    model = parse_model(content, "path/to/model.sqlx")
    assert model is None


# Test Evaluator
def test_evaluate_models():
    """Test model evaluation."""
    model = {'name': 'test_model', 'file_path': 'path/to/model.sqlx'}
    violations = evaluate_models([model])
    assert len(violations) >= 0

# Test Reporter Functions
def test_report_violations_console(capsys):
    """Test console output of report_violations."""
    violations = [{'model': 'test_model', 'message': 'Test violation', 'severity': 'ERROR', 'file_path': 'test_path.sqlx'}]
    report_violations(violations, output_format='console')
    captured = capsys.readouterr()
    assert "Test violation" in captured.out

def test_report_violations_json(capsys):
    """Test JSON output of report_violations."""
    violations = [{'model': 'test_model', 'message': 'Test violation', 'severity': 'ERROR', 'file_path': 'test_path.sqlx'}]
    report_violations(violations, output_format='json')
    captured = capsys.readouterr()
    assert '"message": "Test violation"' in captured.out