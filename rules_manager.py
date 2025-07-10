#!/usr/bin/env python3

"""
Rules Manager - User-facing entry point

This is a wrapper that provides easy access to the core rules system
located in the rules_system directory. Users should run this file
directly without needing to navigate into system directories.

Usage:
    python3 programmatic_rules/rules_manager.py <command> [options]

Commands:
    startup     Load and apply rules from startup_rules.conf
    shutdown    Execute shutdown instructions for the model
    list        Display all available rules
    show        Show detailed information about a specific rule
"""

import sys
import os

# Add the system directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rules_system'))

try:
    from rules_manager import main
except ImportError as e:
    print(f"ERROR: Could not import rules system: {e}")
    print("Make sure the rules_system directory exists and contains the core system files.")
    sys.exit(1)

if __name__ == "__main__":
    main() 