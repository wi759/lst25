import re

# Import the test results
from test_results import test_results

# Read the test file
test_file_path = "test_main.py"
with open(test_file_path, "r") as f:
    content = f.read()

# Process each test case
for test_name, expected_values in test_results.items():
    # Find the test function in the content
    test_pattern = f"def {test_name}\(\):[\s\S]+?(?=\ndef |$)"
    test_match = re.search(test_pattern, content)

    if test_match:
        test_code = test_match.group(0)
        updated_test_code = test_code

        # Find all assertions in the test code
        assertion_matches = re.finditer(
            r'\s+assert result\["([^"]+)"\] == Decimal\([^)]+\)', test_code
        )

        for match in assertion_matches:
            full_match = match.group(0)
            key = match.group(1)

            if key in expected_values:
                # Create the updated assertion
                updated_assertion = (
                    f'    assert result["{key}"] == Decimal({expected_values[key]})\n'
                )

                # Replace the assertion
                updated_test_code = updated_test_code.replace(
                    full_match, updated_assertion
                )

        # Replace the test code in the content
        content = content.replace(test_code, updated_test_code)

# Write the updated content back to the file
with open(test_file_path, "w") as f:
    f.write(content)

print(f"Updated assertions in {test_file_path}")
