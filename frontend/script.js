// ==========================================
// AI CODING AGENT - FRONTEND JAVASCRIPT
// ==========================================


// ==========================================
// HELPER - ESCAPE HTML
// ==========================================

function escapeHtml(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// ==========================================
// ANALYZE CODE
// ==========================================

async function analyzeCode() {

    const codeElement =
        document.getElementById("code");

    const languageElement =
        document.getElementById("language");

    const resultElement =
        document.getElementById("result");

    const loadingElement =
        document.getElementById("loading");

    const analyzeButton =
        document.getElementById("analyzeBtn");


    const code =
        codeElement.value;

    const language =
        languageElement.value;


    // ==========================================
    // CHECK EMPTY CODE
    // ==========================================

    if (!code.trim()) {

        resultElement.innerHTML = `
            <div class="error-box">

                <h3>
                    ❌ No Code Entered
                </h3>

                <p>
                    Please enter some code before analyzing.
                </p>

            </div>
        `;

        return;
    }


    // ==========================================
    // SHOW LOADING
    // ==========================================

    loadingElement.style.display = "block";

    analyzeButton.disabled = true;

    resultElement.innerHTML = "";


    try {

        // ==========================================
        // SEND REQUEST TO BACKEND
        // ==========================================

        const response = await fetch(
            "/analyze",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    code: code,
                    language: language
                })
            }
        );


        // ==========================================
        // CHECK SERVER RESPONSE
        // ==========================================

        if (!response.ok) {

            throw new Error(
                "Server returned HTTP " +
                response.status
            );
        }


        const data =
            await response.json();


        // ==========================================
        // SAVE TO HISTORY
        // ==========================================

        if (
            data.quality &&
            data.quality.score !== undefined
        ) {

            saveToHistory(
                code,
                language,
                data.quality
            );

        }


        // ==========================================
        // BUILD RESULT
        // ==========================================

        let output = "";
        // ==========================================
// DASHBOARD SUMMARY
// ==========================================

const analysisSummary = data.analysis;
const qualitySummary = data.quality;

