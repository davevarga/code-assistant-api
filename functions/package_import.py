# Authorize import for CodeAct agent
import subprocess
import sys
from smolagents import tool
from smolagents import CodeAgent


@tool
def authorize_imports(agent: CodeAgent, package_name: str) -> str:
    """
    When an unauthorized import error occurs, use this function to download
    the package in the virtual environment, and authorize the agent to use
    the package
    Args:
        agent: The agent that called the tool, passes a reference to itself.
        package_name (str): The package to import.
    Returns:
        A string response if the package download was successful.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        agent.additional_authorized_imports.append(package_name)
        response = f"Package {package_name} was successfully imported."
    except subprocess.CalledProcessError:
        response = f"Package {package_name} could not be imported."
    return response
