# Custom Shell Script

This is a simple Python-based shell implementation that mimics basic shell commands like `echo`, `exit`, `type`, `pwd`, and `cd`. It also allows running commands found in the system's `PATH`.

## Features

- **Custom Commands**:
  - `echo [text]`: Prints the specified text to the console.
  - `exit 0`: Exits the shell.
  - `type [command]`: Checks if the command is a shell builtin or available in the system `PATH`.
  - `pwd`: Prints the current working directory.
  - `cd [directory]`: Changes the current directory.

- **System Commands**: If the command entered is not a custom command, the script searches for it in the system's `PATH` and executes it if found.

## Functions

### `list_all_directories(searcg)`

- **Purpose**: Recursively traverses the directory tree starting from the root (`/`) and checks if the specified directory exists.
- **Parameters**:
  - `searcg` (str): The directory to search for.
- **Returns**: `1` if the directory is found, `0` otherwise.
- **Exceptions**: Catches and handles `PermissionError` and other general exceptions.

### `find_command_in_path(command)`

- **Purpose**: Searches for a command in the system's `PATH`.
- **Parameters**:
  - `command` (str): The command to search for.
- **Returns**: The full path to the command if found, `None` otherwise.

### `main()`

- **Purpose**: The main loop of the shell, continuously prompts the user for input and executes the appropriate command based on the input.
- **Commands**:
  - `type [command]`
  - `echo [text]`
  - `exit 0`
  - `pwd`
  - `cd [directory]`
  - System commands (if found in `PATH`)

## Usage

To use this script, simply run it with Python:

```bash
python3 shell.py
