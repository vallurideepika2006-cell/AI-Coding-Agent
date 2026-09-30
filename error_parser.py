import re


ERROR_EXPLANATIONS = {

    "ZeroDivisionError": {
        "title": "Division by zero",
        "explanation": (
            "The program attempted to divide a number by zero."
        ),
        "suggestion": (
            "Check that the denominator is not zero "
            "before performing the division."
        )
    },

    "IndexError": {
        "title": "Invalid list index",
        "explanation": (
            "The program tried to access a list position "
            "that does not exist."
        ),
        "suggestion": (
            "Check the list length and make sure the index "
            "is within the valid range."
        )
    },

    "KeyError": {
        "title": "Missing dictionary key",
        "explanation": (
            "The program tried to access a dictionary "
            "key that does not exist."
        ),
        "suggestion": (
            "Check whether the key exists before accessing it."
        )
    },

    "NameError": {
        "title": "Undefined variable or name",
        "explanation": (
            "The program tried to use a variable or name "
            "that has not been defined."
        ),
        "suggestion": (
            "Check the spelling and make sure the variable "
            "is defined before it is used."
        )
    },

    "TypeError": {
        "title": "Invalid operation between data types",
        "explanation": (
            "The program attempted an operation using "
            "incompatible data types."
        ),
        "suggestion": (
            "Check the types of the values involved in the operation."
        )
    },

    "ValueError": {
        "title": "Invalid value",
        "explanation": (
            "A function received a value of an inappropriate type "
            "or format."
        ),
        "suggestion": (
            "Check the value being passed to the function."
        )
    },

    "AttributeError": {
        "title": "Attribute does not exist",
        "explanation": (
            "The program tried to access an attribute or method "
            "that the object does not have."
        ),
        "suggestion": (
            "Check the object's type and the name of the attribute."
        )
    },

    "FileNotFoundError": {
        "title": "File not found",
        "explanation": (
            "The program attempted to open a file that "
            "could not be found."
        ),
        "suggestion": (
            "Check the file path and make sure the file exists."
        )
    }
}


def parse_runtime_error(error_text):

    if not error_text:
        return {
            "type": "UnknownError",
            "line": None,
            "message": "Unknown runtime error.",
            "title": "Unknown error",
            "explanation": "The program stopped unexpectedly.",
            "suggestion": "Check the program output and traceback."
        }


    error_type = "UnknownError"

    for error_name in ERROR_EXPLANATIONS:

        if error_name in error_text:
            error_type = error_name
            break


    line_number = None

    matches = re.findall(
        r'line (\d+)',
        error_text
    )

    if matches:
        line_number = int(matches[-1])


    lines = error_text.strip().splitlines()

    message = lines[-1] if lines else error_text


    details = ERROR_EXPLANATIONS.get(
        error_type,
        {
            "title": "Runtime error",
            "explanation": (
                "The program stopped because of a runtime error."
            ),
            "suggestion": (
                "Review the traceback and the line where "
                "the error occurred."
            )
        }
    )


    return {

        "type": error_type,

        "line": line_number,

        "message": message,

        "title": details["title"],

        "explanation": details["explanation"],

        "suggestion": details["suggestion"]
    }