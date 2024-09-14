from collections import defaultdict
def shortest_longest(names):
    shortest_name, longest_name = min(names, key=len), max(names, key=len)  # Find the shortest name by length # Find the longest name by length
    return shortest_name, longest_name # returns the names in a list

def pairs(name):
    pairs = []
    for i in range(len(name) - 1):
        pairs.append([name[i], name[i+1]])  # Create a pair and add to the list
    start_letter, end_letter = name[0], name[-1]  # First letter of the name # Last letter of the name
    return pairs, start_letter, end_letter

def count_letter_pairs_and_ends(names):
    pair_counts = defaultdict(int)  # To store pair frequencies
    start_end_counts = defaultdict(int)  # To store start and end letter counts
    for name in names:
        name = name.strip().lower()  # Clean up the name (strip spaces, convert to lowercase)
        start_end_counts[('#', name[0])] += 1 # Count start letter with '#' marker
        for i in range(len(name) - 1): # Count pairs
            pair = (name[i], name[i+1])
            pair_counts[pair] += 1
        start_end_counts[(name[-1], '$')] += 1  # Count end letter with '$' marker

    return pair_counts, start_end_counts

def write_pair_frequencies_to_file(filename, pair_counts, start_end_counts):
    with open(filename, 'w') as f:
        for pair, count in pair_counts.items(): # Write pair frequencies
            f.write(f"({pair}, {count})\n")
        for pair, count in start_end_counts.items(): # Write start and end frequencies
            f.write(f"({pair}, {count})\n")

with open('names.txt', 'r') as file:
    names = file.readlines()  # Reads all lines into a list
    names = [name.strip() for name in names]  # Removes trailing newline characters

#print(f"\nShortest name: {shortest_longest(names)[0]}\nLongest name: {shortest_longest(names)[1]}\n")

#name = input("Give a name: ")
#letter_pairs, start, end = pairs(name)
#print(f"\nLetter pairs: {letter_pairs}\nStart letter: {start}\nEnd letter: {end}\n")

pair_counts, start_end_counts = count_letter_pairs_and_ends(names) # Count letter pairs and start/end letters
write_pair_frequencies_to_file('pair_freqs_raw.txt', pair_counts, start_end_counts) # Write results to a file
