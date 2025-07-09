#!/usr/bin/env python3

import os
from abc import ABC, abstractmethod
from typing import List, Optional

class BaseCommand(ABC):
    """
    Base class for all Rules Manager commands.
    Provides shared functionality and defines the command interface.
    """
    
    def __init__(self, args=None):
        """Initialize the command with optional arguments."""
        self.args = args
        # Find the programmatic_rules directory relative to this file's location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.rules_base_path = os.path.join(current_dir, "..", "..")
        self.rules_base_path = os.path.normpath(self.rules_base_path)
        self.rules_dir = os.path.join(self.rules_base_path, "rules")
    
    def print_header(self, title: str, width: int = 50) -> None:
        """Print a formatted header for command output."""
        print(title)
        print("=" * width)
    
    def print_separator(self, width: int = 30) -> None:
        """Print a separator line."""
        print("-" * width)
    
    def print_footer(self, width: int = 50) -> None:
        """Print a footer line."""
        print("=" * width)
    
    def check_rules_directory(self) -> bool:
        """Check if the rules directory exists."""
        if not os.path.exists(self.rules_dir):
            print("Rules directory not found.")
            return False
        return True
    
    def get_rule_files(self) -> List[str]:
        """Get list of all JSON rule files, including those in subdirectories."""
        if not self.check_rules_directory():
            return []
        
        rule_files = []
        
        # Walk through the rules directory recursively
        for root, dirs, files in os.walk(self.rules_dir):
            for file in files:
                if file.endswith('.json'):
                    # Get the relative path from the rules directory
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, self.rules_dir)
                    rule_files.append(relative_path)
        
        return rule_files
    
    def load_rule(self, rule_path: str):
        """Load a rule using the Rule class."""
        # Import here to avoid circular imports
        from rule import Rule
        return Rule(file_path=rule_path)
    
    def handle_error(self, error: Exception, context: str = "") -> None:
        """Standard error handling for commands."""
        error_msg = f"ERROR{f' in {context}' if context else ''}: {error}"
        print(error_msg)
    
    @abstractmethod
    def execute(self) -> None:
        """Execute the command. Must be implemented by subclasses."""
        pass
    
    @classmethod
    @abstractmethod
    def get_command_name(cls) -> str:
        """Return the command name for registration. Must be implemented by subclasses."""
        pass
    
    @classmethod
    def get_description(cls) -> str:
        """Return a description of what this command does."""
        return "No description available."
    
    @classmethod
    def add_arguments(cls, parser) -> None:
        """Add command-specific arguments to the argument parser."""
        # Default implementation - subclasses can override
        pass 