#def greet(name):
 #   print(f"Hello, {name}!")
#greet("Alice")  # Outputs: Hello, Alice!

def calculate_area(shape, length, width=0):
    if shape == 'rectangle':
        return length * width
    elif shape == 'circle':
        return 3.14 * length * length
    else:
        return None

area = calculate_area('rectangle', length=10, width=5)
print(f"Area of the rectangle: {area} sq. meters")
