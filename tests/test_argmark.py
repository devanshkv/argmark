import filecmp
import sys
import logging  # Added import
import os  # Already present by implication of _install_dir

from argmark.argmark import *

_install_dir = os.path.abspath(os.path.dirname(__file__))


def test_inline_code():
    assert inline_code("f") == "`f`"


def test_gen_help():
    py_file = os.path.join(_install_dir, "sample_argparse.py")
    md_file = "sample_argparse.md"
    answer = os.path.join(_install_dir, "answer.md")
    with open(py_file, "r") as f:
        gen_help(f.readlines())
    assert os.path.isfile(md_file)
    assert filecmp.cmp(md_file, answer)
    os.remove(md_file)


def test_main_file_not_found_error_handling(caplog):
    """Tests that main() handles FileNotFoundError gracefully."""
    non_existent_file = "this_file_does_not_exist_ever.py"

    # Ensure the non-existent file really doesn't exist before the test
    if os.path.exists(non_existent_file):
        os.remove(non_existent_file)  # Should not happen with this name

    original_argv = sys.argv
    # Simulate command line arguments for argmark's main()
    # prog_name (sys.argv[0]) + -f + filename
    sys.argv = ["argmark", "-f", non_existent_file]

    # Set logging level to capture ERROR messages
    caplog.set_level(logging.ERROR)

    try:
        main()  # Call the main function from argmark.argmark
    except SystemExit as e:
        # argparse by default calls sys.exit() on error.
        # If main() calls parser.error() or if required args aren't met,
        # it might exit. For a FileNotFoundError, our handler shouldn't cause SystemExit.
        # However, if no files are processed successfully, main() might not produce output,
        # which could be fine. The key is it doesn't crash from an unhandled FileNotFoundError.
        # For this test, we are checking if our try/except in main() for open() works.
        pass  # Or assert e.code if a specific exit code is expected for "no files processed"

    sys.argv = original_argv  # Restore original sys.argv

    # Verify that an error message was logged
    assert len(caplog.records) >= 1, "No error message was logged."
    found_log = False
    for record in caplog.records:
        if record.levelname == "ERROR" and non_existent_file in record.message:
            # Check if the message contains 'File not found' or the specific exception text
            # Example: "Error: File not found: this_file_does_not_exist_ever.py. [Errno 2] No such file or directory: 'this_file_does_not_exist_ever.py'"
            if (
                "File not found" in record.message
                or "No such file or directory" in record.message
            ):
                found_log = True
                break
    assert (
        found_log
    ), f"Expected error message for {non_existent_file} not found in logs: {caplog.text}"

    # Clean up just in case, though it should not have been created
    if os.path.exists(non_existent_file):
        os.remove(non_existent_file)


def test_gen_help_with_subparsers():
    py_file = os.path.join(_install_dir, "sample_subparser_script.py")
    # Output prog is "app", so md_file will be "app.md"
    md_file = "app.md"
    answer_file = os.path.join(_install_dir, "answer_subparser.md")

    # Ensure old files are removed if any
    if os.path.exists(md_file):
        os.remove(md_file)

    with open(py_file, "r") as f:
        gen_help(f.readlines())

    assert os.path.isfile(md_file), f"{md_file} was not generated."
    # For debugging if filecmp fails:
    # with open(md_file, 'r') as f_actual, open(answer_file, 'r') as f_expected:
    #     print("Actual output:\n", f_actual.read())
    #     print("Expected output:\n", f_expected.read())
    assert filecmp.cmp(
        md_file, answer_file, shallow=False
    ), f"Generated {md_file} does not match {answer_file}."

    if os.path.exists(md_file):
        os.remove(md_file)


def test_main():
    py_file = os.path.join(_install_dir, "sample_argparse.py")
    sys.argv.append("-f")
    sys.argv.append(py_file)
    sys.argv.append("-v")
    main()
    md_file = "sample_argparse.md"
    answer = os.path.join(_install_dir, "answer.md")
    with open(py_file, "r") as f:
        gen_help(f.readlines())
    assert os.path.isfile(md_file)
    assert filecmp.cmp(md_file, answer)
    os.remove(md_file)
