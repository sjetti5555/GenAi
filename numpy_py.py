import numpy as np

# Define the matrix A
A = np.array([[4, 1],
              [2, 3]])

# Calculate eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)

# Output the eigenvalues and eigenvectors
print("Eigenvalues:", eigenvalues)
print("Eigenvectors:")
print(eigenvectors)
