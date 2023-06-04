import re
import datetime
import typer

# Regular expression patterns
PRIORITY_PATTERN = r'\(([A-Z])\)'
PROJECT_TAG_PATTERN = r'\+(\w+)'
CONTEXT_TAG_PATTERN = r'@(\w+)'
DUE_DATE_PATTERN = r'd(\d{4}—\d{2}—\d{2})'

# Todo.txt file location
DB_FILE = "db.todo.txt"
SYNCED_FILE = "todo.txt"

# Function to extract the priority from the input string
def extract_priority(input_string):
    match = re.search(PRIORITY_PATTERN, input_string)
    if match:
        priority = match.group(1)
        return priority
    return None

# Function to extract the project tags from the input string
def extract_project_tags(input_string):
    tags = re.findall(PROJECT_TAG_PATTERN, input_string)
    return tags

# Function to extract the context tags from the input string
def extract_context_tags(input_string):
    tags = re.findall(CONTEXT_TAG_PATTERN, input_string)
    return tags

# Function to extract the due date from the input string
def extract_due_date(input_string):
    match = re.search(DUE_DATE_PATTERN, input_string)
    if match:
        due_date = match.group(1)
        return due_date
    return None

# Function to format the entry
def format_entry(input_string):
    priority = extract_priority(input_string)
    creation_date = datetime.datetime.now().strftime('%Y—%m—%d')
    completion_date = None  # Not provided in the input string
    todo_entry = re.sub(PRIORITY_PATTERN, '', input_string).strip()
    project_tags = extract_project_tags(input_string)
    context_tags = extract_context_tags(input_string)
    due_date = extract_due_date(input_string)

    formatted_entry = {
        'priority': priority,
        'todo_entry': todo_entry,
        'project_tags': project_tags,
        'context_tags': context_tags,
        'creation_date': creation_date,
        'completion_date': completion_date,
        'due_date': due_date
    }

    return formatted_entry

# Function to save the entry to todo.txt
def save_entry(entry, file_path):
    tempData = None
    with open(file_path, 'r') as file:
        tempData = file.read()
    with open(file_path, 'w') as file:
        file.write(str(entry))
        file.write('\n' + tempData)

# Function to load entries from todo.txt
def load_entries(file_path):
    entries = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if(file_path is SYNCED_FILE):
                entries.append(line)
            else:
                entry = eval(line.strip())
                entries.append(entry)
    return entries

# Clear a file
def clear_todos(file_path):
    with open(file_path, 'w') as file:
        file.truncate()

# Create a Typer app
app = typer.Typer()

@app.command()
def todo(
    entry: str
):
    # Format and save the entry
    save_entry(entry,SYNCED_FILE)
    formatted_entry = format_entry(entry)
    save_entry(formatted_entry,DB_FILE)
    typer.echo(entry)

@app.command()
def list():
    # Show all entries in human readable form
    entries = load_entries(SYNCED_FILE)
    typer.echo(f"Total entries {len(entries)}")
    for entry in entries:
        typer.echo(entry)

@app.command()
def debug(
    clear: bool = typer.Option(False, '--clear')
):
    if clear:
        clear_todos(DB_FILE)
        clear_todos(SYNCED_FILE)

    entries = load_entries(DB_FILE)
    typer.echo(f"Total entries {len(entries)}")
    for entry in entries:
        typer.echo(entry)


# Run the Typer app
if __name__ == '__main__':
    app()

