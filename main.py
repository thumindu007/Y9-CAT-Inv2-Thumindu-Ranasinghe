from collections import defaultdict as df
import ast
import plotly.express as px
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

with open('names.txt', 'r') as f:
    names = f.readlines()
    names = [name.strip() for name in names] # cleans it up

#print(f"\nShortest name: {long_short(names)[0]}\nLongest name: {long_short(names)[1]}\n")

#name = input("Give a name: ")
#letter_pairs, start, end = detect_pairs(name)
#print(f"\nLetter pairs: {letter_pairs}\nStart letter: {start}\nEnd letter: {end}\n")

pair_counts, start_end_counts = count_letter_pairs(names) # Count letter pairs
big_letter_pairs = writing('pair_freqs_raw.txt', pair_counts, start_end_counts) # writes

#piechat(big_letter_pairs)

wanted_letter = input("What letter do you watn to search: ")
result = pairs_with_spesific_letter(wanted_letter, big_letter_pairs)
for pair in result:
    print(pair)