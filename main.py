from collections import defaultdict as df
import ast
import plotly.express as px
import random
#https://pythongeeks.org/defaultdict-in-python/
def long_short(names):
    shortest_name, longest_name = min(names, key=len), max(names, key=len)
    return shortest_name, longest_name

def detect_pairs(name):
    pairs = []
    for i in range(len(name) - 1):
        pairs.append([name[i], name[i+1]])  # create a pair and add to the list
    start_letter, end_letter = name[0], name[-1]  # gets first and last letter
    return pairs, start_letter, end_letter

def count_letter_pairs(names):
    pair_counts, start_end_counts = [df(int), df(int)]
    for name in names:
        start_end_counts[('#', name[0])] += 1 # gets first pair
        for i in range(len(name) - 1):
            pair = (name[i], name[i+1])
            pair_counts[pair] += 1
        start_end_counts[(name[-1], '$')] += 1  #gets last pair

    return pair_counts, start_end_counts

def writing(file, pair_counts, start_end_counts):
    with open(file, 'w') as f:
        for pair, count in pair_counts.items(): # write pairs frequencies
            f.write(f"({pair}, {count})\n")
        for pair, count in start_end_counts.items(): # writes start and end 
            f.write(f"({pair}, {count})\n")
    with open(file, 'r') as file:
        biglist = [ast.literal_eval(line.strip()) for line in file.readlines()]
    return biglist

def piechat(l_pairs):
    pairs = [f"({pair[0]},{pair[1]})" for pair, freq in l_pairs]
    frequencies = [freq for pairs, freq in l_pairs]
    fig = px.pie(
     names=pairs, 
     values=frequencies,
     title="Frequency of Letter Pairs",
     labels={'pairs': 'Letter Pairs'}
    )
    fig.update_traces(textinfo='label+percent', hoverinfo='label+value')
    fig.show()

def pairs_with_spesific_letter(letter, pairs):
    filtered_pairs = [pair for pair in pairs if pair[0][0] == letter]
    return filtered_pairs

def randomness(whichone):
    coin, wheel = ['0', '0', '0', '0', '0', '0', '0', '0', '1', '1'], ['0', '0', '1', '2', '3', '3', '3', '3', '3', '3']
    if whichone == 'coin': return random.choice(coin)
    elif whichone == 'wheel': return random.choice(wheel)

def weighted_random_choice(pairs):
    frequencies = [freq for pair, freq in pairs]
    chosen_pair = random.choices(pairs, weights=frequencies, k=1)[0]
    return chosen_pair

def display_top_pairs(file_path, n):
    # Read the file content
    with open(file_path, 'r') as f:
        pair_freqs = []
        for line in f:
            # Convert the line string into a tuple (pair, frequency)
            pair, freq = eval(line.strip())
            pair_freqs.append((pair, freq))
    
    # Sort the pairs by frequency in descending order
    sorted_pairs = sorted(pair_freqs, key=lambda x: x[1], reverse=True)
    
    # Display the top 'n' pairs
    for i in range(min(n, len(sorted_pairs))):
        print(sorted_pairs[i])

def get_next_letter(last_letter):
    # Filter the pair frequency dictionary for pairs that start with the last letter
    candidates = [(pair[1], freq) for pair, freq in result_dict.items() if pair[0] == last_letter]
    if not candidates:
        return None
    letters, frequencies = zip(*candidates)
    # Normalize frequencies for a random weighted choice
    total = sum(frequencies)
    probabilities = [f / total for f in frequencies]
    next_letter = random.choices(letters, probabilities)[0]
    return next_letter

def generate_name(start_letter, length=6):
    name = [start_letter]  # Start with the user-inputted letter
    # Generate the next characters based on pair frequencies
    while len(name) < length:
        last_letter = name[-1]
        next_letter = get_next_letter(last_letter)
        if next_letter is None:
            break  # If no valid next letter, stop the generation
        name.append(next_letter)
    # Ensure the generated name doesn't end with '$'
    if name[-1] == '$':
        name.pop()  # Remove the last character if it's '$'

    return ''.join(name)

def generate_random_name(length=6):
    letters = set(pair[0] for pair in result_dict.keys()).union(set(pair[1] for pair in result_dict.keys()))
    
    # Randomly choose letters for the name
    name = [random.choice(list(letters)) for _ in range(length)]
    
    # Ensure the generated name doesn't end with '$'
    if name[-1] == '$':
        name.pop()  # Remove the last character if it's '$'
    
    return ''.join(name)

with open('names.txt', 'r') as f:
    names = f.readlines()
    names = [name.strip() for name in names] # cleans it up

#print(f"\nShortest name: {long_short(names)[0]}\nLongest name: {long_short(names)[1]}\n")
#MAKE ALPHABETICALLY SORTED PAIRFREQUANCEY
#MAKE FREQUCNY SORTED PAIRFREQUANCEY list
#name = input("Give a name: ")
#letter_pairs, start, end = detect_pairs(name)
#print(f"\nLetter pairs: {letter_pairs}\nStart letter: {start}\nEnd letter: {end}\n")

#display_top_pairs('pair_freqs_raw.txt', 20) #PART 2


pair_counts, start_end_counts = count_letter_pairs(names) # Count letter pairs
big_letter_pairs = writing('pair_freqs_raw.txt', pair_counts, start_end_counts) # writes
global result_dict
result_dict = {key: value for (key, value) in big_letter_pairs}

#piechat(big_letter_pairs)

#wanted_letter = input("What letter do you watn to search: ")
#result = pairs_with_spesific_letter(wanted_letter, big_letter_pairs)
#for pair in result:
#    print(pair)

#print(f"probablitiy output: {randomness('coin')}")

#print(f"probablitiy output: {randomness('wheel')}")

num_names = int(input("How many names do you want to generate? "))

# Ask if the user wants to specify a starting letter
generate_with_start_letter = input("Do you want to start with a specific letter? (yes/no): ").lower()

if generate_with_start_letter == 'yes':
    start_letter = input("Enter the letter to start the name with: ").lower()
    # Generate and print the specified number of names based on the starting letter
    for _ in range(num_names):
        generated_name = generate_name(start_letter, length=6)
        print("Generated name:", generated_name)
else:
    # Generate and print the specified number of completely random names
    for _ in range(num_names):
        generated_name = generate_random_name(length=6)
        print("Generated name:", generated_name)

#wanted_letter = input("What letter do you watn to search: ")
#result = pairs_with_spesific_letter(wanted_letter, big_letter_pairs)
#chosen_pair = weighted_random_choice(result)
#print(f"Randomly selected pair: {chosen_pair}")