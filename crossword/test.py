import time

from generate import *


def test(structure, words, output=None):
    # Check usage
    # if len(sys.argv) not in [3, 4]:
    #     sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    # structure = sys.argv[1]
    # words = sys.argv[2]
    # output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(f"data/{structure}", f"data/{words}")
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


start_time = time.time()
test('structure2.txt', 'words2.txt', 'test1.png')
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")