if (
    analysisSummary &&
    analysisSummary.success &&
    qualitySummary
) {
    const metricsSummary =
        analysisSummary.metrics || {};

    output += `
        <div class="dashboard-summary">

            <div class="summary-card">
                <div class="summary-title">
                    📊 Quality
                </div>

                <div class="summary-value">
                    ${qualitySummary.score}/100
                </div>

                <div class="summary-label">
                    ${escapeHtml(
                        qualitySummary.level
                    )}
                </div>
            </div>


            <div class="summary-card">
                <div class="summary-title">
                    🔧 Functions
                </div>

                <div class="summary-value">
                    ${metricsSummary.functions ?? 0}
                </div>

                <div class="summary-label">
                    Detected
                </div>
            </div>


            <div class="summary-card">
                <div class="summary-title">
                    🔐 Security
                </div>

                <div class="summary-value">
                    ${qualitySummary.security_issues}
                </div>

                <div class="summary-label">
                    Issues
                </div>
            </div>


            <div class="summary-card">
                <div class="summary-title">
                    🧠 Complexity
                </div>

                <div class="summary-value">
                    ${metricsSummary.cyclomatic_complexity ?? 1}
                </div>

                <div class="summary-label">
                    Cyclomatic
                </div>
            </div>

        </div>
    `;
}


        // ==========================================
        // STATIC ANALYSIS
        // ==========================================

        const analysis =
            data.analysis;


        output += `
            <div class="result-section">

                <h2>
                    🔍 Static Analysis
                </h2>
        `;


        if (
            analysis &&
            analysis.success
        ) {

            const metrics =
                analysis.metrics || {};


            output += `
                <div class="analysis-box">

                    <h3>
                        📊 Code Metrics
                    </h3>

                    <p>
                        <strong>Functions:</strong>
                        ${metrics.functions ?? 0}
                    </p>

                    <p>
                        <strong>Classes:</strong>
                        ${metrics.classes ?? 0}
                    </p>

                    <p>
                        <strong>Loops:</strong>
                        ${metrics.loops ?? 0}
                    </p>

                    <p>
                        <strong>Conditions:</strong>
                        ${metrics.conditions ?? 0}
                    </p>

                    <p>
                        <strong>Assignments:</strong>
                        ${metrics.assignments ?? 0}
                    </p>

                    <p>
                        <strong>Return Statements:</strong>
                        ${metrics.return_statements ?? 0}
                    </p>

                    <p>
                        <strong>Cyclomatic Complexity:</strong>
                        ${metrics.cyclomatic_complexity ?? 1}
                    </p>

                </div>
            `;


            // ==========================================
            // FUNCTIONS
            // ==========================================

            if (
                analysis.functions &&
                analysis.functions.length > 0
            ) {

                output += `
                    <div class="analysis-box">

                        <h3>
                            🔧 Functions
                        </h3>

                `;

                analysis.functions.forEach(
                    function(func) {

                        output += `
                            <p>
                                <strong>
                                    ${escapeHtml(func.name)}
                                </strong>

                                — Line
                                ${func.line}

                                — Parameters:
                                ${func.parameters}
                            </p>
                        `;

                    }
                );

                output += `
                    </div>
                `;
            }


            // ==========================================
            // CLASSES
            // ==========================================

            if (
                analysis.classes &&
                analysis.classes.length > 0
            ) {

                output += `
                    <div class="analysis-box">

                        <h3>
                            🏛️ Classes
                        </h3>

                `;

                analysis.classes.forEach(
                    function(cls) {

                        output += `
                            <p>
                                <strong>
                                    ${escapeHtml(cls.name)}
                                </strong>

                                — Line
                                ${cls.line}
                            </p>
                        `;

                    }
                );

                output += `
                    </div>
                `;
            }


            // ==========================================
            // IMPORTS
            // ==========================================

            if (
                analysis.imports &&
                analysis.imports.length > 0
            ) {

                output += `
                    <div class="analysis-box">

                        <h3>
                            📦 Imports
                        </h3>

                        <p>
                            ${analysis.imports
                                .map(
                                    item =>
                                        escapeHtml(item)
                                )
                                .join(", ")
                            }
                        </p>

                    </div>
                `;
            }


            // ==========================================
            // WARNINGS
            // ==========================================

            if (
                analysis.warnings &&
                analysis.warnings.length > 0
            ) {

                output += `
                    <div class="error-box">

                        <h3>
                            ⚠️ Static Analysis Warnings
                        </h3>
                `;

                analysis.warnings.forEach(
                    function(warning) {

                        output += `
                            <p>
                                ${escapeHtml(warning)}
                            </p>
                        `;

                    }
                );

                output += `
                    </div>
                `;

            } else {

                output += `
                    <div class="success-box">

                        <h3>
                            ✅ No Static Analysis Warnings
                        </h3>

                    </div>
                `;
            }

        } else {

            output += `
                <div class="error-box">

                    <h3>
                        ❌ Analysis Failed
                    </h3>

                    <p>
                        ${
                            escapeHtml(
                                analysis?.error ||
                                "Code analysis failed."
                            )
                        }
                    </p>

                </div>
            `;
        }


        output += `
            </div>
        `;


        // ==========================================
        // SECURITY ANALYSIS
        // ==========================================

        const security =
            data.security;


        output += `
            <div class="result-section">

                <h2>
                    🔐 Security Analysis
                </h2>
        `;


        if (
            security &&
            security.success
        ) {

            if (
                security.count === 0
            ) {

                output += `
                    <div class="success-box">

                        <h3>
                            ✅ No Security Vulnerabilities Found
                        </h3>

                        <p>
                            No known security issues were
                            detected by the current
                            security checks.
                        </p>

                    </div>
                `;

            } else {

                output += `
                    <div class="error-box">

                        <h3>
                            ⚠️ ${security.count}
                            Security Vulnerabilit${
                                security.count === 1
                                ? "y"
                                : "ies"
                            } Found
                        </h3>

                    </div>
                `;


                if (
                    security.vulnerabilities
                ) {

                    security.vulnerabilities.forEach(
                        function(vulnerability) {

                            output += `
                                <div class="error-box">

                                    <h3>
                                        🔴
                                        ${escapeHtml(
                                            vulnerability.severity
                                        )}
                                    </h3>

                                    <p>
                                        <strong>
                                            ${escapeHtml(
                                                vulnerability.type
                                            )}
                                        </strong>
                                    </p>

                                    <p>
                                        <strong>
                                            Line:
                                        </strong>

                                        ${vulnerability.line}
                                    </p>

                                    <p>
                                        <strong>
                                            Problem:
                                        </strong>

                                        ${escapeHtml(
                                            vulnerability.message
                                        )}
                                    </p>

                                    <p>
                                        <strong>
                                            Suggestion:
                                        </strong>

                                        ${escapeHtml(
                                            vulnerability.suggestion
                                        )}
                                    </p>

                                </div>
                            `;

                        }
                    );

                }

            }

        } else {

            output += `
                <div class="error-box">

                    <h3>
                        ❌ Security Analysis Error
                    </h3>

                    <p>
                        Security analysis could not
                        be completed.
                    </p>

                </div>
            `;
        }


        output += `
            </div>
        `;


        // ==========================================
        // CODE QUALITY SCORE
        // ==========================================

        const quality = data.quality;

