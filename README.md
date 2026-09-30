# 🤖 AI Coding Agent

An AI-powered web application for analyzing, executing, debugging, explaining, and improving Python and Java programs.

The system combines static code analysis, runtime execution, error parsing, security analysis, code quality scoring, AI-assisted explanations, optimization suggestions, and automatic Python code fixing in a single dashboard.

---

## 📌 Overview

Traditional programming environments often provide error messages but require developers to manually identify the cause, understand the problem, and determine how to fix it.

The **AI Coding Agent** automates several parts of this debugging workflow.

A user can enter Python or Java code, select the programming language, and analyze the program through a web-based dashboard.

The system can:

- Analyze source code
- Detect potential coding issues
- Execute Python and Java programs
- Detect runtime and compilation errors
- Explain errors in beginner-friendly language
- Detect common security vulnerabilities
- Calculate a code quality score
- Generate optimization suggestions
- Automatically generate corrected Python code for supported runtime errors
- Execute the corrected Python code
- Maintain code analysis history
- Download analyzed or fixed code

---

# ✨ Features

## 1. 🔍 Static Code Analysis

The system analyzes source code before execution.

### Python

Python code is analyzed using the Python `ast` module.

The analyzer detects:

- Functions
- Classes
- Loops
- Conditional statements
- Variable assignments
- Return statements
- Imports
- Function calls
- Cyclomatic complexity
- Basic static warnings

### Java

Java source code is analyzed using pattern-based analysis.

The analyzer detects:

- Classes
- Methods
- Loops
- Conditional statements
- Assignments
- Return statements
- Imports
- Basic warnings
- Cyclomatic complexity

---

## 2. ▶️ Code Execution

The system supports local execution of:

- Python programs
- Java programs

### Python

Python programs are executed using the Python interpreter through `subprocess`.

### Java

Java programs are:

1. Saved temporarily
2. Compiled using `javac`
3. Executed using the Java runtime
4. Temporary files are removed after execution

Execution timeout controls help prevent programs from running indefinitely.

---

## 3. ❌ Runtime and Compilation Error Detection

The system identifies errors generated during execution or compilation.

### Python error examples

- `ZeroDivisionError`
- `IndexError`
- `KeyError`
- `NameError`
- `TypeError`
- `ValueError`
- `AttributeError`
- `FileNotFoundError`

### Java error examples

- `ArithmeticException`
- `NullPointerException`
- `ArrayIndexOutOfBoundsException`
- `StringIndexOutOfBoundsException`
- `NumberFormatException`
- `ClassCastException`
- `IllegalArgumentException`
- `FileNotFoundException`
- `IOException`

The system extracts information such as:

- Error type
- Error message
- Line number
- Explanation
- Suggested solution

---

# 🤖 AI-Powered Explanation

The project integrates Google's Gemini API for AI-assisted programming explanations.

The AI can explain:

1. What went wrong
2. Why the error occurred
3. Which part of the program caused the problem
4. How the problem can be fixed
5. Possible optimization improvements

The system also contains local fallback logic so that basic explanations and optimization suggestions can still be generated when the AI service is unavailable.

> **Note:** AI functionality depends on API availability and account quota.

---

# 🔧 Automatic Code Fixing

For supported Python runtime errors, the system can generate corrected code.

The workflow is:

```text
Python Code
     ↓
Execution
     ↓
Runtime Error
     ↓
Error Parser
     ↓
Code Fixer
     ↓
Corrected Python Code
     ↓
Re-execution