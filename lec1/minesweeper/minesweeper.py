import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __hash__(self):
        return hash(tuple(self.cells)) ^ hash(self.count)

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        # raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        # raise NotImplementedError


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = set()

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
        # print("Marked mine: ", cell)
        # print("self.knowledge")
        # for sentence in self.knowledge:
        #     print(sentence)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
        # print("Marked safe: ", cell)
        # print("self.knowledge")
        # for sentence in self.knowledge:
        #     print(sentence)

    def model_check(self):
        """
        Update the self.mines and self.safes based on the knowledge base
        Also update the knowledge base based on 2 sentences -> new sentence
        """
        new_sentences = []
        list_knowledge = list(self.knowledge)
        for i in range(len(self.knowledge)):
            for j in range(i + 1, len(self.knowledge)):
                sentence1 = list_knowledge[i]
                sentence2 = list_knowledge[j]
                if (
                    sentence1.cells.issubset(sentence2.cells)
                    and len(sentence1.cells) > 0
                ):
                    new_cells = sentence2.cells - sentence1.cells
                    new_count = sentence2.count - sentence1.count
                    new_sentence = Sentence(new_cells, new_count)
                    new_sentences.append(new_sentence)
                elif (
                    sentence2.cells.issubset(sentence1.cells)
                    and len(sentence2.cells) > 0
                ):
                    new_cells = sentence1.cells - sentence2.cells
                    new_count = sentence1.count - sentence2.count
                    new_sentence = Sentence(new_cells, new_count)
                    new_sentences.append(new_sentence)
        self.knowledge.update(new_sentences)
        mark_mines = set()
        mark_safes = set()
        for sentence in self.knowledge:
            if len(sentence.cells) == sentence.count:
                for cell in sentence.cells:
                    mark_mines.add(cell)
            elif sentence.count == 0:
                for cell in sentence.cells:
                    mark_safes.add(cell)
        for cell in mark_mines:
            self.mark_mine(cell)
        for cell in mark_safes:
            self.mark_safe(cell)
        return (
            True
            if (mark_mines or mark_safes or len(self.knowledge) > len(list_knowledge))
            else False
        )

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1
        self.moves_made.add(cell)
        # 2
        self.mark_safe(cell)
        # 3
        nearby_cells = [
            (cell[0] + i, cell[1] + j)
            for i in range(-1, 2)
            for j in range(-1, 2)
            if (i != 0 or j != 0)
            and self.height > cell[0] + i >= 0
            and self.width > cell[1] + j >= 0
            and (cell[0] + i, cell[1] + j) not in self.safes
        ]
        num_explored_mines = 0
        for nearby_cell in nearby_cells:
            if nearby_cell in self.mines:
                num_explored_mines += 1
        count -= num_explored_mines
        nearby_cells = set(
            nearby_cell for nearby_cell in nearby_cells if nearby_cell not in self.mines
        )
        self.knowledge.add(Sentence(nearby_cells, count))
        # raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        update_check = True
        self.knowledge = set(
            sentence for sentence in self.knowledge if len(sentence.cells) > 0
        )
        while update_check:
            update_check = self.model_check()
        print("Explored Mines: ", self.mines)
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        available_moves = {}
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    available_moves.setdefault((i, j), 0)
        if not available_moves:
            return None, None
        for key, value in available_moves.items():
            for sentence in self.knowledge:
                if key in sentence.cells:
                    posibility = 100 - (sentence.count * 100 / len(sentence.cells))
                    available_moves[key] = max(value, posibility)
        for key, value in available_moves.items():
            if value == 0:
                available_moves[key] = 50
        # find the move with the minimum posibility
        min_posibility = max(available_moves.values())
        prior_moves = []
        for key, value in available_moves.items():
            if value == min_posibility:
                prior_moves.append(key)
        if prior_moves:
            return random.choice(prior_moves), min_posibility
        return None, None
        # raise NotImplementedError
