#!/usr/bin/env python3
"""
AI-Powered Code Comment Generator (Offline)
A local tool that analyzes Python code files and automatically generates meaningful comments
and documentation without using any external APIs.
"""

import ast
import argparse
import os
import re
import sys
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import tokenize
from io import StringIO


class CodeAnalyzer:
    """Analyzes Python code structure and extracts meaningful information."""
    
    def __init__(self):
        self.common_patterns = {
            'get_': 'Retrieves or fetches',
            'set_': 'Sets or updates',
            'is_': 'Checks if',
            'has_': 'Checks if contains',
            'add_': 'Adds or appends',
            'remove_': 'Removes or deletes',
            'create_': 'Creates or initializes',
            'update_': 'Updates or modifies',
            'delete_': 'Deletes or removes',
            'validate_': 'Validates or checks',
            'parse_': 'Parses or converts',
            'format_': 'Formats or converts',
            'calculate_': 'Calculates or computes',
            'process_': 'Processes or handles',
            'generate_': 'Generates or creates',
            'find_': 'Finds or searches',
            'sort_': 'Sorts or arranges',
            'filter_': 'Filters or selects',
            'transform_': 'Transforms or converts',
            'convert_': 'Converts or transforms'
        }
        
        self.data_types = {
            'str': 'string',
            'int': 'integer',
            'float': 'floating point number',
            'bool': 'boolean',
            'list': 'list',
            'dict': 'dictionary',
            'tuple': 'tuple',
            'set': 'set',
            'bytes': 'bytes',
            'None': 'None value'
        }
    
    def analyze_function(self, func_node: ast.FunctionDef) -> Dict:
        """Analyzes a function and extracts meaningful information."""
        analysis = {
            'name': func_node.name,
            'args': [],
            'returns': None,
            'docstring': ast.get_docstring(func_node),
            'complexity': 0,
            'purpose': '',
            'suggested_comment': ''
        }
        
        # Analyze arguments
        for arg in func_node.args.args:
            arg_info = {
                'name': arg.arg,
                'annotation': self._get_annotation_name(arg.annotation) if arg.annotation else None,
                'default': None
            }
            analysis['args'].append(arg_info)
        
        # Analyze return type
        if func_node.returns:
            analysis['returns'] = self._get_annotation_name(func_node.returns)
        
        # Calculate complexity (simple metric)
        analysis['complexity'] = self._calculate_complexity(func_node)
        
        # Determine purpose based on name patterns
        analysis['purpose'] = self._determine_purpose(func_node.name)
        
        # Generate suggested comment
        analysis['suggested_comment'] = self._generate_function_comment(analysis)
        
        return analysis
    
    def analyze_class(self, class_node: ast.ClassDef) -> Dict:
        """Analyzes a class and extracts meaningful information."""
        analysis = {
            'name': class_node.name,
            'bases': [self._get_annotation_name(base) for base in class_node.bases],
            'docstring': ast.get_docstring(class_node),
            'methods': [],
            'attributes': [],
            'purpose': '',
            'suggested_comment': ''
        }
        
        # Analyze methods
        for item in class_node.body:
            if isinstance(item, ast.FunctionDef):
                method_analysis = self.analyze_function(item)
                analysis['methods'].append(method_analysis)
        
        # Determine purpose
        analysis['purpose'] = self._determine_class_purpose(class_node.name, analysis['methods'])
        
        # Generate suggested comment
        analysis['suggested_comment'] = self._generate_class_comment(analysis)
        
        return analysis
    
    def _get_annotation_name(self, annotation) -> str:
        """Extracts the name from a type annotation."""
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Attribute):
            return f"{self._get_annotation_name(annotation.value)}.{annotation.attr}"
        elif isinstance(annotation, ast.Subscript):
            return f"{self._get_annotation_name(annotation.value)}[{self._get_annotation_name(annotation.slice)}]"
        return str(annotation)
    
    def _calculate_complexity(self, func_node: ast.FunctionDef) -> int:
        """Calculates a simple complexity metric for a function."""
        complexity = 0
        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler)):
                complexity += 1
        return complexity
    
    def _determine_purpose(self, func_name: str) -> str:
        """Determines the purpose of a function based on its name."""
        func_name_lower = func_name.lower()
        
        for pattern, description in self.common_patterns.items():
            if func_name_lower.startswith(pattern):
                return description
        
        # Additional heuristics
        if func_name_lower.endswith('_handler'):
            return "Handles or processes"
        elif func_name_lower.endswith('_manager'):
            return "Manages or controls"
        elif func_name_lower.endswith('_service'):
            return "Provides service or functionality"
        elif func_name_lower.endswith('_factory'):
            return "Creates or manufactures"
        elif func_name_lower.endswith('_builder'):
            return "Builds or constructs"
        
        return "Performs operation"
    
    def _determine_class_purpose(self, class_name: str, methods: List[Dict]) -> str:
        """Determines the purpose of a class based on its name and methods."""
        class_name_lower = class_name.lower()
        
        # Check for common class patterns
        if class_name_lower.endswith('manager'):
            return "Manages and coordinates"
        elif class_name_lower.endswith('handler'):
            return "Handles and processes"
        elif class_name_lower.endswith('service'):
            return "Provides service functionality"
        elif class_name_lower.endswith('factory'):
            return "Creates and manufactures objects"
        elif class_name_lower.endswith('builder'):
            return "Builds and constructs objects"
        elif class_name_lower.endswith('config'):
            return "Manages configuration"
        elif class_name_lower.endswith('client'):
            return "Client interface"
        elif class_name_lower.endswith('server'):
            return "Server implementation"
        
        # Analyze methods to determine purpose
        method_names = [method['name'].lower() for method in methods]
        if any('get' in name for name in method_names):
            return "Data access and retrieval"
        elif any('set' in name for name in method_names):
            return "Data modification and storage"
        elif any('process' in name for name in method_names):
            return "Data processing and transformation"
        
        return "Represents a data structure or entity"
    
    def _generate_function_comment(self, analysis: Dict) -> str:
        """Generates a comprehensive function comment."""
        name = analysis['name']
        purpose = analysis['purpose']
        args = analysis['args']
        returns = analysis['returns']
        
        # Build argument description
        arg_descriptions = []
        for arg in args:
            arg_desc = arg['name']
            if arg['annotation']:
                arg_desc += f" ({arg['annotation']})"
            arg_descriptions.append(arg_desc)
        
        # Build comment
        comment = f"{purpose} {name}"
        if arg_descriptions:
            comment += f" with parameters: {', '.join(arg_descriptions)}"
        
        if returns:
            comment += f". Returns {returns}."
        else:
            comment += "."
        
        # Add complexity note
        if analysis['complexity'] > 5:
            comment += " Note: This function has high complexity."
        
        return comment
    
    def _generate_class_comment(self, analysis: Dict) -> str:
        """Generates a comprehensive class comment."""
        name = analysis['name']
        purpose = analysis['purpose']
        bases = analysis['bases']
        methods = analysis['methods']
        
        comment = f"{purpose} class {name}"
        
        if bases:
            comment += f" inheriting from {', '.join(bases)}"
        
        comment += f". Contains {len(methods)} methods."
        
        return comment


