#!/usr/bin/env python3

import os
import sys
from .base_command import BaseCommand

class ShowCommand(BaseCommand):
    """Command to display comprehensive information about a specific rule."""
    
    @classmethod
    def get_command_name(cls) -> str:
        return "show"
    
    @classmethod
    def get_description(cls) -> str:
        return "Display comprehensive information about a specific rule"
    
    @classmethod
    def add_arguments(cls, parser) -> None:
        """Add command-specific arguments."""
        parser.add_argument('--rule', required=True, help='Rule name to show details for')
    
    def execute(self) -> None:
        """Show detailed information about a specific rule."""
        if not self.args or not self.args.rule:
            print("ERROR: --rule parameter required for show action")
            sys.exit(1)
        
        rule_name = self.args.rule
        rule_path = os.path.join(self.rules_dir, rule_name)
        if not rule_name.endswith('.json'):
            rule_path += '.json'
        
        if not os.path.exists(rule_path):
            print(f"Rule file not found: {rule_path}")
            return
        
        try:
            rule = self.load_rule(rule_path)
            self.print_header("RULE DETAILS:")
            print(f"Title: {rule.title}")
            print(f"Category: {rule.category}")
            print(f"Version: {rule.version}")
            print(f"Status: {rule.status}")
            print(f"Requires: {rule.requires if rule.requires else 'None'}")
            print(f"Relevant: {rule.relevant if rule.relevant else 'None'}")
            print(f"File: {rule_path}")
            self.print_separator()
            print("Content:")
            print(rule.content)
            self.print_footer()
        except Exception as e:
            self.handle_error(e, "loading rule") 