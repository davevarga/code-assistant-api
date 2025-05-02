from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from openinference.instrumentation import using_metadata

from .agents import CodingAgent

register(
    project_name="LLMCodeAct-Lite",
    endpoint="http://localhost:6006/v1/traces",
)
SmolagentsInstrumentor().instrument()

# Define metadata for agent Phoenix logs
metadata = {
    'instance_id': "default",
    'attempt_nr': 0,
    'model': 'gpt-4o-mini'
}