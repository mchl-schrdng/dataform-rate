import pytest
from src.rules import has_mandatory_metadata

def test_has_mandatory_metadata():
    model = {
        'name': 'test_model',
        'description': 'A test model',
        'schema': 'test_schema',
        'columns': {'id': {'description': 'Identifier'}},
        'tags': ['important']
    }
    assert has_mandatory_metadata(model) is None, "Expected no violations when metadata is valid"

def test_naming_conventions():
    valid_model = {'name': 'valid_name', 'columns': {'valid_column': 'Valid column'}}
    assert naming_conventions(valid_model) is None, "Expected no violations for valid snake_case naming."

    invalid_model = {'name': 'InvalidName', 'columns': {'InvalidColumn': 'Invalid column'}}
    result = naming_conventions(invalid_model)
    assert isinstance(result, RuleViolation), "Expected a RuleViolation for invalid naming convention."
    assert "snake_case" in result.message, f"Expected snake_case violation, got {result.message}"