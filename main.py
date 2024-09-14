


with open('names.txt', 'r') as file:
    names = file.readlines()  # Reads all lines into a list
    names = [name.strip() for name in names]  # Removes trailing newline characters

