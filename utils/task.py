import subprocess


def execute_task_background(command: str, directory: str) -> None:
    process = subprocess.run(
        f"./{command}", stdout=subprocess.PIPE, cwd=directory)

    if process.stdout is not None:
        result = [r for r in str(
            process.stdout, 'UTF-8', errors="backslashreplace").split("\n") if r]

        print(result)
