import json
import os
import pandas
import platform
from datasets import load_dataset

from utils import CSVLogger, RepoHandler, ContextManager
from utils import RepoTaskSolver, RetryTaskTool
from agents import CodingAgent

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


# Configure run
solutions_path = os.getenv("RESULTS_LOG") if os.getenv("RESULTS_LOG") else './results'
log_path = os.getenv("STATS_LOG") if os.getenv("STATS_LOG") else './results'
root = os.getenv('REPO_ROOT') if os.getenv('REPO_ROOT') else './temp'


if __name__ == '__main__':
    # Suppose the files exist
    assert os.path.exists(solutions_path), 'Solutions file does not exist'
    assert os.path.exists(log_path), 'Log file does not exist'

    # Create files for logging
    if not os.path.exists(solutions_path):
        solution_file = open(solutions_path, 'w', encoding='utf-8')
    else:
        solution_file = open(solutions_path, 'a', encoding='utf-8')

    # Download the dataset from Kaggle:
    dataset_url = 'princeton-nlp/SWE-bench_Lite'
    dataset = load_dataset(dataset_url, split='test')
    swe_bench = pandas.DataFrame(dataset)
    if platform.system() == "Windows":
        swe_bench['repo'] = swe_bench['repo'].apply(lambda x: x.replace('/', '\\'))

    # Log in file specified by docker compose
    csv_logger = CSVLogger(log_path)

    # Context handler for agent guardrails
    context_handler = ContextManager(root)

    # Create agent to solve the task
    coding_agent = CodingAgent(
        context_handler,
        csv_logger,
        name='coding_agent',
        add_base_tools=True,
        verbosity_level=0,
        max_steps=25,
    )
    # Helper clones every repository
    repo_handler = RepoHandler(
        root=root,
        logger=csv_logger,
        context_handler=context_handler,
    )
    # Create solver object to solve problems
    problem_solver = RepoTaskSolver(
        agent=coding_agent,
        logger=csv_logger,
    )
    # Create retry tool for solver
    retry_tool = RetryTaskTool(
        solver=problem_solver,
    )
    coding_agent.insert_tool(retry_tool)

    # Each problem has its own solver, and therefore a separate context
    # Problems are independent, and therefore isolated by the ContextManager
    for index, task in swe_bench.iterrows():
        # Step 1: Clone the repository
        repo_handler.clone(
            name=task['repo'],
            commit=task['base_commit']
        )
        # Check context managers
        assert context_handler.get_root() == repo_handler.repo_path(), \
            (f'Context root is: {context_handler.get_root()} '
             f'instead of {repo_handler.repo_path()}')
        assert context_handler.get(abs=True) == repo_handler.repo_path(), \
            (f'Context initialization failed: {context_handler.get(abs=True)}'
             f' instead of {repo_handler.repo_path()}')

        # Step 2: Agents solves the task
        prediction = problem_solver.solve_repo_task(
            repo=repo_handler,
            task_id=task['instance_id'],
            description=task['problem_statement'],
        )
        # Check instance_id against solution
        assert prediction['instance_id'] == task['instance_id'], \
            (f"Missmatch in problem and solution identifiers: "
             f"{prediction['instance_id']} vs. {task['instance_id']}")

        # Step 3: Save the solution
        solution_json = json.dumps(prediction)
        solution_file.write(solution_json + '\n')
        csv_logger.log('id', task['instance_id'])
        csv_logger.save()
        break

    solution_file.close()