output += `
    <div class="result-section">
        <h2>📊 Code Quality Score</h2>
`;

if (quality) {

    output += `
        <div class="quality-dashboard">

            <div class="quality-score-card">

                <div class="score-circle">
                    <span class="score-number">
                        ${quality.score}
                    </span>

                    <span class="score-label">
                        /100
                    </span>
                </div>

                <h3>
                    ${escapeHtml(quality.level)}
                </h3>

                <p>
                    Overall Code Quality
                </p>

            </div>


            <div class="quality-details">

                <div class="quality-stat">
                    <strong>
                        ${quality.warnings}
                    </strong>

                    <span>
                        Warnings
                    </span>
                </div>


                <div class="quality-stat">
                    <strong>
                        ${quality.complexity}
                    </strong>

                    <span>
                        Complexity
                    </span>
                </div>


                <div class="quality-stat">
                    <strong>
                        ${quality.security_issues}
                    </strong>

                    <span>
                        Security Issues
                    </span>
                </div>

            </div>

        </div>
    `;

} else {

    output += `
        <div class="error-box">

            <p>
                Code quality score could
                not be calculated.
            </p>

        </div>
    `;
}

output += `</div>`;


        // ==========================================
        // DOWNLOAD ANALYZED CODE
        // ==========================================

        const analyzedExtension =
            language.toLowerCase() === "java"
            ? "java"
            : "py";


        const analyzedFilename =
            "analyzed_code." +
            analyzedExtension;


        output += `
            <div class="download-section">

                <button
                    class="download-btn"
                    onclick="downloadCode(
                        decodeURIComponent(
                            '${encodeURIComponent(code)
                                .replace(/'/g, "%27")}'
                        ),
                        '${analyzedFilename}'
                    )"
                >
                    ⬇️ Download Analyzed Code
                </button>

            </div>
        `;


        // ==========================================
        // AI OPTIMIZATION SUGGESTIONS
        // ==========================================

        const optimization =
            data.optimization_suggestions;


        output += `
            <div class="result-section">

                <h2>
                    🤖 AI Optimization Suggestions
                </h2>

                <div class="optimization-box">
        `;


        if (optimization) {

            output += `
                <p>
                    ${escapeHtml(
                        optimization
                    ).replace(/\n/g, "<br>")}
                </p>
            `;

        } else {

            output += `
                <p>
                    No optimization suggestions
                    available.
                </p>
            `;
        }


        output += `
                </div>

            </div>
        `;


        // ==========================================
        // EXECUTION RESULT
        // ==========================================

        const execution =
            data.execution;


        output += `
            <div class="result-section">

                <h2>
                    ▶️ Execution Result
                </h2>
        `;


        if (
            execution &&
            execution.success
        ) {

            output += `
                <div class="success-box">

                    <h3>
                        ✅ Program Executed Successfully
                    </h3>

                    <pre>
${escapeHtml(
    execution.output || "No output."
)}
                    </pre>

                </div>
            `;

        } else {

            output += `
                <div class="error-box">

                    <h3>
                        ❌ Program Execution Failed
                    </h3>

                    <pre>
${escapeHtml(
    execution?.error ||
    "Unknown execution error."
)}
                    </pre>

                </div>
            `;
        }


        output += `
            </div>
        `;


        // ==========================================
        // ERROR DETAILS
        // ==========================================

        const errorDetails =
            data.error_details;


        if (errorDetails) {

            output += `
                <div class="result-section">

                    <h2>
                        ⚠️ Error Details
                    </h2>

                    <div class="error-box">

                        <h3>
                            ${escapeHtml(
                                errorDetails.title
                            )}
                        </h3>

                        <p>
                            <strong>
                                Error Type:
                            </strong>

                            ${escapeHtml(
                                errorDetails.type
                            )}
                        </p>

                        <p>
                            <strong>
                                Line:
                            </strong>

                            ${
                                errorDetails.line ??
                                "Unknown"
                            }
                        </p>

                        <p>
                            <strong>
                                Message:
                            </strong>

                            ${escapeHtml(
                                errorDetails.message
                            )}
                        </p>

                        <p>
                            <strong>
                                Explanation:
                            </strong>

                            ${escapeHtml(
                                errorDetails.explanation
                            )}
                        </p>

                        <p>
                            <strong>
                                Suggestion:
                            </strong>

                            ${escapeHtml(
                                errorDetails.suggestion
                            )}
                        </p>

                    </div>

                </div>
            `;
        }


        // ==========================================
        // AI EXPLANATION
        // ==========================================

        if (
            data.ai_explanation
        ) {

            output += `
                <div class="result-section">

                    <h2>
                        🤖 AI Explanation
                    </h2>

                    <div class="ai-box">

                        <p>
                            ${escapeHtml(
                                data.ai_explanation
                            ).replace(
                                /\n/g,
                                "<br>"
                            )}
                        </p>

                    </div>

                </div>
            `;
        }


        // ==========================================
        // FIXED CODE
        // ==========================================

        if (
            data.fixed_code
        ) {

            output += `
                <div class="result-section">

                    <h2>
                        🔧 AI Fixed Code
                    </h2>

                    <pre class="code-box">
${escapeHtml(
    data.fixed_code
)}
                    </pre>

                    <button
                        class="download-btn"
                        onclick="downloadCode(
                            decodeURIComponent(
                                '${encodeURIComponent(
                                    data.fixed_code
                                ).replace(
                                    /'/g,
                                    "%27"
                                )}'
                            ),
                            'fixed_code.py'
                        )"
                    >
                        ⬇️ Download Fixed Code
                    </button>

                </div>
            `;
        }


        // ==========================================
        // FIXED CODE EXECUTION
        // ==========================================

        if (
            data.fixed_execution
        ) {

            output += `
                <div class="result-section">

                    <h2>
                        ▶️ Fixed Code Execution
                    </h2>
            `;


            if (
                data.fixed_execution.success
            ) {

                output += `
                    <div class="success-box">

                        <h3>
                            ✅ Fixed Code Executed Successfully
                        </h3>

                        <pre>
${escapeHtml(
    data.fixed_execution.output ||
    "No output."
)}
                        </pre>

                    </div>
                `;

            } else {

                output += `
                    <div class="error-box">

                        <h3>
                            ❌ Fixed Code Execution Failed
                        </h3>

                        <pre>
${escapeHtml(
    data.fixed_execution.error ||
    "Unknown error."
)}
                        </pre>

                    </div>
                `;
            }


            output += `
                </div>
            `;
        }


        // ==========================================
        // DISPLAY FINAL RESULT
        // ==========================================

        resultElement.innerHTML =
            output;


    } catch (error) {

        // ==========================================
        // FRONTEND ERROR
        // ==========================================

        resultElement.innerHTML = `
            <div class="error-box">

                <h3>
                    ❌ Error
                </h3>

                <p>
                    ${escapeHtml(
                        error.message
                    )}
                </p>

                <p>
                    Make sure the FastAPI server
                    is running on port 8001.
                </p>

            </div>
        `;

    } finally {

        // ==========================================
        // HIDE LOADING
        // ==========================================

        loadingElement.style.display =
            "none";

        analyzeButton.disabled =
            false;
    }
}


