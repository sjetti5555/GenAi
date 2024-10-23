import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def calculate_probability():
    # Set B: First 1000 odd numbers
    B = set(range(1, 2000, 2))
    
    # Upper bound of B
    upper_bound = max(B)
    
    # Set A: All prime numbers up to the upper bound of B
    A = set(num for num in range(2, upper_bound + 1) if is_prime(num))
    
    # Intersection of A and B
    A_intersect_B = A.intersection(B)
    
    # Calculate probability P(A|B) = P(A ∩ B) / P(B)
    probability = len(A_intersect_B) / len(B)
    
    return probability

# Calculate and print the probability
prob = calculate_probability()
print(f"The probability of A given B is: {prob:.4f}")

# Optional: Print additional information
print(f"Number of elements in B: {1000}")
print(f"Number of elements in A ∩ B: {len(set(num for num in range(1, 2000, 2) if is_prime(num)))}")
