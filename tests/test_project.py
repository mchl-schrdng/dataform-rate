import pytest
from src.rules import *

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
    valid_model = {'name': 'valid_model', 'columns': {'valid_column': 'Valid description'}}
    assert naming_conventions(valid_model) is None

    invalid_model = {'name': 'InvalidModel', 'columns': {'InvalidColumn': 'Description'}}
    result = naming_conventions(invalid_model)
    assert isinstance(result, RuleViolation)
    assert "snake_case" in result.message

def test_columns_have_descriptions():
    model = {
        'name': 'test_model',
        'columns': {
            'id': 'Identifier',
            'name': ''
        }
    }
    result = columns_have_descriptions(model)
    assert isinstance(result, RuleViolation)
    assert "Columns missing descriptions" in result.message

def test_has_partitioning():
    model = {'name': 'test_model'}
    result = has_partitioning(model)
    assert isinstance(result, RuleViolation)
    assert "missing partitioning information" in result.message

    partitioned_model = {'name': 'test_model', 'partition_by': 'order_date'}
    assert has_partitioning(partitioned_model) is None

def test_has_any_labels():
    model = {'name': 'test_model'}
    result = has_any_labels(model)
    assert isinstance(result, RuleViolation)
    assert "No labels found" in result.message

    labeled_model = {'name': 'test_model', 'labels': {'label1': 'value1'}}
    assert has_any_labels(labeled_model) is None

def test_avoid_select_star():
    model = {'name': 'test_model', 'sql': 'SELECT * FROM orders'}
    result = avoid_select_star(model)
    assert isinstance(result, RuleViolation)
    assert "Avoid using SELECT *" in result.message

    specific_select_model = {'name': 'test_model', 'sql': 'SELECT order_id FROM orders'}
    assert avoid_select_star(specific_select_model) is None

def test_sql_line_limit():
    model = {'sql': '\n'.join([f"Line {i}" for i in range(201)])}
    result = sql_line_limit(model)
    assert isinstance(result, RuleViolation)
    assert "SQL exceeds 200 lines" in result.message

    short_model = {'sql': '\n'.join([f"Line {i}" for i in range(199)])}
    assert sql_line_limit(short_model) is None

def test_comprehensive_column_descriptions():
    model = {
        'name': 'test_model',
        'columns': {
            'id': 'ID',
            'description': 'This is a proper description with more than five words'
        }
    }
    result = comprehensive_column_descriptions(model)
    assert isinstance(result, RuleViolation)
    assert "Column 'id' has a description that is too short" in result.message

    valid_model = {'name': 'test_model', 'columns': {'id': 'This is a detailed description for the id column'}}
    assert comprehensive_column_descriptions(valid_model) is None

def test_avoid_hardcoded_values():
    model = {'sql': 'SELECT * FROM orders WHERE order_id = 123'}
    result = avoid_hardcoded_values(model)
    assert isinstance(result, RuleViolation)
    assert "Avoid using hardcoded numeric values" in result.message

    valid_model = {'sql': 'SELECT * FROM orders WHERE order_id = ?'}
    assert avoid_hardcoded_values(valid_model) is None