// ==========================================
// DOWNLOAD CODE
// ==========================================

function downloadCode(
    code,
    filename
) {

    const blob =
        new Blob(
            [code],
            {
                type: "text/plain"
            }
        );


    const url =
        URL.createObjectURL(
            blob
        );


    const link =
        document.createElement(
            "a"
        );


    link.href =
        url;

    link.download =
        filename;


    document.body.appendChild(
        link
    );


    link.click();


    document.body.removeChild(
        link
    );


    URL.revokeObjectURL(
        url
    );
}


// ==========================================
// SAVE CODE HISTORY
// ==========================================

function saveToHistory(
    code,
    language,
    quality
) {

    let history =
        JSON.parse(
            localStorage.getItem(
                "codeHistory"
            ) || "[]"
        );


    const record = {

        code: code,

        language: language,

        score: quality.score,

        level: quality.level,

        warnings: quality.warnings,

        complexity: quality.complexity,

        securityIssues:
            quality.security_issues,

        date:
            new Date().toLocaleString()
    };


    history.unshift(
        record
    );


    // ==========================================
    // KEEP ONLY LAST 10
    // ==========================================

    if (
        history.length > 10
    ) {

        history =
            history.slice(
                0,
                10
            );
    }


    localStorage.setItem(
        "codeHistory",
        JSON.stringify(
            history
        )
    );
}


