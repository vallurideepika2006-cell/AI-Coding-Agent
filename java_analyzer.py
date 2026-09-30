import re


def analyze_java_code(code):

    if not code.strip():
        return {
            "success": False,
            "error": "No code was entered."
        }

    functions = []
    classes = []
    loops = 0
    conditions = 0
    assignments = 0
    imports = []
    warnings = []
    return_statements = 0

    lines = code.splitlines()

    # --------------------------------
    # IMPORTS
    # --------------------------------

    for line_number, line in enumerate(lines, start=1):

        stripped = line.strip()

        if stripped.startswith("import "):

            import_name = stripped[7:].rstrip(";")

            imports.append(import_name)

    # --------------------------------
    # CLASSES
    # --------------------------------

    class_pattern = re.compile(
        r'\bclass\s+([A-Za-z_][A-Za-z0-9_]*)'
    )

    for line_number, line in enumerate(lines, start=1):

        match = class_pattern.search(line)

        if match:

            classes.append({
                "name": match.group(1),
                "line": line_number
            })

    # --------------------------------
    # METHODS
    # --------------------------------

    method_pattern = re.compile(
        r'(?:public|private|protected|static|final|synchronized|\s)*'
        r'(?:void|int|double|float|long|short|byte|boolean|char|String|'
        r'[A-Za-z_][A-Za-z0-9_<>\[\]]*)\s+'
        r'([A-Za-z_][A-Za-z0-9_]*)\s*'
        r'\(([^)]*)\)'
    )

    for line_number, line in enumerate(lines, start=1):

        match = method_pattern.search(line)

        if match:

            method_name = match.group(1)

            parameters = match.group(2).strip()

            if parameters == "":
                parameter_count = 0
            else:
                parameter_count = len(parameters.split(","))

            # Avoid treating common control statements as methods

            if method_name not in [
                "if",
                "for",
                "while",
                "switch",
                "catch"
            ]:

                functions.append({
                    "name": method_name,
                    "line": line_number,
                    "parameters": parameter_count
                })

    # --------------------------------
    # LOOPS
    # --------------------------------

    for line in lines:

        stripped = line.strip()

        if re.search(r'\bfor\s*\(', stripped):
            loops += 1

        if re.search(r'\bwhile\s*\(', stripped):
            loops += 1

        if re.search(r'\bdo\s*\{?', stripped):
            loops += 1

    # --------------------------------
    # CONDITIONS
    # --------------------------------

    for line in lines:

        stripped = line.strip()

        if re.search(r'\bif\s*\(', stripped):
            conditions += 1

        if re.search(r'\belse\s+if\s*\(', stripped):
            conditions += 1

        if re.search(r'\bswitch\s*\(', stripped):
            conditions += 1

    # --------------------------------
    # ASSIGNMENTS
    # --------------------------------

    for line in lines:

        stripped = line.strip()

        if (
            "=" in stripped
            and "==" not in stripped
            and "!=" not in stripped
            and ">=" not in stripped
            and "<=" not in stripped
            and "=>" not in stripped
        ):
            assignments += 1

    # --------------------------------
    # RETURN STATEMENTS
    # --------------------------------

    for line in lines:

        if re.search(r'\breturn\b', line):

            return_statements += 1

    # --------------------------------
    # WARNINGS
    # --------------------------------

    for line_number, line in enumerate(lines, start=1):

        stripped = line.strip()

        # System.out.println without newline is not a problem,
        # so we don't warn about normal output.

        # Empty catch block

        if stripped.startswith("catch") and line_number < len(lines):

            next_line = lines[line_number].strip()

            if next_line == "}":
                warnings.append(
                    f"Line {line_number}: Empty catch block detected."
                )

        # Possible division by zero

        if re.search(r'/\s*0\b', stripped):

            warnings.append(
                f"Line {line_number}: Possible division by zero."
            )

    # --------------------------------
    # COMPLEXITY
    # --------------------------------

    complexity = 1 + loops + conditions

    return {
        "success": True,
        "syntax_error": False,

        "metrics": {
            "functions": len(functions),
            "classes": len(classes),
            "loops": loops,
            "conditions": conditions,
            "assignments": assignments,
            "return_statements": return_statements,
            "cyclomatic_complexity": complexity
        },

        "functions": functions,

        "classes": classes,

        "imports": imports,

        "function_calls": [],

        "warnings": warnings
    }