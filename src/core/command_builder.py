"""
Command builder for Nuitka compilation.
"""
import sys

from .flag_plan import compile_flag_plan, render_command, render_command_string
from .setting_definitions import load_setting_definitions


class CommandBuilder:
    """Builds Nuitka command from configuration."""

    def __init__(self, config_manager):
        """
        Initialize command builder.

        Args:
            config_manager: ConfigManager instance
        """
        self.config = config_manager
        self.registry = load_setting_definitions()
        self._plan = None

    def _get_plan(self):
        """Compile and cache the flag plan for the current config snapshot."""
        if self._plan is None:
            self._plan = compile_flag_plan(self.config.to_dict(), self.registry)
        return self._plan

    def build(self):
        """
        Build complete Nuitka command.

        Returns:
            list: Command arguments
        """
        return render_command(self._get_plan(), python_exe=sys.executable)

    def get_command_string(self):
        """
        Get command as a single string.

        Returns:
            str: Command string
        """
        return render_command_string(self._get_plan(), python_exe=sys.executable)
