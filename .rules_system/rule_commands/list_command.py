#!/usr/bin/env python3

import os
from .base_command import BaseCommand

class ListCommand(BaseCommand):
    """Command to display all available rule files with status information."""
    
    @classmethod
    def get_command_name(cls) -> str:
        return "list"
    
    @classmethod
    def get_description(cls) -> str:
        return "Display all available rule files with status information"
    
    def execute(self) -> None:
        """List all available rule files in the rules directory."""
        rule_files = self.get_rule_files()
        
        if not rule_files:
            print("No rule files found.")
            return
        
        self.print_header("AVAILABLE RULES:")
        
        for rule_file in sorted(rule_files):
            try:
                rule_path = os.path.join(self.rules_dir, rule_file)
                rule = self.load_rule(rule_path)
                status_indicator = "✓" if rule.is_active() else "✗"
                print(f"{status_indicator} {rule_file}: {rule.title} ({rule.status})")
                print(f"  Category: {rule.category}, Version: {rule.version}")
                if rule.requires:
                    print(f"  Requires: {', '.join(rule.requires)}")
            except Exception as e:
                print(f"✗ {rule_file}: ERROR - {e}")
        
        self.print_footer() 