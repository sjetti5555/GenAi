import sys

def get_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")

# Check if command-line arguments are provided
if len(sys.argv) == 3:
    a = int(sys.argv[1])
    b = int(sys.argv[2])
else:
    # If not, ask for input
    a = get_number("Enter the first number: ")
    b = get_number("Enter the second number: ")

print(f"The sum of {a} and {b} is: {a + b}")
