# Rules Manager Guide

The `rules_manager.py` script is a unified tool for managing programmatic rules in AI interactions. It uses a YAML-based configuration system with dependency resolution and entrypoint patterns.

## Overview

The Rules Manager provides a centralized way to:
- Load and apply rules at interaction startup with dependency resolution
- Execute shutdown procedures with configurable rules
- Browse and inspect available rules
- View detailed rule information
- Manage rule dependencies automatically

## Usage

```bash
python3 programmatic_rules/rules_manager.py <action> [options]
```

## Available Actions

### 1. Startup (`startup`)

**Purpose**: Load and apply rules specified in the YAML configuration with dependency resolution.

**Usage**: 
```bash
python3 programmatic_rules/rules_manager.py startup
```

**What it does**:
- Reads `programmatic_rules/rules.yaml` for startup configuration
- Loads the startup entrypoint rule and resolves all dependencies
- Displays active rules in dependency order (dependencies first)
- Skips inactive rules with notification
- Shows error messages for invalid or missing rule files

**Example Output**:
```
APPLYING STARTUP RULES:
==================================================
RULE: Hello World
CONTENT: Put a hello world message in a markdown block in the chat.
------------------------------
RULE: Startup Entrypoint
CONTENT: Main startup entrypoint rule. Ready for project-specific customization.
------------------------------
==================================================
```

### 2. Shutdown (`shutdown`)

**Purpose**: Execute model shutdown instructions and final output requirements.

**Usage**:
```bash
python3 programmatic_rules/rules_manager.py shutdown
```

**What it does**:
- Reads `programmatic_rules/rules.yaml` for shutdown configuration
- Loads the shutdown entrypoint rule and resolves all dependencies
- Provides instructions for the AI model's end-of-turn behavior
- Displays rules in dependency order

**Example Output**:
```
EXECUTING SHUTDOWN RULES:
==================================================
INSTRUCTIONS TO MODEL:
RULE: Goodbye World
CONTENT: This is a development rule that prints goodbye world at shutdown.
------------------------------
INSTRUCTIONS TO MODEL:
RULE: Shutdown Entrypoint
CONTENT: Main shutdown entrypoint rule. Ready for project-specific customization.
------------------------------
==================================================
```

### 3. List Rules (`list`)

**Purpose**: Display all available rule files with status information.

**Usage**:
```bash
python3 programmatic_rules/rules_manager.py list
```

**What it does**:
- Scans the `programmatic_rules/rules/` directory for `.json` files
- Shows rule status (✓ for active, ✗ for inactive/error)
- Displays rule title and dependency information
- Reports errors for malformed rule files

**Example Output**:
```
AVAILABLE RULES:
==================================================
✓ hello_world.json: Hello World (Active)
  Dependencies: None
✓ startup_entrypoint.json: Startup Entrypoint (Active)
  Dependencies: rules/hello_world.json
✗ inactive_rule.json: Inactive Rule (Inactive)
  Dependencies: None
==================================================
```

### 4. Show Rule Details (`show`)

**Purpose**: Display comprehensive information about a specific rule.

**Usage**:
```bash
python3 programmatic_rules/rules_manager.py show --rule <rule_name>
```

**Parameters**:
- `--rule`: Name of the rule file (with or without `.json` extension)

**What it does**:
- Loads the specified rule file
- Shows complete metadata (title, status, dependencies)
- Displays the full rule content
- Shows file path information

**Example Usage**:
```bash
python3 programmatic_rules/rules_manager.py show --rule hello_world
python3 programmatic_rules/rules_manager.py show --rule startup_entrypoint.json
```

**Example Output**:
```
RULE DETAILS:
==================================================
Title: Hello World
Status: Active
Dependencies: None
File: programmatic_rules/rules/hello_world.json
--------------------------------------------------
Content:
Put a hello world message in a markdown block in the chat.
==================================================
```

## Configuration System

### YAML Configuration (`rules.yaml`)

The system uses a unified YAML configuration file at `programmatic_rules/rules.yaml`:

```yaml
# Rules System Configuration
startup:
  # Primary entrypoint rule that manages startup sequence
  entrypoint: rules/startup_entrypoint.json
  
shutdown:
  # Primary entrypoint rule that manages shutdown sequence  
  entrypoint: rules/shutdown_entrypoint.json

# Configuration options
options:
  # Enable dependency resolution (recommended)
  resolve_dependencies: true
  
  # Show dependency resolution details during execution
  show_dependency_info: false
```

### Entrypoint Pattern

The system uses an entrypoint pattern where:
- **Startup**: Loads `startup_entrypoint.json` and all its dependencies
- **Shutdown**: Loads `shutdown_entrypoint.json` and all its dependencies
- **Dependencies**: Automatically resolved in correct order using `requires` field

## Rule File Structure

Rules are stored as JSON files in `programmatic_rules/rules/` with the following structure:

```json
{
  "title": "Rule Title",
  "content": "Rule description and instructions...",
  "active": true,
  "requires": ["rules/dependency1.json", "rules/dependency2.json"]
}
```

### Fields:
- **title**: Human-readable rule name
- **content**: Detailed rule instructions for the AI model
- **active**: Boolean indicating if rule should be executed
- **requires**: Array of dependency rule file paths (relative to project root)

### Dependency Resolution

The system automatically:
- Resolves dependencies recursively
- Loads dependencies before their dependents
- Detects and prevents circular dependencies
- Maintains execution order (dependencies first)

**Example Dependency Chain**:
```
startup_entrypoint.json
└── requires: ["rules/hello_world.json"]
    └── requires: [] (no dependencies)
```

**Execution Order**: `hello_world.json` → `startup_entrypoint.json`

## System Architecture

### Class-Based Design

The system uses a modular class-based architecture:

```
BaseCommand (abstract)
├── RuleListCommand (abstract)
│   ├── StartupCommand
│   └── ShutdownCommand
├── ListCommand
└── ShowCommand
```

### Key Features

- **Unified Configuration**: Single YAML file for all settings
- **Dependency Resolution**: Automatic handling of rule dependencies
- **Entrypoint Pattern**: Clean separation of concerns
- **Error Handling**: Comprehensive error reporting
- **Extensible**: Easy to add new commands and features

## Integration with AI Workflow

### Startup Integration
```bash
python3 programmatic_rules/rules_manager.py startup
```

### Shutdown Integration  
```bash
python3 programmatic_rules/rules_manager.py shutdown
```

### Development vs Production

The system supports different configurations:
- **Development**: May include debug rules and verbose output
- **Production**: Clean, minimal rule sets for distribution

## Error Handling

The Rules Manager includes comprehensive error handling:
- Missing YAML configuration files
- Invalid rule file paths in dependencies
- Malformed JSON rule files
- Circular dependency detection
- Missing required rule files

## Migration from Legacy Systems

If migrating from older `.txt` or `.conf` based systems:
1. Create `rules.yaml` with entrypoint configuration
2. Update rule files to use simplified JSON structure
3. Add dependency information to `requires` fields
4. Test dependency resolution with `show_dependency_info: true` 