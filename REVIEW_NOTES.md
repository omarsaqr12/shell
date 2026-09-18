# Engineering review / handoff — shell

## Identity and baseline

- Repository: `omarsaqr12/shell`, default branch `main`.
- Baseline commit: `63685e6d9e8016206c397be4351ce408fc9963da` (read through the connected GitHub API; default branch not edited).
- Category: CodeCrafters educational interactive command interpreter, not a POSIX shell.
- Evidence standard: verify tokenization, builtin dispatch, filesystem behavior, PATH resolution, external process execution, and EOF handling; compare expected behavior with the Python 3.12 `shlex` and `subprocess` documentation.

## Baseline inventory and file coverage

All **eight** tracked files were read in full: root `README.md`; nested `Pipfile`, `Pipfile.lock`, `README.md`, `app/main.py`, `app/tempCodeRunnerFile.py`, `codecrafters.yml`, and `your_program.sh`. No tracked binary/vendor or experiment results were present. The four-byte `app/tempCodeRunnerFile.py` contains only `type`; left unchanged to preserve historical material. The CodeCrafters files remain untouched. The launcher has no executable bit; invoke with `sh your_program.sh` after installing Pipenv. No independent grader score or contribution breakdown was available.

## Confirmed baseline problems (source review)

1. **Directory lookup:** `list_all_directories` recursively walks `/` on every `cd`, which is expensive and fails for inaccessible paths, symlinks, and edge cases. Indexing `s[3]` causes an exception for input `cd`.
2. **Faulty directory resolution:** hand-assembled relative paths mishandle some `..` and `~` cases instead of allowing the OS to resolve them.
3. **Tokenization:** `split(' ')` cannot preserve quoted filenames and arguments; prefix-based `startswith` checks misclassify commands such as `echofoo` or `typewriter`.
4. **Process errors:** `subprocess.run(check=True)` raises on ordinary nonzero child exit codes and can terminate the shell.
5. **Reproducibility / claims:** both READMEs instruct `python3 shell.py`, but no such tracked file exists; the root README has an unterminated code fence; neither repository has tracked tests.

## Changes and verification

- Used `shlex.split` for shell-like argument parsing and exact builtin command matching.
- Used `os.chdir` plus `expanduser` for directory changes and `shutil.which` for PATH lookup.
- Executed external programs with an argument vector (no `shell=True`); child nonzero exits no longer crash the prompt.
- Handled malformed quotes and EOF; documented unsupported POSIX features and correct command paths.
- Added real-subprocess and builtin regression tests, plus lightweight GitHub Actions test workflow for Python 3.12.

Local verification: from `codecrafters-shell-python`, run `python3 -m unittest discover -s tests -v` and `python3 -m py_compile app/main.py tests/test_shell.py`. Tests exercise real child processes, nonzero exit continuity, quoted arguments, relative/absolute/home directory changes, and empty input. No CodeCrafters grader score is claimed.

## Deliberate scope and limitations

No pipelines, redirection, globbing, variables, command substitution, background jobs, job control, shell scripting, or POSIX compatibility claims. `exit` only accepts `0` (or no arguments); these are consciously limited learning-project semantics. Pipenv, the remote CodeCrafters test suite, and Python 3.12 may not be available in the local testing environment; report those separately. No license, deployment, or scope-expanding features were added.
