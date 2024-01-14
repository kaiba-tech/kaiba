from returns.result import Result, Success
from returns.pointfree import bind

from kaiba.functions import apply_if_statements
from kaiba.models.if_statement import IfStatement



def test_something():
    # ifs = partial(apply_if_statements, statements=cfg.if_statements)

    """Test that 1 if (is) statement works."""
    test_value = 'target_value'
    if_statements = [
        IfStatement(**{
            'condition': 'is',
            'target': 'target_value',
            'then': 'value2',
        })
    ]
    # test2 = apply_if_statements(test_value, if_statements)
    # print(test2)
    # assert test2 == Success('value2')
    test = Result.do(
        apply_if_statements(a, if_statements)
        for a in Success(test_value)
    )

    assert test == 2
