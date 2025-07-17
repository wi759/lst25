import ast
from pathlib import Path
from test_results import TEST_RESULTS


def update_test_assertions():
    """
    Parses test_main.py and updates the assert statements
    with the correct values from the TEST_RESULTS dictionary.
    """
    base_path = Path(__file__).parent
    test_file_path = base_path / "test_main.py"

    with open(test_file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    for func_def in ast.walk(tree):
        if not isinstance(func_def, ast.FunctionDef) or not func_def.name.startswith(
            "test_"
        ):
            continue

        if func_def.name not in TEST_RESULTS:
            continue

        expected_results = TEST_RESULTS[func_def.name]
        new_body = []

        # Flag to track if we are replacing asserts
        is_after_result_calculation = False

        for node in func_def.body:
            # Keep nodes until the result calculation
            if not is_after_result_calculation:
                new_body.append(node)
                if (
                    isinstance(node, ast.Assign)
                    and len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name)
                    and node.targets[0].id == "result"
                ):
                    is_after_result_calculation = True

            # After the result calculation, we discard old asserts
            if is_after_result_calculation and isinstance(node, ast.Assert):
                continue  # Discard existing assert statements

        # Add new assert statements based on the results
        if is_after_result_calculation:
            for key, value in expected_results.items():
                new_assert = ast.Assert(
                    test=ast.Compare(
                        left=ast.Subscript(
                            value=ast.Name(id="result", ctx=ast.Load()),
                            slice=ast.Index(value=ast.Constant(value=key)),
                            ctx=ast.Load(),
                        ),
                        ops=[ast.Eq()],
                        comparators=[ast.Constant(value=value)],
                    ),
                    msg=None,
                )
                # To make it pretty, convert Decimal to Decimal('...')
                if isinstance(value, str):
                    new_assert.test.comparators[0] = ast.Call(
                        func=ast.Name(id="Decimal", ctx=ast.Load()),
                        args=[ast.Constant(value=str(value))],
                        keywords=[],
                    )

                new_body.append(new_assert)

        func_def.body = new_body

    # Use ast.unparse if available (Python 3.9+)
    try:
        updated_code = ast.unparse(tree)
    except AttributeError:
        # Fallback for older Python versions, might need an external library like 'astor'
        import astor

        updated_code = astor.to_source(tree)

    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(updated_code)

    print(f"Test assertions in {test_file_path} updated successfully.")


if __name__ == "__main__":
    update_test_assertions()
