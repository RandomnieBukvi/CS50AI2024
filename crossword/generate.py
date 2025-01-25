import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            for word in self.domains[var].copy():
                if len(word) != var.length:
                    self.domains[var].remove(word)
        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y]
        if not overlap:
            return False
        x_index, y_index = overlap
        revised = False
        x_domain = self.domains[x].copy()
        y_domain = self.domains[y].copy()
        for x_word in x_domain:
            constraint_satisfied = False
            for y_word in y_domain:
                if x_word[x_index] == y_word[y_index]:
                    constraint_satisfied = True
                    break
            if not constraint_satisfied:
                revised = True
                self.domains[x].remove(x_word)
        return revised
        # raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        def dequeue():
            if arcs:
                return arcs.pop(0)
            else:
                return None

        if not arcs:
            arcs = list(self.crossword.overlaps.keys())
        while len(arcs) != 0:
            x, y = dequeue()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    arcs.append((z, x))
        return True
        # raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if set(assignment) != self.crossword.variables:
            return False
        return True
        # raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var, val in assignment.items():
            if var.length != len(val):
                return False
        for var1, val1 in assignment.items():
            for var2, val2 in assignment.items():
                if var1 == var2:
                    continue
                if val1 == val2:
                    return False
        neighbors = {arc: overlap for arc, overlap in self.crossword.overlaps.items()
                     if overlap and arc[0] in assignment and arc[1] in assignment}
        for arc, overlap in neighbors.items():
            n1_val = assignment[arc[0]]
            n2_val = assignment[arc[1]]
            n1_index, n2_index = overlap
            if n1_val[n1_index] != n2_val[n2_index]:
                return False
        return True
        # raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        def get_eliminated_choices(character, index, neighbor):
            neighbor_domain = self.domains[neighbor]
            eliminated = 0
            for word in neighbor_domain:
                if word[index] != character:
                    eliminated += 1
            return eliminated

        neighbors = {neighbor for neighbor in self.crossword.neighbors(var) if neighbor not in assignment}
        domains_constrains = {}
        for domain in self.domains[var]:
            eliminated_choices = 0
            for neighbor in neighbors:
                var_index, neighbor_index = self.crossword.overlaps[var, neighbor]
                var_char = domain[var_index]
                eliminated_choices += get_eliminated_choices(var_char, neighbor_index, neighbor)
            domains_constrains[domain] = eliminated_choices
        ordered_domain = sorted(domains_constrains, key=lambda k: domains_constrains[k])
        return ordered_domain
        # raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_variables = {var for var in self.crossword.variables if var not in assignment}
        var_vals = dict()
        for var in unassigned_variables:
            remaining_vals = len(self.domains[var])
            var_vals[var] = remaining_vals
        ordered_var_vals = sorted(var_vals, key=lambda k: var_vals[k])
        min_remaining_vals = [var for var in ordered_var_vals if var == ordered_var_vals[0]]
        if len(min_remaining_vals) == 1:
            return min_remaining_vals[0]

        degrees = dict()
        for var in min_remaining_vals:
            degree = len(self.crossword.neighbors(var))
            degrees[var] = degree
        ordered_degrees = sorted(degrees, key=lambda k: degrees[k], reverse=True)
        return ordered_degrees[0]
        # raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = val

            if self.consistent(new_assignment):
                assignment[var] = val
                result = self.backtrack(assignment)
                if result:
                    return result
                assignment.pop(var)
        return None
        # raise NotImplementedError


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
