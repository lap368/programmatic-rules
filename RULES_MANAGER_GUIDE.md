# Rules Manager Guide

The `rules_manager.py` script is a unified tool for managing programmatic rules in AI interactions. It replaces the separate `startup.py` and `shutdown.py` scripts with a single, more powerful interface.

## Overview

The Rules Manager provides a centralized way to:
- Load and apply rules at interaction startup
- Execute shutdown procedures
- Browse and inspect available rules
- View detailed rule information

## Usage

```bash
python3 programmatic_rules/rules_manager.py <action> [options]
```

## Available Actions

### 1. Startup (`startup`)

**Purpose**: Load and apply rules specified in the startup configuration file.

**Usage**: 
```bash
python3 programmatic_rules/rules_manager.py startup
```

**What it does**:
- Reads `programmatic_rules/startup_rules.txt` for rule file paths
- Loads each specified rule from the `rules/` directory  
- Displays active rules that will be applied to the AI model
- Skips inactive rules with notification
- Shows error messages for invalid or missing rule files

**Example Output**:
```
APPLYING STARTUP RULES:
==================================================
RULE: PYTHON Capitalization Rule
CONTENT: Whenever you write the word 'python' in any response, you MUST write it
 as 'PYTHON' in all capital letters. EXCEPTION: Do not capitalize when constructing 
 actual program calls (e.g., 'python3 script.py', 'python -m module'). This rule 
 applies to all other instances of the word.
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
- Provides instructions for the AI model's end-of-turn behavior
- Specifies what final output should be generated
- Controls conversation termination procedures

**Example Output**:
```
INSTRUCTIONS TO MODEL:
All instructions that follow are REQUIRED to be executed. From this point on, no further text should be sent
 to the user except for any text that you are explicitly told to include from one of these rules.
Please say Hello World to the user in a markdown block in the chat.
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
- Displays rule title, category, and version
- Lists dependencies if any exist
- Reports errors for malformed rule files

**Example Output**:
```
AVAILABLE RULES:
==================================================
✓ caps_python.json: PYTHON Capitalization Rule (Active)
  Category: Language, Version: 1.0
✗ example_inactive.json: Example Rule (Inactive)
  Category: Test, Version: 1.0
  Requires: dependency_rule
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
- Shows complete metadata (title, category, version, status, dependencies)
- Displays the full rule content
- Shows file path information

**Example Usage**:
```bash
python3 programmatic_rules/rules_manager.py show --rule caps_python
python3 programmatic_rules/rules_manager.py show --rule caps_python.json
```

**Example Output**:
```
RULE DETAILS:
==================================================
Title: PYTHON Capitalization Rule
Category: Language
Version: 1.0
Status: Active
Requires: None
Relevant: None
File: programmatic_rules/rules/caps_python.json
--------------------------------------------------
Content:
Whenever you write the word 'python' in any response, you MUST write it as 'PYTHON' 
in all capital letters. EXCEPTION: Do not capitalize when constructing actual program 
calls (e.g., 'python3 script.py', 'python -m module'). This rule applies to all 
other instances of the word.
==================================================
```

## Rule File Structure

Rules are stored as JSON files in `programmatic_rules/rules/` with the following structure:

```json
{
  "category": "Language",
  "version": "1.0", 
  "status": "Active",
  "requires": [],
  "relevant": [],
  "title": "Rule Title",
  "content": "Rule description and instructions..."
}
```

### Fields:
- **category**: Logical grouping (e.g., "Language", "Behavior", "Format")
- **version**: Semantic version number
- **status**: "Active" or "Inactive" 
- **requires**: Array of dependency rule file names
- **relevant**: Array of conditionally relevant rule file names
- **title**: Human-readable rule name
- **content**: Detailed rule instructions for the AI model

## Configuration Files

### startup_rules.txt
Located at `programmatic_rules/startup_rules.txt`, this file contains a comma-separated list of rule file paths to load at startup:

```
rules/caps_python.json,rules/formatting_rule.json
```

Empty file = no rules loaded at startup.

## Error Handling

The Rules Manager includes comprehensive error handling:
- Missing files are reported with clear messages
- Malformed JSON files show parsing errors
- Invalid rule paths are logged and skipped
- Missing required parameters trigger usage help

## Integration with AI Workflow

### Startup Integration
Replace calls to `startup.py` with:
```bash
python3 programmatic_rules/rules_manager.py startup
```

### Shutdown Integration  
Replace calls to `shutdown.py` with:
```bash
python3 programmatic_rules/rules_manager.py shutdown
```

### Development Workflow
Use `list` and `show` actions for rule development and debugging:
```bash
# See all available rules
python3 programmatic_rules/rules_manager.py list

# Examine specific rule
python3 programmatic_rules/rules_manager.py show --rule my_rule

# Test startup behavior  
python3 programmatic_rules/rules_manager.py startup
```

## Future Enhancements

Potential future actions for the Rules Manager:
- `create`: Interactive rule creation wizard
- `edit`: Modify existing rules 
- `validate`: Check rule syntax and dependencies
- `activate`/`deactivate`: Toggle rule status
- `dependencies`: Show rule dependency graph
- `export`: Package rules for sharing
- `import`: Load rule sets from external sources 