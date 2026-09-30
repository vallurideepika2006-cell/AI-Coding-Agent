from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from analyzer import analyze_code
from java_analyzer import analyze_java_code

from security_analyzer import analyze_security

from quality_analyzer import calculate_quality_score

from executor import (
    execute_python_code,
    execute_java_code
)

from error_parser import parse_runtime_error
from java_error_parser import parse_java_error

from ai_agent import (
    explain_code_problem,
    generate_optimization_suggestions
)

from code_fixer import generate_fixed_code


app = FastAPI(
    title="AI Coding Agent",
    description=(
        "AI-powered code analysis, execution, "
        "explanation and fixing system"
    ),
    version="1.0"
)


# ==========================================
# FRONTEND
# ==========================================

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)


@app.get("/app")
def home():

    return FileResponse(
        "frontend/index.html"
    )


# ==========================================
# REQUEST MODEL
# ==========================================

class CodeRequest(BaseModel):

    code: str
    language: str = "python"


# ==========================================
# ANALYZE CODE
# ==========================================

@app.post("/analyze")
def analyze(request: CodeRequest):

    # ==========================================
    # STATIC ANALYSIS
    # ==========================================

    if request.language.lower() == "java":

        analysis = analyze_java_code(
            request.code
        )

    else:

        analysis = analyze_code(
            request.code,
            request.language
        )


    # ==========================================
    # SECURITY ANALYSIS
    # ==========================================

    security = analyze_security(
        request.code,
        request.language
    )


    # ==========================================
    # CODE QUALITY SCORE
    # ==========================================

    if analysis["success"]:

        quality = calculate_quality_score(
            analysis,
            security
        )

    else:

        quality = {
            "score": 0,
            "level": "Unable to calculate",
            "warnings": 0,
            "complexity": 0,
            "security_issues": 0
        }


    # ==========================================
    # STATIC ANALYSIS FAILURE
    # ==========================================

    if not analysis["success"]:

        return {

            "analysis": analysis,

            "security": security,

            "quality": quality,

            "optimization_suggestions": None,

            "execution": {
                "success": False,
                "output": "",
                "error": analysis.get(
                    "error",
                    "Code analysis failed."
                )
            },

            "error_details": None,

            "ai_explanation": None,

            "fixed_code": None,

            "fixed_execution": None
        }


    # ==========================================
    # AI OPTIMIZATION SUGGESTIONS
    # ==========================================

    optimization_suggestions = (
        generate_optimization_suggestions(
            request.code,
            analysis,
            request.language
        )
    )


    # ==========================================
    # CODE EXECUTION
    # ==========================================

    if request.language.lower() == "java":

        execution = execute_java_code(
            request.code
        )

    else:

        execution = execute_python_code(
            request.code
        )


    # ==========================================
    # ERROR PARSING
    # ==========================================

    error_details = None


    if not execution["success"]:

        if request.language.lower() == "python":

            error_details = parse_runtime_error(
                execution["error"]
            )

        else:

            error_details = parse_java_error(
                execution["error"]
            )


    # ==========================================
    # AI EXPLANATION
    # ==========================================

    ai_explanation = None


    if not execution["success"]:

        ai_explanation = explain_code_problem(
            request.code,
            analysis,
            execution,
            error_details,
            request.language
        )


    # ==========================================
    # AI FIXED CODE
    # ==========================================

    fixed_code = None

    fixed_execution = None


    if (
        not execution["success"]
        and request.language.lower() == "python"
    ):

        fixed_code = generate_fixed_code(
            request.code,
            error_details
        )


        if fixed_code:

            fixed_execution = execute_python_code(
                fixed_code
            )


    # ==========================================
    # FINAL RESPONSE
    # ==========================================

    return {

        "analysis": analysis,

        "security": security,

        "quality": quality,

        "optimization_suggestions":
            optimization_suggestions,

        "execution": execution,

        "error_details": error_details,

        "ai_explanation": ai_explanation,

        "fixed_code": fixed_code,

        "fixed_execution": fixed_execution
    }