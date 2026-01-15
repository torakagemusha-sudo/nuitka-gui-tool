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

    def build(self):
        """
        Build complete Nuitka command.

        Returns:
            list: Command arguments
        """
        plan = compile_flag_plan(self.config.to_dict(), self.registry)
        return render_command(plan, python_exe=sys.executable)
    def get_command_string(self):
        """
        Get command as a single string.

        Returns:
            str: Command string
        """
        plan = compile_flag_plan(self.config.to_dict(), self.registry)
        return render_command_string(plan, python_exe=sys.executable)
