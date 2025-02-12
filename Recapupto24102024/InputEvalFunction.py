with open('input_file2.txt', 'r') as file:
    content = file.read()
    print(content)

with open('input_file2.txt', 'a') as file:
    file.write('New input entry\n')

with open('input_file2.txt', 'r') as file:
    content = file.read()
    print(content)