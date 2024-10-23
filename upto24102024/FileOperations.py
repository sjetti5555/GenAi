import os
import tkinter as tk
from tkinter import filedialog
import math

# Function to select file
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select text file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    return file_path

# Function to read data from text file
def read_txt(filename):
    if not os.path.isfile(filename):
        print(f"File '{filename}' not found. Creating a new file...")
        create_txt(filename)
    
    with open(filename, mode='r') as file:
        data = file.readlines()
        
        # Check if there's data in the file
        if not data:
            print("No data found in the file.")
        else:
            print("Data found in the file:")
            for line in data:
                print(line.strip())
    
    return data

# Function to create a new text file
def create_txt(filename):
    with open(filename, mode='w') as file:
        file.write("This is a new text file.\n")

# Function to add data from terminal
def add_data(filename):
    data = []
    print("Enter data (press Enter twice to finish):")
    while True:
        line = input()
        if line == "":
            break
        data.append(line + "\n")
    
    with open(filename, mode='a') as file:
        file.writelines(data)
    
    print(f"{len(data)} line(s) added to the file.")

# Function to chunk data and create new files
def chunk_data(filename, num_chunks):
    with open(filename, 'r') as file:
        data = file.readlines()
    
    if len(data) == 0:
        print("Not enough data to chunk.")
        return

    chunk_size = math.ceil(len(data) / num_chunks)
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    base_name = os.path.splitext(filename)[0]
    for i, chunk in enumerate(chunked_data, 1):
        chunk_filename = f"{base_name}_chunk_{i}.txt"
        with open(chunk_filename, mode='w') as file:
            file.writelines(chunk)
        print(f"Created {chunk_filename}")

# Main execution
if __name__ == "__main__":
    filename = select_file()
    if not filename:
        print("No file selected. Exiting.")
        exit()

    print(f"Selected file: {filename}")

    while True:
        print("\n1. Read data")
        print("2. Add data")
        print("3. Chunk data")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")
        
        if choice == '1':
            read_txt(filename)
        elif choice == '2':
            add_data(filename)
        elif choice == '3':
            num_chunks = int(input("Enter the number of chunks to create: "))
            chunk_data(filename, num_chunks)
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
