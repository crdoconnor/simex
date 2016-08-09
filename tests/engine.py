from commandlib import run
import hitchpython
import hitchtest
import hitchcli
import kaching
import time


class ExecutionEngine(hitchtest.ExecutionEngine):
    """Hitch bootstrap engine tester."""

    def set_up(self):
        self.path.project = self.path.engine.parent
        self.path.state = self.path.engine.parent.joinpath("state")
        self.path.samples = self.path.engine.joinpath("samples")

        if self.path.state.exists():
            self.path.state.rmtree()
        self.path.state.mkdir()

        if self.settings.get("kaching", False):
            kaching.start()

        self.python_package = hitchpython.PythonPackage(
            python_version=self.preconditions.get('python_version', '3.5.0')
        )
        self.python_package.build()

        self.python = self.python_package.cmd.python
        self.pip = self.python_package.cmd.pip

        self.cli_steps = hitchcli.CommandLineStepLibrary(
            default_timeout=int(self.settings.get("cli_timeout", 5))
        )

        self.cd = self.cli_steps.cd
        self.pexpect_run = self.cli_steps.run
        self.expect = self.cli_steps.expect
        self.send_control = self.cli_steps.send_control
        self.send_line = self.cli_steps.send_line
        self.exit_with_any_code = self.cli_steps.exit_with_any_code
        self.exit = self.cli_steps.exit
        self.finish = self.cli_steps.finish

        run(self.pip("uninstall", "simex", "-y").ignore_errors())
        run(self.pip("install", ".").in_dir(self.path.project))
        run(self.pip("install", "ipykernel"))
        run(self.pip("install", "pip"))
        run(self.pip("install", "q"))
        run(self.pip("install", "pudb"))

        for filename, contents in self.preconditions.get("files", {}).items():
            self.path.state.joinpath(filename).write_text(contents)
        self.path.state.chdir()

    def lint(self, args=None):
        """Lint the source code."""
        run(self.pip("install", "flake8"))
        run(self.python_package.cmd.flake8(*args).in_dir(self.path.project))

    def run(self, filename="example_code.py"):
        self.path.state.chdir()
        self.pexpect_run("{0} {1}".format(self.python, filename))

    def exit_with_error(self):
        self.exit(with_code=1)

    def exited_successfully(self):
        self.finish()

    def file_was_created_with(self, filename="", contents=""):
        if not self.path.state.joinpath(filename).exists():
            raise RuntimeError("{0} does not exist".format(filename))
        if self.path.state.joinpath(filename).bytes().decode('utf8') != contents:
            raise RuntimeError("{0} did not contain {0}".format(filename, contents))

    def sleep(self, duration):
        """Sleep for specified duration."""
        time.sleep(int(duration))

    def placeholder(self):
        """Placeholder to add a new test."""
        pass

    def pause(self, message=""):
        if hasattr(self, 'services') and self.services is not None:
            self.services.start_interactive_mode()
        self.ipython(message=message)
        if hasattr(self, 'services') and self.services is not None:
            self.services.stop_interactive_mode()

    def on_failure(self):
        """Stop and IPython."""
        if self.settings.get("kaching", False):
            kaching.fail()
        if self.settings.get("pause_on_failure", False):
            self.pause(message=self.stacktrace.to_template())

    def on_success(self):
        """Ka-ching!"""
        if self.settings.get("kaching", False):
            kaching.win()
        if self.settings.get("pause_on_success", False):
            self.pause(message="SUCCESS")

    def stop_services(self):
        if hasattr(self, 'services'):
            if self.services is not None:
                self.services.shutdown()

    def tear_down(self):
        """Clean out the state directory."""
        self.stop_services()
