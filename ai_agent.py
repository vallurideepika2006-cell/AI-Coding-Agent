import os
import json
import urllib.request
import urllib.error


def explain_code_problem(
    code,
    analysis,
    execution,
    error_details,
    language="python"
):

    def local_explanation():

        if not error_details:
            return (
                "The program encountered an error during "
                "execution. Review the execution output "
                "and check the reported line."
            )

        error_type = error_details.get(
            "type",
            "UnknownError"
        )

        line = error_details.get(
            "line"
        )

        explanation = error_details.get(
            "explanation",
            "The program encountered an error."
        )

        suggestion = error_details.get(
            "suggestion",
            "Review the code around the reported line."
        )

        line_text = (
            f"Line {line}"
            if line
            else "the reported line"
        )

        return (
            f"The program encountered a "
            f"{error_type} error at {line_text}.\n\n"
            f"Explanation: {explanation}\n\n"
            f"How to fix it: {suggestion}"
        )

    try:

        import os
        import json
        import urllib.request

        api_key = os.environ.get(
            "GEMINI_API_KEY"
        )

        if not api_key:
            return local_explanation()

        prompt = f"""
You are a programming debugging assistant.

Analyze the following {language} program and
explain the error clearly for a beginner.

Explain:

1. What went wrong
2. Why it happened
3. Which line caused the problem
4. How to fix it

Do not rewrite the complete program.

Use simple and clear language.

CODE:

{code}

STATIC ANALYSIS:

{json.dumps(analysis, indent=2)}

EXECUTION ERROR:

{json.dumps(execution, indent=2)}

ERROR DETAILS:

{json.dumps(error_details, indent=2)}
"""

        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-3.8-flash:generateContent"
            "?key="
            + api_key
        )

        request_data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        request = urllib.request.Request(
            url,
            data=json.dumps(
                request_data
            ).encode("utf-8"),
            headers={
                "Content-Type":
                "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            result = json.loads(
                response.read().decode(
                    "utf-8"
                )
            )

        return (
            result
            ["candidates"]
            [0]
            ["content"]
            ["parts"]
            [0]
            ["text"]
        )

    except Exception:
        return local_explanation()
def generate_optimization_suggestions(
    code,
    analysis,
    language="python"
):

    # ==========================================
    # LOCAL FALLBACK OPTIMIZATION
    # ==========================================

    def local_optimization():

        suggestions = []

        metrics = analysis.get(
            "metrics",
            {}
        )

        warnings = analysis.get(
            "warnings",
            []
        )

        functions = metrics.get(
            "functions",
            0
        )

        loops = metrics.get(
            "loops",
            0
        )

        conditions = metrics.get(
            "conditions",
            0
        )

        complexity = metrics.get(
            "cyclomatic_complexity",
            1
        )

        assignments = metrics.get(
            "assignments",
            0
        )


        # ==========================================
        # COMPLEXITY
        # ==========================================

        if complexity > 10:

            suggestions.append(
                "• High cyclomatic complexity detected. "
                "Consider breaking the code into smaller functions."
            )

        elif complexity > 5:

            suggestions.append(
                "• Moderate code complexity detected. "
                "Consider simplifying conditions and loops."
            )

        else:

            suggestions.append(
                "• The code has relatively low cyclomatic complexity."
            )


        # ==========================================
        # LOOPS
        # ==========================================

        if loops > 2:

            suggestions.append(
                "• Multiple loops were detected. "
                "Check whether some loops can be simplified "
                "or combined."
            )

        elif loops == 1:

            suggestions.append(
                "• A loop is present. Check whether a built-in "
                "function or more direct approach could simplify it."
            )


        # ==========================================
        # FUNCTIONS
        # ==========================================

        if functions == 0 and len(code.splitlines()) > 15:

            suggestions.append(
                "• Consider dividing longer code into functions "
                "to improve readability and maintainability."
            )

        elif functions > 0:

            suggestions.append(
                "• Functions are being used, which helps organize "
                "the program into reusable components."
            )


        # ==========================================
        # CONDITIONS
        # ==========================================

        if conditions > 3:

            suggestions.append(
                "• Several conditional statements were detected. "
                "Consider simplifying complex decision logic."
            )


        # ==========================================
        # ASSIGNMENTS
        # ==========================================

        if assignments > 8:

            suggestions.append(
                "• Many variable assignments were detected. "
                "Check whether some temporary variables can be removed."
            )


        # ==========================================
        # WARNINGS
        # ==========================================

        if warnings:

            suggestions.append(
                "• Static analysis warnings were detected. "
                "Resolve these warnings to improve code quality."
            )

        else:

            suggestions.append(
                "• No static analysis warnings were detected."
            )


        # ==========================================
        # GENERAL SUGGESTIONS
        # ==========================================

        suggestions.append(
            "• Use meaningful variable and function names "
            "to improve code readability."
        )

        suggestions.append(
            "• Avoid unnecessary calculations and repeated "
            "operations where possible."
        )

        suggestions.append(
            "• Keep functions focused on a single responsibility "
            "for easier maintenance."
        )


        return "\n".join(
            suggestions
        )


    # ==========================================
    # TRY GEMINI AI FIRST
    # ==========================================

    try:

        import os
        import json
        import urllib.request
        import urllib.error


        api_key = os.environ.get(
            "GEMINI_API_KEY"
        )


        # ==========================================
        # IF API KEY IS NOT AVAILABLE
        # ==========================================

        if not api_key:

            return local_optimization()


        prompt = f"""
Analyze the following {language} code and provide
useful optimization suggestions.

Focus on:

1. Performance
2. Readability
3. Maintainability
4. Code structure
5. Unnecessary operations
6. Better programming practices

Do not rewrite the complete code.

Provide clear bullet-point suggestions.

CODE:

{code}

STATIC ANALYSIS:

{json.dumps(analysis, indent=2)}
"""


        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-3.8-flash:generateContent"
            "?key="
            + api_key
        )


        request_data = {

            "contents": [

                {
                    "parts": [

                        {
                            "text": prompt
                        }

                    ]
                }

            ]

        }


        request = urllib.request.Request(

            url,

            data=json.dumps(
                request_data
            ).encode("utf-8"),

            headers={
                "Content-Type":
                "application/json"
            },

            method="POST"
        )


        # ==========================================
        # GEMINI REQUEST
        # ==========================================

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            result = json.loads(
                response.read().decode(
                    "utf-8"
                )
            )


        # ==========================================
        # EXTRACT AI RESPONSE
        # ==========================================

        return (
            result
            ["candidates"]
            [0]
            ["content"]
            ["parts"]
            [0]
            ["text"]
        )


    # ==========================================
    # GEMINI QUOTA / SERVER ERROR
    # ==========================================

    except (
        urllib.error.HTTPError,
        urllib.error.URLError,
        TimeoutError,
        Exception
    ):

        return local_optimization()