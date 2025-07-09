#!/usr/bin/env python3

from .rule_list_command import RuleListCommand

class ShutdownCommand(RuleListCommand):
    """Command to execute shutdown rules specified in the shutdown configuration file."""
    
    @classmethod
    def get_command_name(cls) -> str:
        return "shutdown"
    
    @classmethod
    def get_description(cls) -> str:
        return "Execute shutdown rules specified in the shutdown configuration file"
    
    def get_header_message(self) -> str:
        """Return the header message for shutdown rules."""
        return "EXECUTING SHUTDOWN RULES:"
    
    def get_config_section(self) -> str:
        """Return the YAML config section name."""
        return "shutdown"
    
    def execute_rule(self, rule, rule_path: str) -> None:
        """
        Execute a shutdown rule. For shutdown, we print the rule content as instructions.
        """
        print("INSTRUCTIONS TO MODEL:")
        print(f"RULE: {rule.title}")
        print(f"CONTENT: {rule.content}")
        self.print_separator() 