"""A small interactive shell: builtins, quoting, and external commands."""

import os
import shlex
import shutil
import subprocess
import sys

BUILTINS = ("echo", "exit", "type", "pwd", "cd")


def execute(line):
    """Execute one command; return True if the shell should exit."""
    try:
        args = shlex.split(line)
    except ValueError as error:
        print(f"shell: {error}")
        return False
    if not args:
        return False
    command, *arguments = args
    if command == "exit":
        if not arguments or arguments == ["0"]:
            return True
        print("exit: only exit 0 is supported")
    elif command == "echo":
        print(" ".join(arguments))
    elif command == "pwd":
        print(os.getcwd())
    elif command == "cd":
        destination = os.path.expanduser(arguments[0]) if arguments else os.path.expanduser("~")
        if len(arguments) > 1:
            print("cd: too many arguments")
            return False
        try:
            os.chdir(destination)
        except OSError as error:
            print(f"cd: {destination}: {error.strerror}")
    elif command == "type":
        if not arguments:
            print("type: missing command")
        else:
            for name in arguments:
                if name in BUILTINS:
                    print(f"{name} is a shell builtin")
                else:
                    found = shutil.which(name)
                    print(f"{name} is {found}" if found else f"{name}: not found")
    else:
        found = shutil.which(command)
        if not found:
            print(f"{command}: command not found")
        else:
            try:
                subprocess.run([found, *arguments], check=False)
            except OSError as error:
                print(f"{command}: {error.strerror}")
    return False


def main():
    while True:
        try:
            line = input("$ ")
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            continue
        if execute(line):
            break


if __name__ == "__main__":
    main()
