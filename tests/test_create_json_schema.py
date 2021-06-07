from kaiba.pydantic_schema import KaibaObject


def test_create_jsonschema_from_model():
    assert KaibaObject.schema_json(indent=2)
