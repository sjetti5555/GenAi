# Types of arguments in Python

# 1. Positional arguments
def positional_args(arg1, arg2, arg3):
    print(f"Positional arguments: {arg1}, {arg2}, {arg3}")

# 2. Keyword arguments
def keyword_args(name, age, city):
    print(f"Keyword arguments: Name: {name}, Age: {age}, City: {city}")

# 3. Default arguments
def default_args(name, age=30, city="Unknown"):
    print(f"Default arguments: Name: {name}, Age: {age}, City: {city}")

# 4. Variable-length arguments (*args)
def var_args(*args):
    print("Variable-length arguments:")
    for arg in args:
        print(arg)

# 5. Variable-length keyword arguments (**kwargs)
def var_kwargs(**kwargs):
    print("Variable-length keyword arguments:")
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# 6. Positional-only arguments (Python 3.8+)
def pos_only_args(arg1, arg2, /, arg3):
    print(f"Positional-only arguments: {arg1}, {arg2}, {arg3}")

# 7. Keyword-only arguments
def kw_only_args(*, arg1, arg2):
    print(f"Keyword-only arguments: {arg1}, {arg2}")

# 8. Combined usage of different argument types
def combined_args(pos1, pos2, /, standard, *, kw1, kw2, **kwargs):
    print(f"Positional-only: {pos1}, {pos2}")
    print(f"Standard: {standard}")
    print(f"Keyword-only: {kw1}, {kw2}")
    print("Additional keyword arguments:")
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# Example usage of the functions
if __name__ == "__main__":
    positional_args(1, 2, 3)
    keyword_args(name="Alice", age=25, city="New York")
    default_args("Bob")
    var_args(1, 2, 3, 4, 5)
    var_kwargs(name="Charlie", age=35, city="London", job="Developer")
    pos_only_args(1, 2, 3)
    kw_only_args(arg1="Hello", arg2="World")
    combined_args(1, 2, "Standard", kw1="Key1", kw2="Key2", extra1="Extra1", extra2="Extra2")
