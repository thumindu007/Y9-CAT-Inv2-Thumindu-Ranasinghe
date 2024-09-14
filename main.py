def shortest_longest(names):
    shortest_name, longest_name = min(names, key=len), max(names, key=len)  # Find the shortest name by length # Find the longest name by length
    return shortest_name, longest_name # returns the names in a list

def letter_pairs(name):
    pairs = []
    for i in range(len(name) - 1):
        pairs.append([name[i], name[i+1]])  # Create a pair and add to the list
    return pairs

with open('names.txt', 'r') as file:
    names = file.readlines()  # Reads all lines into a list
    names = [name.strip() for name in names]  # Removes trailing newline characters

#print(f"\nShortest name: {shortest_longest(names)[0]}\nLongest name: {shortest_longest(names)[1]}\n")

#name = input("Give a name: ")
#print(letter_pairs(name))