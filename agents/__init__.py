from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

from .agents import CodingAgent, LiteLLMAgent
from dotenv import load_dotenv
import os

load_dotenv()

register(
    project_name="LLMCodeAct-Lite",
    endpoint=os.getenv("PHOENIX_COLLECTOR_ENDPOINT"),
    batch=True, # uses a batch span processor
)
SmolagentsInstrumentor().instrument()

# Define metadata for agent Phoenix logs
metadata = {
    'instance_id': "default",
    'attempt_nr': 0,
    'model': 'gpt-4o-mini'
}