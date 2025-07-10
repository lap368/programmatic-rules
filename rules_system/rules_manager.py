#!/usr/bin/env python3

import argparse
import sys
import os

from rule_commands import get_command_class, get_all_commands

class RulesManager:
    """
    Main Rules Manager class that coordinates command execution.
    Uses a plugin-style architecture to load and execute commands.
    """
    
    def __init__(self):
        self.available_commands = get_all_commands()
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser with dynamic command registration."""
        parser = argparse.ArgumentParser(
            description='Manage programmatic rules for AI interactions',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Create subparsers for commands
        subparsers = parser.add_subparsers(
            dest='command',
            help='Available commands',
            metavar='COMMAND'
        )
        
        # Dynamically register all available commands
        for command_name, command_class in self.available_commands.items():
            subparser = subparsers.add_parser(
                command_name,
                help=command_class.get_description()
            )
            # Let each command add its own arguments
            command_class.add_arguments(subparser)
        
        return parser
    
    def execute_command(self, args) -> None:
        """Execute the specified command."""
        if not args.command:
            print("ERROR: No command specified. Use --help for available commands.")
            sys.exit(1)
        
        command_class = get_command_class(args.command)
        if not command_class:
            print(f"ERROR: Unknown command '{args.command}'")
            sys.exit(1)
        
        try:
            command_instance = command_class(args)
            command_instance.execute()
        except Exception as e:
            print(f"ERROR executing command '{args.command}': {e}")
            sys.exit(1)
    
    def run(self, argv=None) -> None:
        """Main entry point for the Rules Manager."""
        parser = self.create_parser()
        args = parser.parse_args(argv)
        
        self.execute_command(args)
    
    def list_available_commands(self) -> None:
        """List all available commands with descriptions."""
        print("Available Commands:")
        print("=" * 50)
        for command_name, command_class in self.available_commands.items():
            print(f"  {command_name}: {command_class.get_description()}")
        print("=" * 50)

def main():
    """Main entry point when run as a script."""
    manager = RulesManager()
    manager.run()

if __name__ == "__main__":
    main() 