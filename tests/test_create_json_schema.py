from kaiba.models.kaiba_object import KaibaObject


def test_create_jsonschema_from_model():
    """Test that we can create jsonschema."""
    assert KaibaObject.schema_json(indent=2)
