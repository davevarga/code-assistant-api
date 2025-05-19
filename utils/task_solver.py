import time
from smolagents import Tool
from utils import CSVLogger, RepoHandler
from agents import CodingAgent
from agents import metadata


class RepoTaskSolver(object):
    diagnosis_instruction = (
        f"DIAGNOSIS:\n\n"
        f" Your task is to identify the root cause of the issue described above."
        f" Search through the relevant parts of the project, inspect the control flow,"
        f" verify assumptions, and reason about how the existing code behaves."
        f" Try to reproduce the issue by simulating or running the affected logic."
        f" Focus on understanding why the described problem happens, not yet how to"
        f" fix it. Document what you believe causes the problem, citing specific"
        f" files, lines of code, or behaviors. If possible, describe how to"
        f" consistently trigger the issue."
    )
    fixing_instruction = (
        f"SOLUTION:\n\n"
        f" Based on your diagnosis above, implement a fix for the identified issue."
        f" Modify only the necessary parts of the code to resolve the root cause."
        f" Ensure that the original problem no longer occurs and that all existing"
        f" functionality remains intact. Keep your changes minimal and consistent"
        f" with the codebase’s style. If the fix involves modifying logic, updating"
        f" interfaces, or handling edge cases, make sure those are thoroughly"
        f" addressed. After applying the fix, include a short note explaining what"
        f" was changed and why."
    )
    testing_instruction = (
        f"TEST:\n\n"
        f" Now test the code to verify that the issue has been successfully fixed."
        f" Reproduce the original scenario where the problem occurred, and confirm"
        f" that the expected behavior now takes place. Additionally, test the"
        f" modified code with a variety of inputs, including edge cases,"
        f" to ensure that the solution is robust and does not introduce regressions."
        f" If the issue still persists or if unexpected behavior is discovered,"
        f" use the retry tool to return to the fixing phase and attempt a corrected"
        f" solution based on this new insight."
    )
    def __init__(self, agent: CodingAgent, logger: CSVLogger):
        self.agent = agent
        self.logger = logger
        self.retry = False

    def solve_repo_task(self, repo: RepoHandler, task_id: str, description: str):
        # Metadata for Phoenix phoenix details
        t_start = time.time()
        attempt_number = 1
        self.retry = False
        metadata['attempt_nr'] = attempt_number
        metadata['instance_id'] = task_id

        # Instruct the agent to make changes in the repository
        # in order to solve the problem.
        prompt = '\n'.join([description, '\n', RepoTaskSolver.diagnosis_instruction])
        metadata['phase'] = 'diagnosis'
        _, diagnosis = self.agent.run(repo, prompt, metadata)

        while True:
            # Solve the problem diagnosed previously
            # This will be the diff file that is returned
            prompt = '\n'.join([description, diagnosis, RepoTaskSolver.fixing_instruction])
            metadata['phase'] = 'fixing'
            diff, changes_made = self.agent.run(repo, prompt, metadata)

            # Test if the changes are correct.
            # Don't include the changes from the test
            # Todo: discard changes from the last testing phase.
            prompt = '\n'.join([description, changes_made, RepoTaskSolver.testing_instruction])
            metadata['phase'] = 'testing'
            _, test_result = self.agent.run(repo, prompt, metadata)

            # Replaces back testing cycles
            if not self.retry or attempt_number > 1: break
            attempt_number += 1
            metadata['attempt_nr'] = attempt_number
            self.retry = False

        # Create the json object
        prediction = {
            "instance_id": task_id,
            "model": "gpt-4o-mini",
            "prediction": diff
        }
        # Delete repository and log
        repo.delete()
        t_end = time.time()
        total_time = t_end - t_start
        self.logger.log('total_time', total_time)
        self.logger.log('attempts', attempt_number)

        self.agent.reset()
        return prediction

    def retry_repo_task(self):
        self.retry = True


class RetryTaskTool(Tool):
    name = "retry_task"
    description = """Used when you reached your final step. After testing,
        it appears that the issue remains unresolved. To proceed,
        carefully review the test results and ensure your solution
        addresses the problem. If necessary, modify the Python code
        in the relevant files and test again using the `run_python` tool.
        Once you are confident the issue is fixed, use the retry tool to
        attempt the solution once more."""
    inputs = {}
    output_type = "string"

    def __init__(self, solver: RepoTaskSolver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.solver = solver

    def forward(self) -> str:
        self.solver.retry_repo_task()
        return (
            """The retry tool has been activated, and a new attempt will be made
             to resolve the issue. The previous solution did not work, as testing
              confirmed that the expected behavior was not achieved. This may be
               due to an incomplete fix or incorrect modifications. 

            For this new attempt, review the issue carefully, ensure all parts
             of the code are addressed, and test the changes using the `run_python`
              tool. If the issue persists, further adjustments may be needed."""
        )


