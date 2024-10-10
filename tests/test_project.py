import pytest
from src.rules import has_mandatory_metadata

def test_has_mandatory_metadata():
    model = {
        'name': 'test_model',
        'columns': {'id': {'description': 'Identifier'}},
        'tags': []
    }
    assert isinstance(has_mandatory_metadata(model), type(None)), "Expected no violations when metadata is valid"