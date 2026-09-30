import re


def analyze_security(code, language="python"):

    vulnerabilities = []

    lines = code.splitlines()

    # ==========================================
    # PYTHON SECURITY CHECKS
    # ==========================================

    if language.lower() == "python":

        for line_number, line in enumerate(lines, start=1):

            stripped = line.strip()

            # ----------------------------------
            # eval()
            # ----------------------------------

            if re.search(r'\beval\s*\(', stripped):

                vulnerabilities.append({
                    "severity": "High",
                    "type": "Dangerous eval() usage",
                    "line": line_number,
                    "message": (
                        "eval() can execute dynamically generated "
                        "Python code and may allow arbitrary code execution."
                    ),
                    "suggestion": (
                        "Avoid eval() when possible. Use safer parsing "
                        "or explicit input validation."
                    )
                })

            # ----------------------------------
            # exec()
            # ----------------------------------

            if re.search(r'\bexec\s*\(', stripped):

                vulnerabilities.append({
                    "severity": "High",
                    "type": "Dangerous exec() usage",
                    "line": line_number,
                    "message": (
                        "exec() can execute dynamically generated "
                        "Python code."
                    ),
                    "suggestion": (
                        "Avoid exec() with untrusted or user-controlled input."
                    )
                })

            # ----------------------------------
            # shell=True
            # ----------------------------------

            if "shell=True" in stripped:

                vulnerabilities.append({
                    "severity": "High",
                    "type": "Potential command injection",
                    "line": line_number,
                    "message": (
                        "Using shell=True can allow command injection "
                        "when command input is not properly controlled."
                    ),
                    "suggestion": (
                        "Avoid shell=True when possible and pass commands "
                        "as a list of arguments."
                    )
                })

            # ----------------------------------
            # Hard-coded password
            # ----------------------------------

            if re.search(
                r'(password|passwd|pwd|secret|api_key|apikey)\s*=\s*["\']',
                stripped,
                re.IGNORECASE
            ):

                vulnerabilities.append({
                    "severity": "High",
                    "type": "Hard-coded secret",
                    "line": line_number,
                    "message": (
                        "A password, secret, or API key appears to be "
                        "hard-coded in the source code."
                    ),
                    "suggestion": (
                        "Use environment variables or a secure "
                        "secret-management system."
                    )
                })

            # ----------------------------------
            # SQL string concatenation
            # ----------------------------------

            if re.search(
                r'(SELECT|INSERT|UPDATE|DELETE).*[\+\%]',
                stripped,
                re.IGNORECASE
            ):

                vulnerabilities.append({
                    "severity": "High",
                    "type": "Potential SQL injection",
                    "line": line_number,
                    "message": (
                        "SQL appears to be constructed using string "
                        "concatenation or formatting."
                    ),
                    "suggestion": (
                        "Use parameterized queries or prepared statements."
                    )
                })


    # ==========================================
    # JAVA SECURITY CHECKS
    # ==========================================

    elif language.lower() == "java":

        for line_number, line in enumerate(lines, start=1):

            stripped = line.strip()

            # ----------------------------------
            # Runtime.exec()
            # ----------------------------------

            if re.search(
                r'Runtime\.getRuntime\(\)\.exec\s*\(',
                stripped
            ):

                vulnerabilities.append({
                    "severity": "High",
                    "type": "Command execution",
                    "line": line_number,
                    "message": (
                        "Runtime.exec() executes operating-system "
                        "commands and may be dangerous with untrusted input."
                    ),
                    "suggestion": (
                        "Validate input carefully and avoid passing "
                        "user-controlled data to system commands."
                    )
                })

            # ----------------------------------
            # Hard-coded secret
            # ----------------------------------

            if re.search(
                r'(password|passwd|secret|apiKey|api_key|token)'
                r'\s*=\s*"',
                stripped,
                re.IGNORECASE
            ):

                vulnerabilities.append({
                    "severity": "High",
                    "type": "Hard-coded secret",
                    "line": line_number,
                    "message": (
                        "A password, secret, token, or API key appears "
                        "to be stored directly in the source code."
                    ),
                    "suggestion": (
                        "Use environment variables or a secure "
                        "secret-management system."
                    )
                })

            # ----------------------------------
            # Weak MD5
            # ----------------------------------

            if re.search(
                r'MessageDigest\.getInstance\s*\(\s*"MD5"',
                stripped,
                re.IGNORECASE
            ):

                vulnerabilities.append({
                    "severity": "Medium",
                    "type": "Weak hashing algorithm",
                    "line": line_number,
                    "message": (
                        "MD5 is considered cryptographically weak "
                        "for security-sensitive applications."
                    ),
                    "suggestion": (
                        "Use a modern cryptographic algorithm appropriate "
                        "for the security requirement."
                    )
                })

            # ----------------------------------
            # Weak SHA-1
            # ----------------------------------

            if re.search(
                r'MessageDigest\.getInstance\s*\(\s*"SHA-1"',
                stripped,
                re.IGNORECASE
            ):

                vulnerabilities.append({
                    "severity": "Medium",
                    "type": "Weak hashing algorithm",
                    "line": line_number,
                    "message": (
                        "SHA-1 is considered weak for many "
                        "security-sensitive applications."
                    ),
                    "suggestion": (
                        "Use a stronger modern hashing algorithm."
                    )
                })

            # ----------------------------------
            # SQL concatenation
            # ----------------------------------

            if re.search(
                r'(SELECT|INSERT|UPDATE|DELETE).*[\+]',
                stripped,
                re.IGNORECASE
            ):

                vulnerabilities.append({
                    "severity": "High",
                    "type": "Potential SQL injection",
                    "line": line_number,
                    "message": (
                        "SQL appears to be constructed using "
                        "string concatenation."
                    ),
                    "suggestion": (
                        "Use PreparedStatement with parameters "
                        "instead of concatenating user input."
                    )
                })


    # ==========================================
    # UNSUPPORTED LANGUAGE
    # ==========================================

    else:

        return {
            "success": False,
            "error": (
                f"Security analysis for {language} "
                "is not implemented yet."
            )
        }


    # ==========================================
    # RETURN RESULT
    # ==========================================

    return {
        "success": True,
        "vulnerabilities": vulnerabilities,
        "count": len(vulnerabilities)
    }