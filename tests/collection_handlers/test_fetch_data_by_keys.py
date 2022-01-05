from kaiba.collection_handlers import fetch_data_by_keys


def test():
    """Test that we can fetch key in dict."""
    assert fetch_data_by_keys(
        {'key': 'val1'},
        ['key'],
    ) == 'val1'


def test_two_keys():
    """Test that we are able to map with multiple keys."""
    assert fetch_data_by_keys(
        {'key1': {'key2': 'val1'}},
        ['key1', 'key2'],
    ) == 'val1'


def test_find_dictionary():
    """Test that giving path to dict is okay."""
    assert fetch_data_by_keys(
        {'key': {'key1': 'val'}},
        ['key'],
    ) == {'key1': 'val'}


def test_find_array():
    """Test that giving path to array is okay."""
    assert fetch_data_by_keys(
        {'key': ['val', 'val']},
        ['key'],
    ) == ['val', 'val']


def test_no_such_key():
    """Test Failure on missing key."""
    t_result = fetch_data_by_keys(
        {'key': 'val1'},
        ['missing'],
    )
    assert t_result is None


def test_no_path():
    """Test no path should return Failure."""
    t_result = fetch_data_by_keys(
        {'key': 'val'},
        [],
    )
    assert t_result is None


def test_no_data():
    """Test no data should return Failure."""
    t_result = fetch_data_by_keys(
        {},
        ['keys'],
    )
    assert t_result is None
