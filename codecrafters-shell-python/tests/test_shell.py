"""Builtins and external commands, including genuine child-process execution."""
import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from app.main import execute


class ShellTests(unittest.TestCase):
    def setUp(self):
        self.cwd = Path.cwd()
        self.temp = tempfile.TemporaryDirectory()
        os.chdir(self.temp.name)

    def tearDown(self):
        os.chdir(self.cwd)
        self.temp.cleanup()

    def run_builtin(self, line):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            done = execute(line)
        return done, output.getvalue()

    def test_builtins_exact_dispatch(self):
        self.assertEqual(self.run_builtin("type echo"), (False, "echo is a shell builtin\n"))
        self.assertEqual(self.run_builtin("typewriter"), (False, "typewriter: command not found\n"))
        self.assertEqual(self.run_builtin("echo 'a  b' c\\ d"), (False, "a  b c d\n"))
        self.assertEqual(self.run_builtin("echo"), (False, "\n"))

    def test_exit_and_bad_quote(self):
        self.assertEqual(self.run_builtin("exit 0"), (True, ""))
        self.assertEqual(self.run_builtin("exit 1"), (False, "exit: only exit 0 is supported\n"))
        self.assertIn("No closing quotation", self.run_builtin("echo '")[1])

    def test_cd_relative_absolute_and_home(self):
        target = Path(self.temp.name) / "space dir"
        target.mkdir()
        self.assertEqual(self.run_builtin("cd 'space dir'"), (False, ""))
        self.assertEqual(Path.cwd(), target)
        self.run_builtin("cd ..")
        self.assertEqual(Path.cwd(), Path(self.temp.name))
        self.run_builtin(f"cd {target}")
        self.assertEqual(Path.cwd(), Path(self.temp.name))
        self.run_builtin("cd")
        self.assertEqual(Path.cwd(), Path.home())

    def test_cd_missing_and_short_input(self):
        self.assertFalse(self.run_builtin("cd")[0])
        self.assertIn("No such file or directory", self.run_builtin("cd /no/such/path/ever")[1])
        self.assertEqual(self.run_builtin(""), (False, ""))

    def test_type_which_and_missing(self):
        found = self.run_builtin("type echo definitely_not_a_command_xyz")[1]
        self.assertIn("echo is a shell builtin", found)
        self.assertIn("definitely_not_a_command_xyz: not found", found)

    def test_real_process_multiple_commands_and_nonzero_exit(self):
        root = Path(__file__).resolve().parents[1]
        script = "echo 'two words'\npwd\n" + f"{sys.executable} -c 'import sys;sys.exit(3)'\n" + "echo survived\nexit 0\n"
        result = subprocess.run([sys.executable, "-m", "app.main"], cwd=root, input=script, text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("two words\n", result.stdout)
        self.assertIn("survived\n", result.stdout)

    def test_eof_terminates(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run([sys.executable, "-m", "app.main"], cwd=root, input="", text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
