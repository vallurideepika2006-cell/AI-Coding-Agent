import subprocess
import sys
import tempfile
import os


def execute_python_code(code):

    if not code.strip():
        return {
            "success": False,
            "error": "No code was entered."
        }

    file_path = None

    try:

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as file:

            file.write(code)
            file_path = file.name


        process = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=5
        )


        if process.returncode == 0:

            return {
                "success": True,
                "output": process.stdout,
                "error": None
            }

        else:

            return {
                "success": False,
                "output": process.stdout,
                "error": process.stderr
            }


    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "output": "",
            "error": "Program execution timed out."
        }


    except Exception as error:

        return {
            "success": False,
            "output": "",
            "error": str(error)
        }


    finally:

        if file_path and os.path.exists(file_path):

            os.remove(file_path)
def execute_java_code(code):
    if not code.strip():
        return {
            "success": False,
            "output": "",
            "error": "No code was entered."
        }

    import os
    import re
    import subprocess
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()

    try:
        # Find public class name
        public_class_match = re.search(
            r'\bpublic\s+class\s+([A-Za-z_][A-Za-z0-9_]*)',
            code
        )

        # If no public class, find normal class
        if public_class_match:
            class_name = public_class_match.group(1)
        else:
            class_match = re.search(
                r'\bclass\s+([A-Za-z_][A-Za-z0-9_]*)',
                code
            )

            if not class_match:
                return {
                    "success": False,
                    "output": "",
                    "error": "No Java class found."
                }

            class_name = class_match.group(1)

        java_file = os.path.join(
            temp_dir,
            class_name + ".java"
        )

        # Write Java source file
        with open(
            java_file,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(code)

        # Compile Java code
        compile_process = subprocess.run(
            [
                "javac",
                java_file
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Compilation failed
        if compile_process.returncode != 0:
            return {
                "success": False,
                "output": "",
                "error": compile_process.stderr
            }

        # Run compiled Java program
        run_process = subprocess.run(
            [
                "java",
                "-cp",
                temp_dir,
                class_name
            ],
            capture_output=True,
            text=True,
            timeout=5
        )

        # Runtime successful
        if run_process.returncode == 0:
            return {
                "success": True,
                "output": run_process.stdout,
                "error": None
            }

        # Runtime error
        return {
            "success": False,
            "output": run_process.stdout,
            "error": run_process.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Java program execution timed out."
        }

    except FileNotFoundError:
        return {
            "success": False,
            "output": "",
            "error": "Java/Javac was not found. Make sure JDK is installed and added to PATH."
        }

    except Exception as error:
        return {
            "success": False,
            "output": "",
            "error": str(error)
        }

    finally:
        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )
def execute_java_code(code):
    if not code.strip():
        return {
            "success": False,
            "output": "",
            "error": "No code was entered."
        }

    import os
    import re
    import subprocess
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()

    try:
        public_class_match = re.search(
            r'\bpublic\s+class\s+([A-Za-z_][A-Za-z0-9_]*)',
            code
        )

        if public_class_match:
            class_name = public_class_match.group(1)
        else:
            class_match = re.search(
                r'\bclass\s+([A-Za-z_][A-Za-z0-9_]*)',
                code
            )

            if not class_match:
                return {
                    "success": False,
                    "output": "",
                    "error": "No Java class found."
                }

            class_name = class_match.group(1)

        java_file = os.path.join(
            temp_dir,
            class_name + ".java"
        )

        with open(java_file, "w", encoding="utf-8") as file:
            file.write(code)

        compile_process = subprocess.run(
            ["javac", java_file],
            capture_output=True,
            text=True,
            timeout=10
        )

        if compile_process.returncode != 0:
            return {
                "success": False,
                "output": "",
                "error": compile_process.stderr
            }

        run_process = subprocess.run(
            ["java", "-cp", temp_dir, class_name],
            capture_output=True,
            text=True,
            timeout=5
        )

        if run_process.returncode == 0:
            return {
                "success": True,
                "output": run_process.stdout,
                "error": None
            }

        return {
            "success": False,
            "output": run_process.stdout,
            "error": run_process.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Java program execution timed out."
        }

    except FileNotFoundError:
        return {
            "success": False,
            "output": "",
            "error": "Java/Javac was not found. Make sure JDK is installed and added to PATH."
        }

    except Exception as error:
        return {
            "success": False,
            "output": "",
            "error": str(error)
        }

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
