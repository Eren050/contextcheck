from pathlib import Path
import pytest
from contextcheck import TestScenario
from contextcheck.endpoints.endpoint_config import EndpointConfig
from contextcheck.endpoints.endpoint_dummy_echo import EndpointDummyEcho
from contextcheck.executors.executor import Executor
from tests.utils import executor


def test_load_scenario_from_yaml():
    ts = TestScenario.from_yaml(Path("tests/scenario_echo.yaml"))
    assert isinstance(ts.config.endpoint_under_test, EndpointConfig)
    assert ts.config.endpoint_under_test.kind == "echo"
    assert ts.config.default_request.chat_uuid == "0xdead"
    assert len(ts.steps) == 6
    assert ts.steps[0].request.message == "Write success in the response"
    assert ts.steps[0].request.chat_uuid == "0xdead"
    assert ts.steps[0].name == "Write success in the response"
    assert ts.steps[1].request.message == "Hello!"
    assert ts.steps[1].request.chat_uuid == "0x00"
    assert ts.steps[1].name == "Send request with additional fields, including variable"
    assert len(ts.steps[2].asserts) == 3
    assert ts.steps[2].asserts[0].eval == "True == True"
    assert ts.steps[2].asserts[1].eval == 'response.message == "Hello!"'
    assert ts.steps[2].asserts[2].eval == 'response.chat_uuid == "0x11"'


def test_run():
    ts = TestScenario.from_yaml(Path("tests/scenario_echo.yaml"))
    executor = Executor(ts)
    assert isinstance(executor.endpoint_under_test, EndpointDummyEcho)
    assert executor.test_scenario.result is None
    for step in executor.test_scenario.steps:
        assert step.result is None
        assert step.response is None
    executor.run_all()
    ts = executor.test_scenario

    assert ts.result is not None
    assert ts.result is False

    for step in ts.steps:
        assert step.result is not None
        assert step.response is not None

    assert ts.steps[0].response.message == "Write success in the response"

    assert ts.steps[1].response.message == "Hello!"
    assert ts.steps[1].response.chat_uuid == "0x00"

    assert ts.steps[2].asserts[0].result is True
    assert ts.steps[2].asserts[1].result is False

    assert ts.steps[0].response.stats is not None
    assert ts.steps[0].response.stats.tokens_total is None

    # Test fields eval:
    assert ts.steps[3].response.chat_uuid == "0x11"
    assert ts.steps[3].response.message == "Here is previous chat_uuid"
    assert ts.steps[3].result is True
    assert ts.steps[3].response.asr_build["some_field1"] == "field1"
    assert ts.steps[3].response.asr_build["some_field3"] == 4

    # Wrong evals:
    assert ts.steps[4].asserts[0].result is None
    assert ts.steps[4].asserts[1].result is None
    assert ts.steps[4].asserts[2].result is None
    assert ts.steps[4].result is False

    # JSON parsing
    assert all(a.result for a in ts.steps[5].asserts)


config_parsing_as_string = """
config:
    endpoint_under_test:
        kind: echo

steps:
  - name: test parsing as json
    request: '{"Hello": "World"}'
"""


@pytest.mark.parametrize("executor", [config_parsing_as_string], indirect=True)
def test_parsing_as_string(executor):
    executor.run_all()
    assert executor.test_scenario.steps[0].response.message == '{"Hello": "World"}'


config_parsing_as_json_2 = """
config:
    endpoint_under_test:
        kind: echo
    default_request:
        parse_response_as_json: true        

steps:
  - name: test parsing as json
    request: '{"Hello": "World"}'
"""


@pytest.mark.parametrize("executor", [config_parsing_as_json_2], indirect=True)
def test_failing_parsing_as_json(executor):
    with pytest.raises(
        ValueError, match="You see this error because of incorrect response parsing"
    ):
        executor.run_all()
