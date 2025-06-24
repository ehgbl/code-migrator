#!/usr/bin/env python3
"""
Python to C++ Migrator - Simple I/O Structure

"""

import sys
import os
import subprocess
import tempfile
import argparse
import openai

from pathlib import Path

input_file="input.py"
output_file="output.cpp"


def parse_arguments():
    parser = argparse.ArgumentParser(description='Python to C++/Rust Code Migrator')
    parser.add_argument('input_file', help='Input Python file to migrate')
    parser.add_argument('--target-language', '-t', default='cpp', 
                       choices=['cpp', 'rust'], help='Target language (default: cpp)')
    parser.add_argument('--output-path', '-o', help='Output file path (default: auto-generated)')
    parser.add_argument('--context', '-c', help='Additional context for migration')
    
    return parser.parse_args()

def get_output_path(input_file, target_language, user_output_path=None):
    if user_output_path:
        return user_output_path
    
    input_path = Path(input_file)
    if target_language == 'cpp':
        return input_path.stem + '.cpp'
    elif target_language == 'rust':
        return input_path.stem + '.rs'
    else:
        return input_path.stem + '.txt'

def read_python_file(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as input_file:
            return input_file.read()
    except FileNotFoundError:
        print(f"Error: File '{file}' not found")
        print(f"Error: File '{file}' not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def analyze_python_code(python_code):
    lines = python_code.split('\n')
    functions = [line for line in lines if line.strip().startswith('def ')]
    classes = [line for line in lines if line.strip().startswith('class ')]
    imports = [line for line in lines if line.strip().startswith(('import ', 'from '))]
    
    return {
        'functions': len(functions),
        'classes': len(classes),
        'imports': len(imports),
        'total_lines': len(lines)
    }


def convert_to_cpp(python_code, context=""):
    client = openai.OpenAI()

    try:
        
        
        
        prompt = f"""
Please translate the following Python code to C++.

Context: {context}

Python Code:
{python_code}

Please provide only the C++ code without any explanations or markdown formatting.
"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                
                {"role":"system","content":"You are a code migration assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.1
        )
        
        result = response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error calling API: {e}")
        return None

def convert_to_rust(python_code, context=""):
    """Convert Python code to Rust"""
    try:
        
        prompt = f"""
Please translate the following Python code to Rust.

Context: {context}

Python Code:
{python_code}

Please provide only the Rust code without any explanations or markdown formatting.
"""
        
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text.strip()
        
    except Exception as e:
        print(f"Error calling API: {e}")
        return None


def write_cpp_file(cpp_code, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(cpp_code)
        print(f"Successfully wrote C++ code to: {output_file}")
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False


def _write_temp_cpp_file(cpp_code, temp_dir):
    temp_cpp_file = os.path.join(temp_dir, "temp_code.cpp")
    with open(temp_cpp_file, 'w', encoding='utf-8') as f:
        f.write(cpp_code)
    return temp_cpp_file

def _run_gcc_compilation(temp_cpp_file, temp_dir):
    output_path = os.path.join(temp_dir, 'output')
    return subprocess.run(
        ['g++', '-std=c++17', '-o', output_path, temp_cpp_file],
        capture_output=True,
        text=True,
        timeout=30
    )

def compile_cpp_code(cpp_code, output_file):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_cpp_file = _write_temp_cpp_file(cpp_code, temp_dir)
            compile_result = _run_gcc_compilation(temp_cpp_file, temp_dir)
            
            if compile_result.returncode == 0:
                print("C++ code compiled successfully!")
                return True, None
            else:
                error_output = compile_result.stderr
                print(" C++ compilation failed!")
                print("Compilation errors:")
                print(error_output)
                return False, error_output
                
    except subprocess.TimeoutExpired:
        print("Compilation timed out")
        return False, "Compilation timed out after 30 seconds"
    except FileNotFoundError:
        print(" g++ not found - install g++ to compile C++ code")
        return False, "g++ compiler not found"
    except Exception as e:
        print(f"Compilation error: {e}")
        return False, str(e)


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <python_file> [context]")
        print("Example: python main.py my_script.py 'This is a simple calculator'")
        print("Usage: python main.py <python_file> [context]")
        print("Example: python main.py my_script.py 'This is a simple calculator'")
        sys.exit(1)
    python_file = sys.argv[1]
    context = sys.argv[2] if len(sys.argv) > 2 else ""
    
    args = parse_arguments()
    
    python_file = args.input_file
    target_language = args.target_language
    output_path = args.output_path
    context = args.context or ""
    
    print(f"Reading Python file: {python_file}")
    print(f"Target language: {target_language}")
    
    python_code = read_python_file(python_file)
    if python_code is None:
        print("Failed to read Python file. Exiting.")
        sys.exit(1)
    
    print(f"Successfully read {len(python_code.splitlines())} lines of Python code")
    
    analysis = analyze_python_code(python_code)
    print(f"Analysis: {analysis['functions']} functions, {analysis['classes']} classes, {analysis['imports']} imports")
    
    print(f"Converting to {target_language.upper()}...")
    if target_language == 'cpp':
        converted_code = convert_to_cpp(python_code, context)
    elif target_language == 'rust':
        converted_code = convert_to_rust(python_code, context)
    else:
        print(f"Unsupported target language: {target_language}")
        sys.exit(1)
    
    if converted_code is None:
        print("Failed to convert code. Exiting.")
        sys.exit(1)
    
    print(f"{target_language.upper()} code generated successfully!")
    
    if target_language == 'cpp':
        print("Validating C++ compilation...")
        compilation_success, compilation_errors = compile_cpp_code(converted_code, output_path)
        
        if not compilation_success:
            print("Compilation validation failed. Not saving invalid C++ code.")
            print("Please review the compilation errors above.")
            sys.exit(1)
    
    final_output_path = get_output_path(python_file, target_language, output_path)
    if write_cpp_file(converted_code, final_output_path):
        print(f"Translation complete! Output saved to: {final_output_path}")
    else:
        print("Failed to write output file.")
        sys.exit(1)


if __name__ == "__main__":
    main()

