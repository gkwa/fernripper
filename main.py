import argparse
import pathlib
import re
import subprocess
import tqdm


def check_already_split(input_dir):
    output_files = list(input_dir.glob("*.txt"))
    return len(output_files) > 0


def split_file_by_regex(input_file, regex_pattern):
    with input_file.open("r") as f:
        content = f.read()

    splits = re.split(regex_pattern, content, flags=re.MULTILINE)
    splits = [s.strip() for s in splits if s.strip()]

    output_dir = pathlib.Path("output")
    output_dir.mkdir(exist_ok=True)

    total_splits = len(splits)  # Total number of splits
    split_progress = tqdm.tqdm(total=total_splits, desc="Splitting")  # Progress bar
    for index, split in enumerate(splits, start=1):
        output_file = output_dir / f"{index:09d}.txt"
        with output_file.open("w") as f:
            f.write(split)
        split_progress.update(1)  # Update progress bar

    split_progress.close()  # Close progress bar


def process_files_with_go_org(input_dir, processed_files_set):
    input_files = list(input_dir.iterdir())
    total_files = len(input_files)  # Total number of input files
    process_progress = tqdm.tqdm(total=total_files, desc="Processing")  # Progress bar
    for index, input_file in enumerate(input_files, start=1):
        if input_file.is_file() and input_file.suffix == ".txt":
            output_file_stdout = f"{input_file.stem}_stdout.txt"
            output_file_stderr = f"{input_file.stem}_stderr.txt"

            if (
                output_file_stdout not in processed_files_set
                and output_file_stderr not in processed_files_set
            ):
                command = ["go-org", "render", str(input_file), "org"]
                with open(output_file_stdout, "w") as stdout_file, open(
                    output_file_stderr, "w"
                ) as stderr_file:
                    subprocess.run(command, stdout=stdout_file, stderr=stderr_file)

                processed_files_set.add(output_file_stdout)
                processed_files_set.add(output_file_stderr)

                with open("processed_files.txt", "a") as f:
                    f.write(f"{output_file_stdout}\n")
                    f.write(f"{output_file_stderr}\n")

        process_progress.update(1)  # Update progress bar

    process_progress.close()  # Close progress bar


def main():
    parser = argparse.ArgumentParser(description="Split file by regex pattern")
    parser.add_argument("input_file", type=pathlib.Path, help="Input file path")
    parser.add_argument("regex_pattern", type=str, help="Regex pattern for splitting")
    args = parser.parse_args()

    input_file_name = args.input_file.name
    processed_files_set = set()

    try:
        with open("processed_files.txt", "r") as f:
            processed_files_set = set(f.read().splitlines())
    except FileNotFoundError:
        pass

    if check_already_split(pathlib.Path("output")):
        print("File already split. Skipping splitting phase.")
    else:
        split_file_by_regex(args.input_file, args.regex_pattern)

    process_files_with_go_org(pathlib.Path("output"), processed_files_set)


if __name__ == "__main__":
    main()
