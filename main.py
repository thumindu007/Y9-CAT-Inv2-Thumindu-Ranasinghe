from collections import defaultdict as df
import ast
import plotly.express as px
import random
import string
#https://pythongeeks.org/defaultdict-in-python/
def long_short(names):
    shortest_name, longest_name = min(names, key=len), max(names, key=len)
    return shortest_name, longest_name

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

def get_next_letter_based_on_frequency(current_letter):
    possible_next_letters = [pair[1] for pair in result_dict if pair[0] == current_letter]
    if not possible_next_letters:
        return None  # No possible next letters
    weights = [result_dict[(current_letter, next_letter)] for next_letter in possible_next_letters]
    return random.choices(possible_next_letters, weights=weights)[0]

def generate_frequency_based_name(start_letter):
    name = start_letter
    current_letter = start_letter
    while True:
        next_letter = get_next_letter_based_on_frequency(current_letter)
        if not next_letter:  # No more possible letters
            break
        name += next_letter
        current_letter = next_letter
    return name

def generate_random_name(start_letter=None):
    if start_letter is None:
        start_letter = random.choice(string.ascii_lowercase)
    name = start_letter
    while True:
        next_letter = random.choice(string.ascii_lowercase)
        # Terminate randomly based on a probability
        if random.random() < 0.1:  # 10% chance to stop
            break
        name += next_letter
    return name

def generate_names(mode, num_names, start_letter=None):
    names = []
    for _ in range(num_names):
        if mode == "frequency_based" and start_letter:
            names.append(generate_frequency_based_name(start_letter))
        elif mode == "random" and start_letter:
            names.append(generate_random_name(start_letter))
        elif mode == "random_no_limit":
            names.append(generate_random_name())
    return names

def get_pair_probability(pair):
    total_frequency = sum(result_dict.values())
    pair_freq = result_dict.get(pair, 0)
    # Calculate probability by normalizing with total frequency
    probability = pair_freq / total_frequency if total_frequency > 0 else 0
    return probability

# Function to evaluate a name and print its pair probabilities
def evaluate_name(name):
    print(f"Evaluating the name: {name}")
    total_probability = 1.0
    
    for i in range(len(name) - 1):
        pair = (name[i], name[i + 1])
        pair_prob = get_pair_probability(pair)
        total_probability *= pair_prob
        print(f"Pair {pair}: Probability = {pair_prob:.6f}")

with open('names.txt', 'r') as f:
    names = f.readlines()
    names = [name.strip() for name in names] # cleans it up

pair_counts, start_end_counts = count_letter_pairs(names) # Count letter pairs
big_letter_pairs = writing('pair_freqs_raw.txt', pair_counts, start_end_counts) # writes
global result_dict
result_dict = {key: value for (key, value) in big_letter_pairs}
print()
part = int(input("Use the menu below to explore the features of Tiny Language Model\n(1) Basic statistics (number of names, shortest, longest, e.t.c.)\n(2) Display the first _ lines of the sorted pairs frequency table\n(3) Display pairs starting with a particular character\n(4) Flip the coin and demonstrate correctness\n(5) Spin the numbered wheel and demonstrate correctness\n(6) Generate _ new names starting with letter _\n(7) Generate _ random names\n(8) Demonstrate the result of an untrained character-pair freq. table\n(9) Evaluate a name against the model by printing its pair probabilities\nEnter 1 to 9, or 0 to quit:"))
if part == 1:
    print(f"\nShortest name: {long_short(names)[0]}\nLongest name: {long_short(names)[1]}\n")
elif part == 2:
    display_top_pairs('pair_freqs_raw.txt', 20)
elif part == 3:
    wanted_letter = input("What letter do you watn to search: ")
    print(pairs_with_spesific_letter(wanted_letter, big_letter_pairs))
elif part == 4:
    print(f"probablitiy output: {randomness('coin')}")
elif part == 5:
    print(f"probablitiy output: {randomness('wheel')}")
elif part == 6:
    num_names = int(input("How many names do you want to generate? "))
    start_letter = input("Enter the letter to start the name with: ").lower()
    frequency_based_names = generate_names("frequency_based", num_names, start_letter)
    frequency_based_names = [sub[: -1] for sub in frequency_based_names]
    for i in frequency_based_names:
        print(i)
elif part == 7:
    num_names = int(input("How many names do you want to generate? "))
    ligma = generate_names("random_no_limit", num_names)
    ligma = [sub[: -1] for sub in ligma]
    for i in ligma:
        print(i)
elif part == 8:
    num_names = int(input("How many names do you want to generate? "))
    start_letter = input("Enter the letter to start the name with: ").lower()
    sugma = generate_names("random", num_names, start_letter)
    sugma = [sub[: -1] for sub in sugma]
    for i in sugma:
        print(i)
elif part == 9:
    name_to_evaluate = input("Enter a name to evaluate: ").lower()
    evaluate_name(name_to_evaluate)
else:
    piechat(big_letter_pairs)