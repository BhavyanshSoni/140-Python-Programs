# AI-Powered Code Comment Generator (Offline)

A local tool that analyzes Python code files and automatically generates meaningful comments and documentation without using any external APIs. The tool uses advanced heuristics and pattern recognition to understand code structure and purpose, making it easier for developers to maintain code.

## Features

- **100% Offline**: No internet connection required, no external API calls
- **Smart Pattern Recognition**: Identifies common coding patterns and naming conventions
- **Comprehensive Analysis**: Analyzes functions, classes, methods, and their relationships
- **Intelligent Comment Generation**: Creates meaningful docstrings based on code structure
- **Batch Processing**: Process single files or entire directories
- **Flexible Output**: Generate new files or overwrite existing ones
- **Complexity Analysis**: Identifies complex functions that may need refactoring

## How It Works

The tool uses several offline techniques to generate meaningful comments:

1. **AST (Abstract Syntax Tree) Analysis**: Parses Python code to understand structure
2. **Pattern Recognition**: Identifies common function/class naming patterns
3. **Heuristic Analysis**: Uses predefined rules to determine code purpose
4. **Complexity Metrics**: Calculates function complexity to provide insights
5. **Type Annotation Analysis**: Extracts and documents parameter types

## Installation

No installation required! This tool uses only Python standard library modules.

```bash
# Clone or download the project
git clone <repository-url>
cd ai-code-comment-generator

# The tool is ready to use
python main.py --help
```

## Usage

### Basic Usage

```bash
# Process a single file
python main.py your_file.py

# Process a file and overwrite it
python main.py your_file.py --overwrite

# Process a file and specify output
python main.py your_file.py -o output_file.py

# Process all Python files in a directory
python main.py your_directory/

# Process directory with verbose output
python main.py your_directory/ --verbose
```

### Command Line Options

- `path`: Python file or directory to process
- `-o, --output`: Output file or directory
- `--overwrite`: Overwrite original files
- `--verbose, -v`: Verbose output
- `-h, --help`: Show help message

## Examples

### Example 1: Simple Function

**Input:**
```python
def calculate_area(length, width):
    return length * width
```

**Output:**
```python
def calculate_area(length, width):
    """Calculates or computes calculate_area with parameters: length, width. Returns None."""
    return length * width
```

### Example 2: Class with Methods

**Input:**
```python
class UserManager:
    def __init__(self, database):
        self.db = database
    
    def get_user(self, user_id):
        return self.db.find_user(user_id)
    
    def create_user(self, user_data):
        return self.db.insert_user(user_data)
```

**Output:**
```python
class UserManager:
    """Manages and coordinates class UserManager. Contains 3 methods."""
    
    def __init__(self, database):
        """Creates or initializes __init__ with parameters: database. Returns None."""
        self.db = database
    
    def get_user(self, user_id):
        """Retrieves or fetches get_user with parameters: user_id. Returns None."""
        return self.db.find_user(user_id)
    
    def create_user(self, user_data):
        """Creates or initializes create_user with parameters: user_data. Returns None."""
        return self.db.insert_user(user_data)
```

## Pattern Recognition

The tool recognizes these common patterns:

### Function Patterns
- `get_*`: Retrieves or fetches
- `set_*`: Sets or updates
- `is_*`: Checks if
- `has_*`: Checks if contains
- `add_*`: Adds or appends
- `remove_*`: Removes or deletes
- `create_*`: Creates or initializes
- `update_*`: Updates or modifies
- `delete_*`: Deletes or removes
- `validate_*`: Validates or checks
- `parse_*`: Parses or converts
- `format_*`: Formats or converts
- `calculate_*`: Calculates or computes
- `process_*`: Processes or handles
- `generate_*`: Generates or creates
- `find_*`: Finds or searches
- `sort_*`: Sorts or arranges
- `filter_*`: Filters or selects
- `transform_*`: Transforms or converts
- `convert_*`: Converts or transforms

### Class Patterns
- `*Manager`: Manages and coordinates
- `*Handler`: Handles and processes
- `*Service`: Provides service functionality
- `*Factory`: Creates and manufactures objects
- `*Builder`: Builds and constructs objects
- `*Config`: Manages configuration
- `*Client`: Client interface
- `*Server`: Server implementation

## Advanced Features

### Complexity Analysis
The tool calculates function complexity based on:
- Number of conditional statements (if/else)
- Number of loops (for/while)
- Number of try/except blocks
- Nested control structures

Functions with complexity > 5 are flagged with a note.

### Type Annotation Support
The tool analyzes and documents:
- Function parameter types
- Return types
- Class inheritance
- Generic types

### Batch Processing
Process entire projects with:
- Recursive directory scanning
- Preserved directory structure
- Error handling and reporting
- Progress tracking

## Limitations

- Only works with Python files (.py)
- Requires valid Python syntax
- Comments are generated based on patterns and heuristics
- May not capture complex business logic context
- Does not analyze external dependencies

## Contributing

Contributions are welcome! Areas for improvement:
- Additional pattern recognition
- Better complexity metrics
- Support for more code structures
- Enhanced comment quality
- Integration with other tools

## License

This project is open source and available under the MIT License.

## Support

If you encounter issues or have suggestions:
1. Check the examples above
2. Ensure your Python files have valid syntax
3. Try the `--verbose` flag for more information
4. Report issues with sample code that reproduces the problem 