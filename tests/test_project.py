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