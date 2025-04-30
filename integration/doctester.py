import doctest
import argparse
import importlib.util
import sys
import os
import re


def load_module_from_path(path):
    """Dynamically load a module from a .py file."""
    module_name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


def filter_doctests_by_keyword(finder, module, keyword):
    """Return only doctest examples where the keyword is present."""
    all_tests = finder.find(module)
    filtered_tests = []

    for test in all_tests:
        filtered_examples = [
            ex for ex in test.examples
            if keyword in ex.source or keyword in test.name
        ]
        if filtered_examples:
            new_test = doctest.DocTest(
                examples=filtered_examples,
                globs=test.globs,
                name=test.name,
                filename=test.filename,
                lineno=test.lineno,
                docstring=test.docstring
            )
            filtered_tests.append(new_test)

    return filtered_tests


def run_filtered_doctests(module_path, keyword):
    module = load_module_from_path(module_path)
    finder = doctest.DocTestFinder()
    runner = doctest.DocTestRunner()

    filtered_tests = filter_doctests_by_keyword(finder, module, keyword)

    if not filtered_tests:
        print(f"No doctests matched the keyword: '{keyword}'")
        return

    for test in filtered_tests:
        runner.run(test)

    runner.summarize()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run filtered doctests by keyword.")
    parser.add_argument(
        "module", type=str, help="Path to Python module (.py file)")
    parser.add_argument(
        "keyword", type=str, help="Keyword to filter doctests")

    args = parser.parse_args()

    run_filtered_doctests(args.module, args.keyword)
