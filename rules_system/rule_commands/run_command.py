#!/usr/bin/env python3

from .rule_list_command import RuleListCommand

class RunCommand(RuleListCommand):
    """Command to load and apply rules from any specified rule set."""
    
    def __init__(self, args=None):
        """Initialize with rule set name from arguments."""
        super().__init__(args)
        self.rule_set_name = getattr(args, 'rule_set', None) if args else None
    
    @classmethod
    def get_command_name(cls) -> str:
        return "run"
    
    @classmethod
    def get_description(cls) -> str:
        return "Load and apply rules from a specified rule set"
    
    @classmethod
    def add_arguments(cls, parser) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            'rule_set',
            help='Name of the rule set to execute (e.g., startup, shutdown)'
        )
    
    def get_header_message(self) -> str:
        """Return the header message for the specified rule set."""
        rule_set_display = self.rule_set_name.upper() if self.rule_set_name else "UNKNOWN"
        return f"EXECUTING {rule_set_display} RULES:"
    
    def get_config_section(self) -> str:
        """Return the rule set name from arguments."""
        if not self.rule_set_name:
            raise ValueError("No rule set specified")
        return self.rule_set_name
    
    def get_rules_from_yaml_config(self):
        """Override to get rule paths from the rule_sets section."""
        config = self.load_yaml_config()
        
        if not config:
            return []
        
        # Look in rule_sets section instead of top-level
        rule_sets = config.get('rule_sets', {})
        if not rule_sets:
            return []
        
        section = rule_sets.get(self.get_config_section())
        if not section:
            return []
        
        rule_paths = []
        
        # Add entrypoint rule
        entrypoint = section.get('entrypoint')
        if entrypoint:
            rule_paths.append(entrypoint)
        
        # Add additional rules if specified
        additional = section.get('additional', [])
        rule_paths.extend(additional)
        
        # Resolve dependencies if enabled
        options = config.get('options', {})
        if options.get('resolve_dependencies', True):
            rule_paths = self.resolve_dependencies(rule_paths)
            
            if options.get('show_dependency_info', False):
                print(f"Dependency resolution order: {rule_paths}")
        
        return rule_paths
    
    def execute(self) -> None:
        """Execute the specified rule set."""
        if not self.rule_set_name:
            print("ERROR: No rule set specified. Use 'rules_manager.py run [rule_set_name]'")
            print("Available rule sets can be seen in rules.yaml")
            return
        
        # Check if rule set exists
        config = self.load_yaml_config()
        rule_sets = config.get('rule_sets', {}) if config else {}
        
        if self.rule_set_name not in rule_sets:
            print(f"ERROR: Rule set '{self.rule_set_name}' not found in rules.yaml")
            print(f"Available rule sets: {list(rule_sets.keys())}")
            return
        
        # Execute using parent class implementation
        super().execute() 