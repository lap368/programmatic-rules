#!/usr/bin/env python3

import json
import os
from typing import List, Optional, Dict, Any

class Rule:
    """
    Represents a rule with structured metadata and content.
    Can load rules from JSON files or be created programmatically.
    """
    
    def __init__(self, file_path: Optional[str] = None, **kwargs):
        """
        Initialize a Rule either from a file or from keyword arguments.
        
        Args:
            file_path: Path to JSON file containing rule data
            **kwargs: Direct rule properties (category, version, etc.)
        """
        # Default values
        self.category: str = "General"
        self.version: str = "1.0"
        self.status: str = "Active"
        self.requires: List[str] = []
        self.relevant: List[str] = []
        self.title: str = ""
        self.content: str = ""
        self.file_path: Optional[str] = file_path
        
        if file_path:
            self.load_from_file(file_path)
        else:
            # Set properties from kwargs
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
    
    def load_from_file(self, file_path: str) -> None:
        """Load rule data from a JSON file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Rule file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        self.category = data.get('category', 'General')
        self.version = data.get('version', '1.0')
        self.status = data.get('status', 'Active')
        self.requires = data.get('requires', [])
        self.relevant = data.get('relevant', [])
        self.title = data.get('title', '')
        self.content = data.get('content', '')
        self.file_path = file_path
    
    def save_to_file(self, file_path: str) -> None:
        """Save rule data to a JSON file."""
        data = {
            'category': self.category,
            'version': self.version,
            'status': self.status,
            'requires': self.requires,
            'relevant': self.relevant,
            'title': self.title,
            'content': self.content
        }
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.file_path = file_path
    
    def is_active(self) -> bool:
        """Check if this rule is active."""
        return self.status.lower() == 'active'
    
    def get_dependencies(self) -> List[str]:
        """Get all required dependencies."""
        return self.requires.copy()
    
    def get_relevant_rules(self) -> List[str]:
        """Get all relevant (conditional) rules."""
        return self.relevant.copy()
    
    def __str__(self) -> str:
        """String representation of the rule."""
        return f"Rule('{self.title}', {self.category}, v{self.version}, {self.status})"
    
    def __repr__(self) -> str:
        """Detailed representation of the rule."""
        return (f"Rule(title='{self.title}', category='{self.category}', "
                f"version='{self.version}', status='{self.status}', "
                f"requires={self.requires}, relevant={self.relevant})")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert rule to dictionary format."""
        return {
            'category': self.category,
            'version': self.version,
            'status': self.status,
            'requires': self.requires,
            'relevant': self.relevant,
            'title': self.title,
            'content': self.content,
            'file_path': self.file_path
        } 