#!/usr/bin/env python3

from .rule_list_command import RuleListCommand

class StartupCommand(RuleListCommand):
    """Command to load and apply rules specified in the startup configuration file."""
    
    @classmethod
    def get_command_name(cls) -> str:
        return "startup"
    
    @classmethod
    def get_description(cls) -> str:
        return "Load and apply rules specified in the startup configuration file"
    
    def get_header_message(self) -> str:
        """Return the header message for startup rules."""
        return "APPLYING STARTUP RULES:"
    
    def get_config_section(self) -> str:
        """Return the YAML config section name."""
        return "startup" 