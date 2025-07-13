import re

# Read the test file
test_file_path = 'test_main.py'
with open(test_file_path, 'r') as f:
    content = f.read()

# Fix the pattern 'result = calculator.calculate()    assert'
pattern = r'result = calculator\.calculate\(\)\s+assert'
replacement = 'result = calculator.calculate()\n    assert'

# Apply the fix
fixed_content = re.sub(pattern, replacement, content)

# Write the fixed content back to the file
with open(test_file_path, 'w') as f:
    f.write(fixed_content)

print(f"Fixed syntax errors in {test_file_path}")