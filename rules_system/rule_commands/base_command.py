#!/usr/bin/env python3

import os
import yaml
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
        # Find paths relative to this file's location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Path to .programmatic directory (for system files like rules.yaml)
        self.system_base_path = os.path.join(current_dir, "..", "..")
        self.system_base_path = os.path.normpath(self.system_base_path)
        
        # Default project root path
        self.project_root = os.path.join(current_dir, "..", "..", "..")
        self.project_root = os.path.normpath(self.project_root)
        
        # Configure rules directory with flexibility
        self.rules_dir = self._configure_rules_directory()
    
    def _configure_rules_directory(self) -> str:
        """Configure the rules directory path using environment variables, config, or defaults."""
        
        # 1. Check environment variable first
        env_rules_dir = os.environ.get('PROGRAMMATIC_RULES_DIR')
        if env_rules_dir:
            if os.path.isabs(env_rules_dir):
                return env_rules_dir
            else:
                return os.path.normpath(os.path.join(self.project_root, env_rules_dir))
        
        # 2. Check configuration file
        config_rules_dir = self._get_rules_dir_from_config()
        if config_rules_dir:
            if os.path.isabs(config_rules_dir):
                return config_rules_dir
            else:
                return os.path.normpath(os.path.join(self.project_root, config_rules_dir))
        
        # 3. Default fallback - try local first, then parent
        local_rules_dir = os.path.join(self.system_base_path, "rules")
        if os.path.exists(local_rules_dir):
            return local_rules_dir
        else:
            return os.path.join(self.project_root, "rules")
    
    def _get_rules_dir_from_config(self) -> Optional[str]:
        """Get rules directory from configuration file."""
        try:
            config_file = os.path.join(self.system_base_path, "rules.yaml")
            if not os.path.exists(config_file):
                return None
                
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f) or {}
            
            return config.get('options', {}).get('rules_directory')
        except Exception:
            return None
    
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
            print(f"Rules directory not found at {self.rules_dir}.")
            print("You can configure it using:")
            print("1. Environment variable: PROGRAMMATIC_RULES_DIR")
            print("2. Configuration: rules_directory in rules.yaml options section")
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