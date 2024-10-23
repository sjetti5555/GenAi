# Function to calculate the probability of drawing a black king from all black cards
def calculate_probability():
    # Take user input for probabilities
    try:
        # Input for P(A): Probability of drawing a black king from the deck
        P_A = float(input("Enter the probability of drawing a black king (e.g., 2/52): "))

        # Input for P(B): Probability of drawing a black card
        P_B = float(input("Enter the probability of drawing a black card (e.g., 26/52): "))

        # P(B|A) is always 1 since if we have a black king, it is definitely a black card
        P_B_given_A = 1.0

        # Calculate P(A|B) using Bayes' theorem
        P_A_given_B = (P_B_given_A * P_A) / P_B

        # Output the result
        print(f"The probability of drawing a black king given that a black card is drawn is: {P_A_given_B:.4f}")

    except ZeroDivisionError:
        print("Error: Division by zero. Please enter a valid probability for P(B).")
    except ValueError:
        print("Error: Invalid input. Please enter probabilities as decimal numbers or fractions.")

# Call the function to perform the calculation
calculate_probability()
