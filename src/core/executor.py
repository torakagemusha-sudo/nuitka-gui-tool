"""
Compilation executor for running Nuitka in a separate thread.
"""
import subprocess
import threading
import time
import logging
from enum import Enum

# Set up logging for executor operations
logger = logging.getLogger(__name__)


class CompilationStatus(Enum):
    """Compilation status enumeration."""
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"
    CANCELLED = "cancelled"


class CompilationExecutor:
    """Executes Nuitka compilation in a separate thread."""

    def __init__(self, command, output_callback=None, completion_callback=None):
        """
        Initialize compilation executor.

        Args:
            command: List of command arguments
            output_callback: Callback function for output lines (line: str)
            completion_callback: Callback function for completion (status: CompilationStatus, return_code: int)
        """
        self.command = command
        self.output_callback = output_callback
        self.completion_callback = completion_callback

        self.thread = None
        self.process = None
        self.status = CompilationStatus.IDLE
        self.return_code = None
        self.stop_flag = False
        self.start_time = None
        self.end_time = None

    def start(self):
        """Start compilation in a separate thread."""
        if self.is_running():
            return False

        self.stop_flag = False
        self.status = CompilationStatus.RUNNING
        self.return_code = None
        self.start_time = time.time()
        self.end_time = None

        self.thread = threading.Thread(target=self._run_compilation, daemon=True)
        self.thread.start()
        return True

    def stop(self):
        """Stop the running compilation."""
        if not self.is_running():
            return False

        self.stop_flag = True
        if self.process:
            try:
                self.process.terminate()
                # Give it a moment to terminate gracefully
                try:
                    self.process.wait(timeout=1.0)
                except subprocess.TimeoutExpired:
                    logger.warning("Process did not terminate gracefully, forcing kill")
                    self.process.kill()
            except (ProcessLookupError, PermissionError) as e:
                logger.error(f"Failed to stop compilation process: {e}")
            except Exception as e:
                logger.error(f"Unexpected error stopping process: {e}")

        return True

    def is_running(self):
        """
        Check if compilation is currently running.

        Returns:
            bool: True if running
        """
        return self.status == CompilationStatus.RUNNING

    def get_status(self):
        """
        Get current compilation status.

        Returns:
            CompilationStatus: Current status
        """
        return self.status

    def get_elapsed_time(self):
        """
        Get elapsed time in seconds.

        Returns:
            float: Elapsed time or None if not started
        """
        if self.start_time is None:
            return None

        if self.end_time is not None:
            return self.end_time - self.start_time
        else:
            return time.time() - self.start_time

    def _run_compilation(self):
        """Run the compilation process (runs in separate thread)."""
        try:
            # Create process
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            # Read output line by line with defensive check
            if self.process.stdout:
                for line in self.process.stdout:
                    if self.stop_flag:
                        break

                    # Send line to callback
                    if self.output_callback:
                        self.output_callback(line.rstrip('\n'))
            else:
                logger.error("Failed to capture process output stream")
                if self.output_callback:
                    self.output_callback("Error: Unable to capture compilation output")

            # Wait for process to complete
            self.return_code = self.process.wait()
            self.end_time = time.time()

            # Determine final status
            if self.stop_flag:
                self.status = CompilationStatus.CANCELLED
            elif self.return_code == 0:
                self.status = CompilationStatus.SUCCESS
            else:
                self.status = CompilationStatus.ERROR

        except FileNotFoundError as e:
            self.end_time = time.time()
            self.status = CompilationStatus.ERROR
            self.return_code = -1
            logger.error(f"Compilation command not found: {e}")
            if self.output_callback:
                self.output_callback(f"\nError: Compilation command not found. Is Nuitka installed?")

        except PermissionError as e:
            self.end_time = time.time()
            self.status = CompilationStatus.ERROR
            self.return_code = -1
            logger.error(f"Permission denied running compilation: {e}")
            if self.output_callback:
                self.output_callback(f"\nError: Permission denied running compilation")

        except subprocess.SubprocessError as e:
            self.end_time = time.time()
            self.status = CompilationStatus.ERROR
            self.return_code = -1
            logger.error(f"Subprocess error during compilation: {e}")
            if self.output_callback:
                self.output_callback(f"\nError running compilation: {e}")

        except Exception as e:
            self.end_time = time.time()
            self.status = CompilationStatus.ERROR
            self.return_code = -1
            logger.error(f"Unexpected error during compilation: {e}")
            if self.output_callback:
                self.output_callback(f"\nUnexpected error: {e}")

        finally:
            # Call completion callback
            if self.completion_callback:
                self.completion_callback(self.status, self.return_code)
