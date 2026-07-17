# Testing

`pytest` is the de facto standard Python test runner: plain `assert`
statements, powerful fixtures for setup/teardown, and parametrization for
running one test body against many inputs.

## The basics

```python
# test_math_utils.py
def test_add():
    assert 2 + 2 == 4          # plain assert -- pytest rewrites it to show
                                 # both sides on failure, no assertTrue/assertEqual needed

def test_raises():
    import pytest
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

```bash
pytest                    # discovers test_*.py / *_test.py, runs test_* functions
pytest -v                 # verbose: one line per test
pytest test_math_utils.py::test_add   # run a single test
pytest -k "add"            # run tests whose name matches "add"
```

## Fixtures: reusable, composable setup

```python
import pytest

@pytest.fixture
def calculator():
    return Calculator()          # fresh instance for EVERY test that requests it

def test_add(calculator):
    assert calculator.add(2, 3) == 5

@pytest.fixture
def db_connection():
    conn = connect()
    yield conn                    # everything after yield is teardown
    conn.close()                   # runs after the test, pass or fail
```

Requesting a fixture by naming it as a test's parameter is how pytest wires
dependencies — no explicit setUp/tearDown class boilerplate required.

## Parametrize: one test body, many cases

```python
@pytest.mark.parametrize("n,expected", [
    (1, False),
    (2, True),
    (4, False),
    (17, True),
])
def test_is_prime(n, expected):
    assert is_prime(n) == expected
# pytest reports each case as a separate test result
```

## monkeypatch: safe, auto-reverted patching

```python
def test_reads_env_var(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    assert get_api_key() == "test-key"
    # automatically restored to the original value after this test --
    # no manual cleanup, even if the test fails

def test_mocked_time(monkeypatch):
    monkeypatch.setattr("time.time", lambda: 1000.0)
    assert current_timestamp() == 1000.0
```

## Mocking external dependencies

```python
from unittest.mock import Mock, patch

def test_calls_external_api():
    mock_client = Mock()
    mock_client.get.return_value = {"status": "ok"}
    result = check_status(mock_client)
    assert result == "ok"
    mock_client.get.assert_called_once_with("/status")

@patch("mymodule.requests.get")
def test_with_patch(mock_get):
    mock_get.return_value.json.return_value = {"id": 1}
    assert fetch_user_id() == 1
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Tests that depend on execution order | Pass in isolation, fail when run together (or in a different order) | Each test should set up its own state via fixtures, not rely on leftovers |
| Mutable fixture shared across tests without `yield` teardown | State leaks between tests | Use function-scoped fixtures (the default) unless sharing is deliberate |
| Mocking too much | Test passes even when the real integration is broken | Reserve mocks for genuinely external/slow dependencies; test real logic directly |
| Manually setting/restoring env vars or attributes | Cleanup skipped if the test fails before the restore line | Use `monkeypatch`, which reverts automatically regardless of outcome |
| Broad `except Exception` inside a test | Swallows the real assertion failure, test looks green | Let assertions and unexpected exceptions propagate; only catch what you're testing for |
