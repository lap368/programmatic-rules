#!/usr/bin/env python3

"""
Commands package for the Rules Manager.
Contains all available command implementations.
"""

from .base_command import BaseCommand
from .rule_list_command import RuleListCommand
from .startup_command import StartupCommand
from .shutdown_command import ShutdownCommand
from .list_command import ListCommand
from .show_command import ShowCommand

# Registry of all available commands
AVAILABLE_COMMANDS = {
    StartupCommand.get_command_name(): StartupCommand,
    ShutdownCommand.get_command_name(): ShutdownCommand,
    ListCommand.get_command_name(): ListCommand,
    ShowCommand.get_command_name(): ShowCommand,
}

def get_command_class(command_name: str):
    """Get a command class by name."""
    return AVAILABLE_COMMANDS.get(command_name)

def get_all_commands():
    """Get all available command classes."""
    return AVAILABLE_COMMANDS

__all__ = [
    'BaseCommand',
    'RuleListCommand',
    'StartupCommand', 
    'ShutdownCommand',
    'ListCommand',
    'ShowCommand',
    'AVAILABLE_COMMANDS',
    'get_command_class',
    'get_all_commands'
] 