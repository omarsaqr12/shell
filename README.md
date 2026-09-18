# Python mini-shell

An interactive, **educational shell implementation** developed in the [CodeCrafters shell challenge](https://codecrafters.io/challenges/shell/overview). It implements five builtins, PATH-based external command execution, quoted arguments, and working-directory changes. It is not a POSIX shell or a replacement for Bash.

## Quickstart

Requires Python 3.12 or later. From the repository root:

```bash
cd codecrafters-shell-python
python3 -m app.main
```

Example interactive session (the `$` lines are prompts):

```text
$ type echo
echo is a shell builtin
$ echo 'two words'
two words
$ pwd
/path/to/codecrafters-shell-python
$ cd ..
$ exit 0
```

The launcher `sh your_program.sh` uses Pipenv and requires `pipenv` to be installed. Invoke it with `sh` because the original file is not tracked with executable permission. Direct `python3 -m app.main` execution requires no third-party runtime packages.

## Implemented behavior

| Command | Behavior |
| --- | --- |
| `echo` | Prints arguments after shell-like quote/backslash tokenization. |
| `type` | Reports builtins or the first executable found on `PATH`. |
| `pwd` | Prints the process working directory. |
| `cd` | Uses `os.chdir` for absolute, relative, and `~` paths; no argument means home. |
| `exit 0` | Stops the loop (`exit` without arguments also stops). |
| Other commands | Finds an executable on `PATH` and runs it with an argument list, **without** `shell=True`. |

Unlike a full shell, this implementation does **not** interpret pipes, redirects, background jobs, variables, command substitution, globbing, or compound expressions. Nonzero child exit codes do not stop the interactive loop. Errors in quotes or `cd` are reported instead of crashing the shell.

## Architecture and verification

- [`codecrafters-shell-python/app/main.py`](codecrafters-shell-python/app/main.py): tokenize input, dispatch builtins, resolve PATH, and run external processes.
- [`codecrafters-shell-python/tests/test_shell.py`](codecrafters-shell-python/tests/test_shell.py): builtin tests plus real child-process and EOF tests.
- [`REVIEW_NOTES.md`](REVIEW_NOTES.md): repository coverage, defects, verification, and limitations.

Run tests from `codecrafters-shell-python`:

```bash
python3 -m unittest discover -s tests -v
```

The original project comes from a CodeCrafters exercise. Check commit history for individual contribution provenance. There is no license file, so this README does not assert a license. These local tests are not a claimed result from CodeCrafters' grading suite.
