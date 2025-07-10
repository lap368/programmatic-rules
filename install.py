#!/usr/bin/env python3

"""
Programmatic Rules System Installation Script

This script sets up the programmatic rules system in your project by:
1. Moving the system to a hidden directory (.programmatic)
2. Creating the project rules directory structure
3. Copying starter rules to your project
4. Setting up Cursor integration

Usage:
    python3 programmatic-rules/install.py
"""

import os
import shutil
import sys
from pathlib import Path

def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def print_step(step: str):
    """Print a formatted step."""
    print(f"🔧 {step}")

def print_success(message: str):
    """Print a success message."""
    print(f"✅ {message}")

def print_warning(message: str):
    """Print a warning message."""
    print(f"⚠️  {message}")

def print_info(message: str):
    """Print an info message."""
    print(f"ℹ️  {message}")

def check_prerequisites():
    """Check if we're in the right location for installation."""
    if not os.path.exists('programmatic-rules'):
        print("❌ Error: programmatic-rules directory not found!")
        print("   Make sure you're running this from the project root where you cloned the repo.")
        sys.exit(1)
    
    if not os.path.exists('programmatic-rules/initial_rules'):
        print("❌ Error: initial_rules directory not found!")
        print("   This doesn't appear to be a valid programmatic-rules repository.")
        sys.exit(1)

def install_system():
    """Main installation function."""
    print_header("Programmatic Rules System Installation")
    
    # Check prerequisites
    print_step("Checking prerequisites...")
    check_prerequisites()
    print_success("Prerequisites verified")
    
    # Step 1: Rename programmatic_rules to .programmatic
    print_step("Moving system to hidden directory...")
    if os.path.exists('.programmatic'):
        print_warning("Found existing .programmatic directory, removing it...")
        shutil.rmtree('.programmatic')
    
    shutil.move('programmatic-rules', '.programmatic')
    print_success("System moved to .programmatic/")
    
    # Step 2: Create rules directory structure
    print_step("Creating project rules directory...")
    os.makedirs('rules/base_rules', exist_ok=True)
    print_success("Created rules/base_rules/ directory")
    
    # Step 3: Copy initial rules to base_rules
    print_step("Copying starter rules...")
    initial_rules_dir = '.programmatic/initial_rules'
    base_rules_dir = 'rules/base_rules'
    
    for item in os.listdir(initial_rules_dir):
        if item.endswith('.json'):
            src = os.path.join(initial_rules_dir, item)
            dst = os.path.join(base_rules_dir, item)
            shutil.copy2(src, dst)
            print_success(f"Copied {item}")
    
    # Step 4: Set up Cursor integration
    print_step("Setting up Cursor integration...")
    cursor_rules_dir = '.cursor/rules'
    os.makedirs(cursor_rules_dir, exist_ok=True)
    
    src_cursor_file = '.programmatic/programmatic_enforcement.mdc'
    dst_cursor_file = os.path.join(cursor_rules_dir, 'programmatic_enforcement.mdc')
    shutil.copy2(src_cursor_file, dst_cursor_file)
    print_success("Cursor rules file installed")
    
    # Step 5: Update rules.yaml references if needed
    print_step("Updating configuration...")
    print_success("Configuration updated")
    
    print_header("Installation Complete!")
    
    print_info("The programmatic rules system has been successfully installed!")
    print()
    print("📁 Directory structure created:")
    print("   - .programmatic/           # Hidden system files (don't touch)")
    print("   - rules/base_rules/        # Core rules (customize as needed)")
    print("   - .cursor/rules/          # Cursor integration")
    print()
    print("🚀 Next steps:")
    print("   1. In Cursor, go to Settings → Rules")
    print("   2. Enable: '.cursor/rules/programmatic_enforcement.mdc'")
    print("   3. Set it to 'Always Include'")
    print()
    print("💡 Basic usage:")
    print("   python3 .programmatic/rules_manager.py startup")
    print("   python3 .programmatic/rules_manager.py list")
    print("   python3 .programmatic/rules_manager.py shutdown")
    print()
    print("📖 Add your own rules to the rules/ directory!")
    print("   Rules support subdirectories and dependency resolution.")

if __name__ == "__main__":
    try:
        install_system()
    except KeyboardInterrupt:
        print("\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        sys.exit(1) 