class CommentGenerator:
    """Generates and inserts comments into Python code."""
    
    def __init__(self):
        self.analyzer = CodeAnalyzer()
    
    def process_file(self, file_path: str, output_path: Optional[str] = None, 
                    overwrite: bool = False) -> str:
        """Processes a Python file and adds comments."""
        if output_path is None:
            if overwrite:
                output_path = file_path
            else:
                base_name = Path(file_path).stem
                output_path = f"{base_name}_commented.py"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse the code
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            return f"Error: Invalid Python syntax in {file_path}: {e}"
        
        # Generate comments
        commented_source = self._add_comments_to_source(source, tree)
        
        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(commented_source)
        
        return f"Successfully processed {file_path} -> {output_path}"
    
    def _add_comments_to_source(self, source: str, tree: ast.AST) -> str:
        """Adds comments to the source code."""
        lines = source.split('\n')
        comments_to_add = {}
        
        # Analyze and collect comments
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    analysis = self.analyzer.analyze_function(node)
                    comments_to_add[node.lineno] = analysis['suggested_comment']
            
            elif isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    analysis = self.analyzer.analyze_class(node)
                    comments_to_add[node.lineno] = analysis['suggested_comment']
        
        # Insert comments
        new_lines = []
        for i, line in enumerate(lines, 1):
            if i in comments_to_add:
                # Add docstring comment
                indent = len(line) - len(line.lstrip())
                comment = comments_to_add[i]
                docstring = f'"""{comment}"""'
                new_lines.append(' ' * indent + docstring)
            
            new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def process_directory(self, directory_path: str, output_dir: Optional[str] = None,
                         overwrite: bool = False) -> List[str]:
        """Processes all Python files in a directory."""
        results = []
        directory = Path(directory_path)
        
        if output_dir is None and not overwrite:
            output_dir = directory / "commented"
            output_dir.mkdir(exist_ok=True)
        
        for py_file in directory.rglob("*.py"):
            if output_dir and not overwrite:
                relative_path = py_file.relative_to(directory)
                output_path = output_dir / relative_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                output_path = None
            
            try:
                result = self.process_file(str(py_file), str(output_path) if output_path else None, overwrite)
                results.append(result)
            except Exception as e:
                results.append(f"Error processing {py_file}: {e}")
        
        return results


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="AI-Powered Code Comment Generator (Offline)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py file.py                    # Process single file
  python main.py file.py -o                 # Overwrite original file
  python main.py file.py -o output.py       # Specify output file
  python main.py directory/                 # Process all .py files in directory
  python main.py directory/ -o              # Overwrite all files in directory
        """
    )
    
    parser.add_argument('path', help='Python file or directory to process')
    parser.add_argument('-o', '--output', help='Output file or directory')
    parser.add_argument('--overwrite', action='store_true', 
                       help='Overwrite original files')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    generator = CommentGenerator()
    
    if os.path.isfile(args.path):
        if not args.path.endswith('.py'):
            print("Error: Input must be a Python file (.py)")
            sys.exit(1)
        
        result = generator.process_file(args.path, args.output, args.overwrite)
        print(result)
    
    elif os.path.isdir(args.path):
        results = generator.process_directory(args.path, args.output, args.overwrite)
        for result in results:
            if args.verbose or result.startswith("Error"):
                print(result)
        print(f"\nProcessed {len(results)} files.")
    
    else:
        print(f"Error: Path '{args.path}' does not exist")
        sys.exit(1)


if __name__ == "__main__":
    main()
