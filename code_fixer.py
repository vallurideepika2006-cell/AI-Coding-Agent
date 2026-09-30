import os
import json
import urllib.request
import urllib.error


def generate_fixed_code(original_code, error_details):

    prompt = f"""
You are an AI coding assistant.

Fix the following Python program.

ORIGINAL CODE:
{original_code}

ERROR DETAILS:
{error_details}

Rules:
1. Fix the actual error.
2. Keep the original purpose of the program.
3. Return ONLY the corrected Python code.
4. Do not include explanations.
5. Do not use markdown code fences.
"""

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("GEMINI_API_KEY is not set.")
        return None

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-3.8-flash:generateContent"
    )

    data = {
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
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

            fixed_code = result["candidates"][0]["content"]["parts"][0]["text"]

            fixed_code = fixed_code.strip()

            # Remove markdown code fences if Gemini adds them
            if fixed_code.startswith("```python"):
                fixed_code = fixed_code[9:]

            elif fixed_code.startswith("```"):
                fixed_code = fixed_code[3:]

            if fixed_code.endswith("```"):
                fixed_code = fixed_code[:-3]

            return fixed_code.strip()

    except urllib.error.HTTPError as error:

        error_body = error.read().decode("utf-8")

        print("Code fixer error:", error_body)

        return None

    except Exception as error:

        print("Code fixer error:", error)

        return None


# Test the code fixer
if __name__ == "__main__":

    original_code = """a = 10
b = 0
print(a / b)
"""

    error_details = {
        "type": "ZeroDivisionError",
        "line": 3,
        "message": "division by zero"
    }

    fixed_code = generate_fixed_code(
        original_code,
        error_details
    )

    print("\nFIXED CODE:\n")

    if fixed_code:
        print(fixed_code)
    else:
        print("Could not generate fixed code.")