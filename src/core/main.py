#!/usr/bin/env python3
"""
Python to C++ Migrator - Simple I/O Structure
Just function signatures with TODOs.
"""

import sys
import os
import anthropic
import subprocess
import tempfile
from pathlib import Path

input_file="input.py"
output_file="output.cpp"
def read_python_file(input_file):
    """TODO: Read Python input_file and return contents"""
    try:
        with open(input_file, 'r', encoding='utf-8') as input_file:
            return input_file.read()
    except FileNotFoundError:
        print(f"Error: File '{file}' not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def analyze_python_code(python_code):
    """TODO: Analyze Python code structure (functions, classes, imports)"""
    # Simple analysis - count functions, classes, imports
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
    """TODO: Convert Python code to C++"""
    try:
        
        client = anthropic.Anthropic()
        
        prompt = f"""
Please translate the following Python code to C++.

Context: {context}

Python Code:
{python_code}

Please provide only the C++ code without any explanations or markdown formatting.
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
    """TODO: Write C++ code to output file"""
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
    """Compile C++ code using g++ and validate it builds successfully"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_cpp_file = _write_temp_cpp_file(cpp_code, temp_dir)
            compile_result = _run_gcc_compilation(temp_cpp_file, temp_dir)
            
            if compile_result.returncode == 0:
                print("✅ C++ code compiled successfully!")
                return True, None
            else:
                error_output = compile_result.stderr
                print("❌ C++ compilation failed!")
                print("Compilation errors:")
                print(error_output)
                return False, error_output
                
    except subprocess.TimeoutExpired:
        print("❌ Compilation timed out")
        return False, "Compilation timed out after 30 seconds"
    except FileNotFoundError:
        print("❌ g++ not found - install g++ to compile C++ code")
        return False, "g++ compiler not found"
    except Exception as e:
        print(f"❌ Compilation error: {e}")
        return False, str(e)


def main():
    """TODO: Main I/O flow"""
    # Step 1: Get input file from command line
    if len(sys.argv) < 2:
        print("Usage: python main.py <python_file> [context]")
        print("Example: python main.py my_script.py 'This is a simple calculator'")
        sys.exit(1)
    
    python_file = sys.argv[1]
    context = sys.argv[2] if len(sys.argv) > 2 else ""
    
    print(f"Reading Python file: {python_file}")
    
    # Step 2: Read Python file
    python_code = read_python_file(python_file)
    if python_code is None:
        print("Failed to read Python file. Exiting.")
        sys.exit(1)
    
    print(f"Successfully read {len(python_code.splitlines())} lines of Python code")
    
    # Step 3: Analyze code
    analysis = analyze_python_code(python_code)
    print(f"Analysis: {analysis['functions']} functions, {analysis['classes']} classes, {analysis['imports']} imports")
    
    # Step 4: Convert to C++
    print("Converting to C++...")
    cpp_code = convert_to_cpp(python_code, context)
    if cpp_code is None:
        print("Failed to convert code. Exiting.")
        sys.exit(1)
    
    print("C++ code generated successfully!")
    
    # Step 5: Validate compilation
    print("Validating C++ compilation...")
    compilation_success, compilation_errors = compile_cpp_code(cpp_code, output_file)
    
    if not compilation_success:
        print("❌ Compilation validation failed. Not saving invalid C++ code.")
        print("Please review the compilation errors above.")
        sys.exit(1)
    
    # Step 6: Write output file (only if compilation succeeded)
    input_path = Path(python_file)
    output_file = input_path.stem + ".cpp"
    if write_cpp_file(cpp_code, output_file):
        print(f"✅ Translation complete! Output saved to: {output_file}")
    else:
        print("Failed to write output file.")
        sys.exit(1)


if __name__ == "__main__":
    main()

