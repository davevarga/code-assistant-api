import json
import os
import time
import tqdm
import pandas
import platform
from datasets import load_dataset

from agents import using_metadata, metadata
from agents import CodingAgent
from utils import CSVLogger, RepoHandler, context

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


# Configure run
solutions_path = os.getenv("RESULTS_LOG")
log_path = os.getenv("STATS_LOG")
cloning_path = './'

# Create files for logging
if not os.path.exists(solutions_path):
    solution_file = open(solutions_path, 'w', encoding='utf-8')
else:
    solution_file = open(solutions_path, 'a', encoding='utf-8')


def solve_task(
    task_id: str,
    description: str,
    agent: CodingAgent,
    repo: RepoHandler,
    logger: CSVLogger,
):
    # Check context manager
    context.set_root(cloning_path)
    assert context.get_root() != os.getcwd(), \
        f'Context is: {context.get_root()}'
    assert context.get_abs() == cloning_path, \
        f"Context management issue because {context.get_abs()} != {cloning_path}"
    assert context.get() == '.', \
        f"Context management issue: cwd is not root ({context.get()})"

    # Metadata for Phoenix phoenix details
    t_start = time.time()
    attempt_number = 1
    metadata['attempt_nr'] = attempt_number
    metadata['instance_id'] = task_id
    with using_metadata(metadata):
        diff, final_answer = agent.run(repo, description)

    # Agents sometime only solve problems in abstract term
    # Force agent to properly change the code.
    assert diff is not None, "Diff is none"
    while diff == '' and attempt_number <= 3:
        attempt_number += 1
        message = (
            "\n\n It seams that you didn't make any changes to the project. "
            "You should solve the github issue, with directly inserting the "
            "python code in according files. "
            "You should also test your code by using the run_python tool."
        )
        metadata['attempt_nr'] = attempt_number
        metadata['instance_id'] = task_id
        with using_metadata(metadata):
            prompt = description + final_answer + message
            diff, final_answer = agent.run(repo, prompt)

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
    logger.log('total_time', total_time)
    logger.log('attempts', attempt_number)

    return prediction



if __name__ == '__main__':
    # Suppose the files exist
    assert os.path.exists(solutions_path), 'Solutions file does not exist'
    assert os.path.exists(log_path), 'Log file does not exist'

    # Log in file specified by docker compose
    csv_logger = CSVLogger(log_path)

    # Download the dataset from Kaggle:
    dataset_url = 'princeton-nlp/SWE-bench_Lite'
    dataset = load_dataset(dataset_url, split='test')
    swebench = pandas.DataFrame(dataset)
    if platform.system() == "Windows":
        swebench['repo'] = swebench['repo'].apply(lambda x: x.replace('/', '\\'))

    # Create agent to solve the task
    coding_agent = CodingAgent(
        logger=csv_logger,
        add_base_tools=True,
        verbosity_level=0,
        max_steps=25,
        name='coding_agent',
    )
    # Helper clones every repository
    repo_handler = RepoHandler(
        root=cloning_path,
        logger=csv_logger,
    )

    for index, task in swebench.iterrows():
        # Step 1: Clone the repository
        repo_handler.clone(
            name=task['repo'],
            commit=task['base_commit']
        )
        # Step 2: Agents solves the task
        prediction = solve_task(
            agent=coding_agent,
            repo=repo_handler,
            task_id=task['instance_id'],
            description=task['problem_statement'],
            logger=csv_logger
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
