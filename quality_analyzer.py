def calculate_quality_score(
    analysis,
    security
):

    score = 100

    # ==========================================
    # STATIC ANALYSIS WARNINGS
    # ==========================================

    warnings = analysis.get(
        "warnings",
        []
    )

    score -= len(warnings) * 5


    # ==========================================
    # CYCLOMATIC COMPLEXITY
    # ==========================================

    metrics = analysis.get(
        "metrics",
        {}
    )

    complexity = metrics.get(
        "cyclomatic_complexity",
        1
    )


    if complexity > 10:

        score -= 20

    elif complexity > 7:

        score -= 15

    elif complexity > 5:

        score -= 10

    elif complexity > 3:

        score -= 5


    # ==========================================
    # SECURITY VULNERABILITIES
    # ==========================================

    vulnerabilities = security.get(
        "vulnerabilities",
        []
    )


    for vulnerability in vulnerabilities:

        severity = vulnerability.get(
            "severity",
            ""
        ).lower()


        if severity == "high":

            score -= 15

        elif severity == "medium":

            score -= 8

        elif severity == "low":

            score -= 3


    # ==========================================
    # KEEP SCORE BETWEEN 0 AND 100
    # ==========================================

    score = max(
        0,
        min(score, 100)
    )


    # ==========================================
    # QUALITY LEVEL
    # ==========================================

    if score >= 90:

        level = "Excellent"

    elif score >= 75:

        level = "Good"

    elif score >= 50:

        level = "Needs Improvement"

    else:

        level = "Poor"


    return {
        "score": score,
        "level": level,
        "warnings": len(warnings),
        "complexity": complexity,
        "security_issues": len(vulnerabilities)
    }