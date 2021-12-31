from kaiba.functions import apply_if_statements
from kaiba.models.if_statement import IfStatement


def test_if_is():
    """Test that 1 if (is) statement works."""
    statements = [
        IfStatement(**{
            'condition': 'is',
            'target': 'target_value',
            'then': 'value2',
        }),
    ]

    assert apply_if_statements(
        'target_value',
        statements,
    ) == 'value2'


def test_if_is_condition_false():
    """Test if condition False."""
    statements = [
        IfStatement(**{
            'condition': 'is',
            'target': 'target_value',
            'then': 'value2',
        }),
    ]

    assert apply_if_statements(
        'not_target_value',
        statements,
    ) == 'not_target_value'


def test_if_is_condition_array_value():
    """Test that we can do if is statement on arrays."""
    statements = [
        IfStatement(**{
            'condition': 'is',
            'target': ['target_value'],
            'then': 'value2',
        }),
    ]

    assert apply_if_statements(
        ['target_value'],
        statements,
    ) == 'value2'


def test_if_is_condition_objects_value():
    """Test that we can do if is statement on objectss."""
    statements = [
        IfStatement(**{
            'condition': 'is',
            'target': {'val': 'target'},
            'then': 'value2',
        }),
    ]
    assert apply_if_statements(
        {'val': 'target'},
        statements,
    ) == 'value2'


def test_if_in():
    """Test that 1 if (in) statement works."""
    statements = [
        IfStatement(**{
            'condition': 'in',
            'target': ['target_value'],
            'then': 'value2',
        }),
    ]
    assert apply_if_statements(
        'target_value',
        statements,
    ) == 'value2'


def test_if_in_condition_false():
    """Test if in condition False."""
    statements = [
        IfStatement(**{
            'condition': 'in',
            'target': 'target_value',
            'then': 'value2',
        }),
    ]

    assert apply_if_statements(
        'not_target_value',
        statements,
    ) == 'not_target_value'


def test_if_in_condition_array_value():
    """Test that we can do if in statement on arrays."""
    statements = [
        IfStatement(**{
            'condition': 'in',
            'target': [['target_value']],
            'then': 'value2',
        }),
    ]

    assert apply_if_statements(
        ['target_value'],
        statements,
    ) == 'value2'


def test_if_in_condition_objects_value():
    """Test that we can do if is statement on objectss."""
    statements = [
        IfStatement(**{
            'condition': 'in',
            'target': [{'val': 'target'}],
            'then': 'value2',
        }),
    ]

    assert apply_if_statements(
        {'val': 'target'},
        statements,
    ) == 'value2'


def test_if_not():
    """Test that 1 if (not) statement works."""
    statements = [
        IfStatement(**{
            'condition': 'not',
            'target': 'not_target',
            'then': 'value2',
        }),
    ]

    assert apply_if_statements(
        'target_value',
        statements,
    ) == 'value2'


def test_if_not_condition_false():
    """Test if not condition False."""
    statements = [
        IfStatement(**{
            'condition': 'not',
            'target': 'target_value',
            'then': 'value2',
        }),
    ]

    assert apply_if_statements(
        'target_value',
        statements,
    ) == 'target_value'


def test_if_not_condition_array_value():
    """Test that we can do if not statement on arrays."""
    statements = [
        IfStatement(**{
            'condition': 'not',
            'target': ['not_target'],
            'then': 'value2',
        }),
    ]

    assert apply_if_statements(
        ['target_value'],
        statements,
    ) == 'value2'


def test_if_not_condition_array_value_with_int():
    """Test that we can do if not statement on arrays."""
    statements = [
        IfStatement(**{
            'condition': 'is',
            'target': [123],
            'then': 'value2',
        }),
    ]

    assert apply_if_statements(
        [123],
        statements,
    ) == 'value2'


def test_if_not_condition_objects_value():
    """Test that we can do if not statement on objectss."""
    statements = [
        IfStatement(**{
            'condition': 'not',
            'target': {'val': 'tarnot'},
            'then': 'value2',
        }),
    ]
    assert apply_if_statements(
        {'val': 'target'},
        statements,
    ) == 'value2'


def test_if_contains():
    """Test that 1 if (contains) statement works."""
    statements = [
        IfStatement(**{
            'condition': 'contains',
            'target': '_value',
            'then': 'value2',
        }),
    ]
    assert apply_if_statements(
        'target_value',
        statements,
    ) == 'value2'


def test_if_contains_condition_false():
    """Test if contains condition False."""
    statements = [
        IfStatement(**{
            'condition': 'contains',
            'target': 'does_not_contain',
            'then': 'value2',
        }),
    ]
    assert apply_if_statements(
        'not_target_value',
        statements,
    ) == 'not_target_value'


def test_if_contains_condition_array_value():
    """Test that we can do if contains statement on arrays."""
    statements = [
        IfStatement(**{
            'condition': 'contains',
            'target': 'target',
            'then': 'value2',
        }),
    ]
    assert apply_if_statements(
        ['value', 'target'],
        statements,
    ) == 'value2'


def test_if_contains_condition_objects_value():
    """Test that we can do if contains statement on objectss."""
    statements = [
        IfStatement(**{
            'condition': 'contains',
            'target': 'val',
            'then': 'value2',
        }),
    ]
    assert apply_if_statements(
        {'val': 'target'},
        statements,
    ) == 'value2'


def test_if_contains_objects_in_array_value():
    """Test that we can do if contains statement on objectss."""
    statements = [
        IfStatement(**{
            'condition': 'contains',
            'target': {'val': 'target'},
            'then': 'value2',
        }),
    ]
    assert apply_if_statements(
        [{'val': 'target'}],
        statements,
    ) == 'value2'


def test_if_contains_array_does_not_stringify():
    """Test that we can do if contains statement on array[objects].

    However its very important that list and object tests does not do
    string casting for check since it would give the check two possible
    ways to do the check and there should only be one.
    for objects the 'in' checks if the key exist
    for arrays the 'in' checks if the element exist inside the array
    for everything else we will stringify the test value.
    """
    statements = [
        IfStatement(**{
            'condition': 'contains',
            'target': 'target',
            'then': 'value2',
        }),
    ]
    assert apply_if_statements(
        [{'val': 'target'}],
        statements,
    ) == [{'val': 'target'}]


def test_if_contains_works_with_non_strings():
    """Test that we can do if contains statement on objectss."""
    statements = [
        IfStatement(**{
            'condition': 'contains',
            'target': 123,
            'then': 'value2',
        }),
    ]
    assert apply_if_statements(
        123,
        statements,
    ) == 'value2'


def test_if_chained():
    """Test that two if (is) statement works."""
    statements = [
        IfStatement(**{
            'condition': 'is',
            'target': 'target_value',
            'then': 'value2',
        }),
        IfStatement(**{
            'condition': 'is',
            'target': 'value2',
            'then': 'value3',
        }),
    ]
    assert apply_if_statements(
        'target_value',
        statements,
    ) == 'value3'


def test_if_failed_condition_goes_to_otherwise():
    """Test that we get the then value when condition fails."""
    statements = [
        IfStatement(**{
            'condition': 'is',
            'target': 'target_value',
            'then': 'no',
            'otherwise': 'yes',
        }),
    ]
    assert apply_if_statements(
        'not_target_value',
        statements,
    ) == 'yes'
