#!/usr/bin/env python3

import os
import yaml
from abc import abstractmethod
from typing import Set, List, Dict, Any
from .base_command import BaseCommand

class RuleListCommand(BaseCommand):
    """
    Abstract base class for commands that load and execute rules from configuration files.
    Provides common functionality for loading rules from .conf files and executing them.
    """
    
    @abstractmethod
    def get_header_message(self) -> str:
        """Return the header message to display before executing rules."""
        pass
    
    @abstractmethod  
    def get_config_section(self) -> str:
        """Return the YAML config section name ('startup' or 'shutdown')."""
        pass
    
    def process_rule_before_execution(self, rule, rule_path: str) -> bool:
        """
        Process a rule before execution. Return True to execute, False to skip.
        Can be overridden by subclasses for custom processing.
        """
        if rule.is_active():
            return True
        else:
            print(f"SKIPPING INACTIVE RULE: {rule.title}")
            return False
    
    def execute_rule(self, rule, rule_path: str) -> None:
        """
        Execute a single rule. Can be overridden by subclasses for custom execution.
        Default implementation prints rule title and content.
        """
        print(f"RULE: {rule.title}")
        print(f"CONTENT: {rule.content}")
        self.print_separator()
    
    def load_yaml_config(self) -> Dict[str, Any]:
        """Load configuration from rules.yaml file."""
        yaml_config_file = os.path.join(self.rules_base_path, "rules.yaml")
        
        if not os.path.exists(yaml_config_file):
            return {}
        
        try:
            with open(yaml_config_file, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            self.handle_error(e, "loading rules.yaml config")
            return {}
    
    def resolve_dependencies(self, rule_paths: List[str], visited: Set[str] = None) -> List[str]:
        """
        Resolve rule dependencies recursively to build execution order.
        Returns a list of rule paths in dependency order (dependencies first).
        """
        if visited is None:
            visited = set()
        
        resolved_paths = []
        
        for rule_path in rule_paths:
            if rule_path in visited:
                continue  # Skip already processed rules
                
            visited.add(rule_path)
            
            try:
                full_rule_path = os.path.join(self.rules_base_path, rule_path)
                rule = self.load_rule(full_rule_path)
                
                # Recursively resolve dependencies first
                if rule.requires:
                    dependency_paths = self.resolve_dependencies(rule.requires, visited)
                    resolved_paths.extend(dependency_paths)
                
                # Add this rule after its dependencies
                if rule_path not in resolved_paths:
                    resolved_paths.append(rule_path)
                    
            except Exception as e:
                self.handle_error(e, f"resolving dependencies for {rule_path}")
        
        return resolved_paths
    
    def get_rules_from_yaml_config(self) -> List[str]:
        """Get rule paths from the unified YAML configuration."""
        config = self.load_yaml_config()
        
        if not config:
            return []
        
        section = config.get(self.get_config_section())
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
        """Main execution method that loads and processes rules from YAML config."""
        # Load from YAML config only (no fallback to legacy .conf files)
        rule_paths = self.get_rules_from_yaml_config()
        
        if not rule_paths:
            print(f"No rules found in rules.yaml for section '{self.get_config_section()}'")
            return
        
        self.print_header(self.get_header_message())
        
        for rule_path in rule_paths:
            try:
                full_rule_path = os.path.join(self.rules_base_path, rule_path)
                rule = self.load_rule(full_rule_path)
                
                if self.process_rule_before_execution(rule, rule_path):
                    self.execute_rule(rule, rule_path)
                    
            except Exception as e:
                self.handle_error(e, f"loading rule {rule_path}")
        
        self.print_footer() 