import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> DN VP | DN VP Conj S | DN VP Conj VP
DN -> NP | Det NP
NP -> N | Adj NP | N PP | NP Adv
VP -> V | V DN | V PP | Adv VP | VP Adv
PP -> P | P DN
"""

# safe
"""
S -> NP VP | NP VP Conj S | NP VP Conj VP
NP -> N | Det NP | Det AP | N PP | NP Adv
VP -> V | V NP | V PP | Adv VP | VP Adv
PP -> P | P NP
AP -> Adj NP | Adj AP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main(s, show=True):
    if show:
        print(s)
    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
        # print(trees)
    except ValueError as e:
        print(e)
        return False
    if not trees:
        # print("Could not parse sentence.")
        return False
    if not show:
        return True
    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = sentence.lower()
    sentence = nltk.tokenize.word_tokenize(sentence)
    for word in sentence.copy():
        if not any(c.isalpha() for c in word):
            sentence.remove(word)
    return sentence
    # raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []
    for subtree in tree.subtrees(lambda t: t.label() == 'NP'):
        if len(list(subtree.subtrees(lambda t: t.label() == 'NP'))) == 1:
            np_chunks.append(subtree)
    return np_chunks
    # raise NotImplementedError


if __name__ == "__main__":
    counter = 0
    for i in range(10):
        with open(f"sentences/{i + 1}.txt") as f:
            s = f.read()
            res = main(s, show=False)
            if res:
                counter += 1
            print(f"{i + 1}.txt : {res}")
    print(counter, "/ 10")
    print()
    while True:
        a = input("which: ")
        if a.isdigit():
            if int(a) < 1:
                break
            else:
                with open(f"sentences/{a}.txt") as f:
                    s = f.read()
                    main(s)
        else:
            main(a)
