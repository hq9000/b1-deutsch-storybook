import os
import re
import shutil
import subprocess
import tempfile


def _replace_multiple_dashes(input_string: str) -> str:
    pattern = r'-+'
    result_string = re.sub(pattern, '-', input_string)
    return result_string

def _extract_chapter_number(input_file_path: str) -> int:
    pattern = re.compile(r'\d+')
    numbers = pattern.findall(input_file_path)
    return int(numbers[0])

def _get_processed_story_content(input_file_path) -> str:
    # Read the content of the input MD file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract the title from the first # or ## block
    match = re.search(r'#{1,2}\s+(.+?)(\n|$)', content)
    title = match.group(1) if match else "Untitled"

    title = title.replace("*", "")

    chapter_number = _extract_chapter_number(input_file_path) + 2

    # Find the first line starting with "# "
    lines = content.split('\n')
    filtered_lines = []
    for i, line in enumerate(lines):
        if line.startswith("# "):
            continue
        if "storybook ids" in line:
            continue
        line = _replace_multiple_dashes(line)
        filtered_lines.append(line)

    headline = f"# {chapter_number}. {title}"

    lines = [headline, *filtered_lines ]

    content = "\n".join(lines)

    # Add metadata to the content
    metadata = f"---\ntitle: {chapter_number}. {title}\nchapter: {chapter_number}\n---\n\n"

    return metadata + content

def get_combined_md_content(input_dir):

    with open("README.md", 'r', encoding='utf-8') as file:
        readme_content = file.read()


    global_title = None
    for line in readme_content.split("\n"):
        if line.startswith("# "):
            global_title = line

    assert global_title is not None

    combined_content = "\n".join([
        "\n",
        "---",
        f"title: {global_title.replace('# ', '')}",
        "date: 2023",
        "geometry: margin=2cm, landscape",
        "papersize: a4",
        "output: pdf_document",
        "---"
        "\n"
    ])

    readme_metadata =  "---\ntitle: Prephase\nchapter: 1\n---\n\n"

    combined_content += readme_metadata
    combined_content += readme_content

    # Iterate through all .md files in the input directory
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    for md_file in sorted(md_files):
        # if "000" not in md_file:
        #     continue
        input_file = os.path.join(input_dir, md_file)
        combined_content = combined_content + "\n\n" + "\\newpage" + "\n\n" +  _get_processed_story_content(input_file)

    return combined_content

if __name__ == "__main__":
    input_directory = "stories"
    output_directory = ".stories_preprocessed"

    combined_content = get_combined_md_content(input_directory)

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:

        shutil.copytree("stories/pictures", f"{temp_dir}/pictures")

        temp_file_path = os.path.join("", 'combined_content.md')
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(combined_content)

        # Define the command as a list of strings
        command = [
            "pandoc",
            temp_file_path,
            "-V",
            "mainfont=\"Liberation Serif\"",
            "-o",
            "b1-deutsch-ai-storybook-eng-rus.pdf"
        ]

        # Run the command
        try:
            subprocess.run(command, check=True)
            print("Conversion completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Conversion failed with error: {e}")


    print("Preprocessing completed.")
