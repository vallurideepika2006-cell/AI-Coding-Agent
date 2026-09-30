# 🤖 AI Coding Agent

An AI-powered web application for analyzing, executing,
explaining and improving Python and Java programs.

## 🚀 Features

- Python static code analysis
- Java static code analysis
- Python code execution
- Java compilation and execution
- Runtime error detection
- Java compiler/runtime error parsing
- AI-powered error explanation
- AI-generated Python code fixes
- Security vulnerability detection
- Code quality scoring
- Cyclomatic complexity analysis
- AI optimization suggestions
- Code analysis history
- Download analyzed code
- Download fixed code
- Professional web dashboard

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- FastAPI
- Pydantic

### Code Analysis

- Python AST
- Java static analysis using pattern analysis
- Regular expressions

### AI

- Google Gemini API

### Execution

- Python subprocess
- Java JDK
- javac
- java

## 🏗️ Project Architecture

User

↓

Frontend

↓

FastAPI Backend

↓

Static Analyzer
Security Analyzer
Quality Analyzer
Python/Java Executor
Error Parser
AI Agent
Code Fixer

↓

Results Dashboard

## 📁 Project Structure

AI-Agent/

├── frontend/

│   ├── index.html

│   ├── style.css

│   └── script.js

├── analyzer.py

├── java_analyzer.py

├── executor.py

├── error_parser.py

├── java_error_parser.py

├── security_analyzer.py

├── quality_analyzer.py

├── ai_agent.py

├── code_fixer.py

├── main.py

├── test_security.py

└── README.md

## ▶️ How to Run

### 1. Open the project

Open the AI-Agent folder in VS Code.

### 2. Activate virtual environment

Windows PowerShell:

    .\venv\Scripts\Activate.ps1

### 3. Set Gemini API key

    $env:GEMINI_API_KEY="YOUR_API_KEY"

### 4. Start the server

    python -m uvicorn main:app --port 8001

### 5. Open the application

Open:

    http://127.0.0.1:8001/app

## 🧪 Example

Python input:

    numbers = [1, 2, 3, 4, 5]

    result = 0

    for n in numbers:
        result += n

    print(result)

The system performs:

1. Static analysis
2. Security analysis
3. Quality scoring
4. Program execution
5. Optimization suggestions

## 🔐 Security Analysis

The application checks for patterns such as:

- Dangerous eval()
- Dangerous exec()
- shell=True
- Hard-coded secrets
- Potential SQL injection
- Runtime command execution
- Weak hashing algorithms

## 📊 Code Quality

The quality analyzer considers:

- Static analysis warnings
- Cyclomatic complexity
- Security vulnerabilities

The result is displayed as a score from 0 to 100.

## 🤖 AI Capabilities

The AI component can:

- Explain runtime errors
- Suggest optimization techniques
- Generate corrected Python code

A local fallback mechanism is also available when the
AI API is unavailable.

## 🎯 Future Improvements

- Support additional programming languages
- Advanced AST-based Java analysis
- User authentication
- Database-backed code history
- More advanced security analysis
- Real-time code suggestions
- Docker-based secure code execution
- Detailed downloadable reports
- Cloud deployment

## 👩‍💻 Author

BTech Information Technology Student

## 📌 Project Type

AI / Software Development / Code Analysis