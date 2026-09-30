import re


JAVA_ERROR_EXPLANATIONS = {

    "ArithmeticException": {
        "title": "Arithmetic error",
        "explanation": (
            "The program performed an invalid arithmetic operation. "
            "A common example is dividing an integer by zero."
        ),
        "suggestion": (
            "Check the values used in the arithmetic operation "
            "and make sure you are not dividing by zero."
        )
    },

    "NullPointerException": {
        "title": "Null reference error",
        "explanation": (
            "The program tried to use an object reference "
            "whose value is null."
        ),
        "suggestion": (
            "Check whether the object is null before using "
            "its methods or properties."
        )
    },

    "ArrayIndexOutOfBoundsException": {
        "title": "Invalid array index",
        "explanation": (
            "The program tried to access an array position "
            "that does not exist."
        ),
        "suggestion": (
            "Check the array length and make sure the index "
            "is between 0 and length - 1."
        )
    },

    "StringIndexOutOfBoundsException": {
        "title": "Invalid string index",
        "explanation": (
            "The program tried to access a character position "
            "outside the valid range of the string."
        ),
        "suggestion": (
            "Check the string length before accessing a character "
            "using its index."
        )
    },

    "NumberFormatException": {
        "title": "Invalid number format",
        "explanation": (
            "The program tried to convert a string into a number, "
            "but the string was not in a valid numeric format."
        ),
        "suggestion": (
            "Check that the string contains a valid number "
            "before converting it."
        )
    },

    "ClassCastException": {
        "title": "Invalid type conversion",
        "explanation": (
            "The program tried to convert an object into an "
            "incompatible type."
        ),
        "suggestion": (
            "Check the actual object type before performing "
            "the type conversion."
        )
    },

    "IllegalArgumentException": {
        "title": "Invalid argument",
        "explanation": (
            "A method received an argument that was not valid "
            "for the operation."
        ),
        "suggestion": (
            "Check the values being passed to the method."
        )
    },

    "FileNotFoundException": {
        "title": "File not found",
        "explanation": (
            "The program tried to access a file that could "
            "not be found at the specified location."
        ),
        "suggestion": (
            "Check the file path and make sure the file exists."
        )
    },

    "IOException": {
        "title": "Input/output error",
        "explanation": (
            "An input or output operation failed while "
            "the program was running."
        ),
        "suggestion": (
            "Check the file, stream, or input/output operation "
            "that caused the error."
        )
    },

    "Exception": {
        "title": "Java runtime exception",
        "explanation": (
            "The program encountered an exception while "
            "executing."
        ),
        "suggestion": (
            "Check the exception message and the line where "
            "the exception occurred."
        )
    }
}


def parse_java_error(error_text):

    if not error_text:

        return {
            "type": "UnknownJavaError",
            "line": None,
            "message": "Unknown Java error.",
            "title": "Unknown Java error",
            "explanation": (
                "The Java program stopped unexpectedly."
            ),
            "suggestion": (
                "Check the compiler or runtime output."
            )
        }


    # ==========================================
    # FIND JAVA ERROR TYPE
    # ==========================================

    error_type = "UnknownJavaError"

    for error_name in JAVA_ERROR_EXPLANATIONS:

        if error_name in error_text:

            error_type = error_name

            break


    # ==========================================
    # FIND LINE NUMBER
    # ==========================================

    line_number = None

    # Runtime error example:
    #
    # at Test.main(Test.java:8)
    #
    runtime_match = re.search(
        r'\.java:(\d+)',
        error_text
    )

    if runtime_match:

        line_number = int(
            runtime_match.group(1)
        )

    else:

        # Compilation error example:
        #
        # Test.java:8: error:
        #
        compile_match = re.search(
            r'\.java:(\d+):',
            error_text
        )

        if compile_match:

            line_number = int(
                compile_match.group(1)
            )


    # ==========================================
    # FIND ERROR MESSAGE
    # ==========================================

    lines = error_text.strip().splitlines()

    message = (
        lines[-1].strip()
        if lines
        else error_text.strip()
    )


    # ==========================================
    # ERROR DETAILS
    # ==========================================

    details = JAVA_ERROR_EXPLANATIONS.get(

        error_type,

        {
            "title": "Java error",

            "explanation": (
                "The Java program encountered "
                "an error during compilation "
                "or execution."
            ),

            "suggestion": (
                "Review the Java error message "
                "and the reported line."
            )
        }
    )


    # ==========================================
    # RETURN RESULT
    # ==========================================

    return {

        "type": error_type,

        "line": line_number,

        "message": message,

        "title": details["title"],

        "explanation": details["explanation"],

        "suggestion": details["suggestion"]
    }