// ==========================================
// SHOW CODE HISTORY
// ==========================================

function showHistory() {

    const historyContainer =
        document.getElementById(
            "history"
        );


    const history =
        JSON.parse(
            localStorage.getItem(
                "codeHistory"
            ) || "[]"
        );


    if (
        history.length === 0
    ) {

        historyContainer.innerHTML = `
            <div class="history-box">

                <h2>
                    📜 Code History
                </h2>

                <p>
                    No previous analyses found.
                </p>

            </div>
        `;

        return;
    }


    let output = `
        <div class="history-box">

            <h2>
                📜 Code History
            </h2>

            <button
                class="clear-history-btn"
                onclick="clearHistory()"
            >
                🗑️ Clear History
            </button>
    `;


    history.forEach(
        function(
            item,
            index
        ) {

            output += `
                <div class="history-item">

                    <h3>
                        ${index + 1}.
                        ${escapeHtml(
                            item.language
                                .toUpperCase()
                        )}
                    </h3>

                    <p>
                        <strong>
                            Score:
                        </strong>

                        ${item.score}/100
                    </p>

                    <p>
                        <strong>
                            Level:
                        </strong>

                        ${escapeHtml(
                            item.level
                        )}
                    </p>

                    <p>
                        <strong>
                            Warnings:
                        </strong>

                        ${item.warnings}
                    </p>

                    <p>
                        <strong>
                            Complexity:
                        </strong>

                        ${item.complexity}
                    </p>

                    <p>
                        <strong>
                            Security Issues:
                        </strong>

                        ${item.securityIssues}
                    </p>

                    <p>
                        <strong>
                            Date:
                        </strong>

                        ${escapeHtml(
                            item.date
                        )}
                    </p>

                </div>
            `;
        }
    );


    output += `
        </div>
    `;


    historyContainer.innerHTML =
        output;
}


// ==========================================
// CLEAR CODE HISTORY
// ==========================================

function clearHistory() {

    localStorage.removeItem(
        "codeHistory"
    );


    showHistory();
}
// ==========================================
// UPDATE EDITOR LANGUAGE
// ==========================================

const languageSelector =
    document.getElementById("language");

const editorLanguage =
    document.getElementById("editorLanguage");

if (
    languageSelector &&
    editorLanguage
) {

    languageSelector.addEventListener(
        "change",
        function() {

            const selectedLanguage =
                languageSelector.value;

            if (
                selectedLanguage === "java"
            ) {

                editorLanguage.textContent =
                    "Java";

            } else {

                editorLanguage.textContent =
                    "Python";
            }

        }
    );
}