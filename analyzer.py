import ast


class CodeAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.functions = []
        self.classes = []
        self.loops = 0
        self.conditions = 0
        self.assignments = 0
        self.imports = []
        self.function_calls = []
        self.return_statements = 0
        self.warnings = []

    def visit_FunctionDef(self, node):
        self.functions.append({
            "name": node.name,
            "line": node.lineno,
            "parameters": len(node.args.args)
        })

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.functions.append({
            "name": node.name,
            "line": node.lineno,
            "parameters": len(node.args.args)
        })

        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append({
            "name": node.name,
            "line": node.lineno
        })

        self.generic_visit(node)

    def visit_For(self, node):
        self.loops += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.loops += 1
        self.generic_visit(node)

    def visit_If(self, node):
        self.conditions += 1
        self.generic_visit(node)

    def visit_Assign(self, node):
        self.assignments += 1
        self.generic_visit(node)

    def visit_Import(self, node):
        for name in node.names:
            self.imports.append(name.name)

        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.append(node.module)

        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.function_calls.append(node.func.id)

        elif isinstance(node.func, ast.Attribute):
            self.function_calls.append(node.func.attr)

        self.generic_visit(node)

    def visit_Return(self, node):
        self.return_statements += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if node.type is None:
            self.warnings.append(
                f"Line {node.lineno}: Bare 'except' detected. "
                "Consider catching a specific exception."
            )

        self.generic_visit(node)

    def visit_BinOp(self, node):
        if isinstance(node.op, (ast.Div, ast.FloorDiv)):

            if isinstance(node.right, ast.Constant):
                if node.right.value == 0:

                    self.warnings.append(
                        f"Line {node.lineno}: Possible division by zero."
                    )

        self.generic_visit(node)


def analyze_python_code(code):

    if not code.strip():
        return {
            "success": False,
            "error": "No code was entered."
        }

    try:
        tree = ast.parse(code)

    except SyntaxError as error:

        return {
            "success": False,
            "syntax_error": True,
            "error": error.msg,
            "line": error.lineno,
            "column": error.offset
        }

    analyzer = CodeAnalyzer()

    analyzer.visit(tree)

    complexity = (
        1
        + analyzer.conditions
        + analyzer.loops
    )

    return {
        "success": True,
        "syntax_error": False,

        "metrics": {
            "functions": len(analyzer.functions),
            "classes": len(analyzer.classes),
            "loops": analyzer.loops,
            "conditions": analyzer.conditions,
            "assignments": analyzer.assignments,
            "return_statements": analyzer.return_statements,
            "cyclomatic_complexity": complexity
        },

        "functions": analyzer.functions,

        "classes": analyzer.classes,

        "imports": analyzer.imports,

        "function_calls": analyzer.function_calls,

        "warnings": analyzer.warnings
    }


def analyze_code(code, language="python"):

    if language.lower() == "python":
        return analyze_python_code(code)

    return {
        "success": False,
        "error": f"{language} analysis is not implemented yet."
    }