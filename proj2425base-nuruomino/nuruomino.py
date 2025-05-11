# nuruomino.py: Template para implementação do projeto de Inteligência Artificial 2024/2025.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 95:
# ist1103243 João Santos
# 00000 Diogo Ceia

from search import Problem, Node
import sys
from sys import stdin

class NuruominoState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = Nuroumino.state_id
        Nuroumino.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id

class Board:
    """Representação interna de um tabuleiro do Puzzle Nuruomino."""

    def __init__(self, grid):
        self.grid = grid #list of lists

    def adjacent_regions(self, region:int) -> list:
        """Devolve uma lista das regiões que fazem fronteira com a região enviada no argumento."""
        #e as letras????
        region=str(region)
        adj_r=set()
        rows=len(self.grid)
        cols=len(self.grid[0])

        for i in range(rows):
            for j in range(cols):
                if self.grid[i][j] == region:
                    if j+1 < cols and self.grid[i][j+1] != region:
                        adj_r.add(int(self.grid[i][j+1]))
                    
                    if j-1 >= 0 and self.grid[i][j-1] != region:
                        adj_r.add(int(self.grid[i][j-1]))

                    if i+1 < rows and self.grid[i+1][j] != region:
                        adj_r.add(int(self.grid[i+1][j]))

                    if i-1 >= 0 and self.grid[i-1][j] != region:
                        adj_r.add(int(self.grid[i-1][j]))

        return list(sorted(adj_r))

    def adjacent_positions(self, row:int, col:int) -> list:
        """Devolve as posições adjacentes à região, em todas as direções, incluindo diagonais."""
        #TODO
        pass

    def adjacent_values(self, row:int, col:int) -> list:
        """Devolve os valores das celulas adjacentes à região, em todas as direções, incluindo diagonais."""
        #TODO
        pass
    
    
    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""

        grid=[]
        for line in sys.stdin:
            row=line.strip().split()
            grid.append(row)

        return(Board(grid))

    # TODO: outros metodos da classe Board

class Nuruomino(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        #TODO
        pass 

    def actions(self, state: NuruominoState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        #TODO
        pass 

    def result(self, state: NuruominoState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        #TODO
        pass 
        

    def goal_test(self, state: NuruominoState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        #TODO
        pass 

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

# Ler grelha do figura 1a:
board = Board.parse_instance()
print(board.adjacent_regions(1))
print(board.adjacent_regions(3))