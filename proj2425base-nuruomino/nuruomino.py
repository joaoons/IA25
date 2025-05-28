# nuruomino.py: Template para implementação do projeto de Inteligência Artificial 2024/2025.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 95:
# ist1103243 João Santos
# 00000 Diogo Ceia

from search import Problem, Node
import sys
from sys import stdin
import numpy as np

class NuruominoState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = Nuruomino.state_id
        Nuruomino.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id

class Board:
    """Representação interna de um tabuleiro do Puzzle Nuruomino."""

    def __init__(self, grid:list):
        self.grid = grid
        self.original = np.copy(grid)

    def adjacent_regions(self, region:int) -> list:
        """Devolve uma lista das regiões que fazem fronteira com a região enviada no argumento."""
        #letras? ou regiao da letra?
        region=str(region)
        adj_r=set()
        rows=len(self.grid)
        cols=len(self.grid[0])

        for i in range(rows):
            for j in range(cols):
                if self.grid[i][j] == region:
                    if j+1 < cols and self.grid[i][j+1] != region:
                        adj_r.add(self.grid[i][j+1])
                    
                    if j-1 >= 0 and self.grid[i][j-1] != region:
                        adj_r.add(self.grid[i][j-1])

                    if i+1 < rows and self.grid[i+1][j] != region:
                        adj_r.add(self.grid[i+1][j])

                    if i-1 >= 0 and self.grid[i-1][j] != region:
                        adj_r.add(self.grid[i-1][j])

        return list(sorted(adj_r))

    def adjacent_positions(self, row:int, col:int) -> list:
        """Devolve as posições adjacentes à região, em todas as direções, incluindo diagonais."""
        #TODO
        pass

    def adjacent_values(self, row:int, col:int) -> list:
        """Devolve os valores das celulas adjacentes à região, em todas as direções, incluindo diagonais."""

        row=row-1
        col=col-1
        adj_v=[]

        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i==0 and j==0:
                    continue
                
                if 0 <= row+i < len(self.grid) and  0 <= col+j < len(self.grid[0]):
                    adj_v.append(self.grid[row+i][col+j])

        return adj_v
    
    def get_value(self,row:int, col:int) -> str: #str?
        """Devolve o valor preenchido numa determinada posição"""

        return self.grid[row-1,col-1]
    
    def print_instance(self):
        """Imprime a grelha no formato standard output (stout)"""

        for row in self.grid:
            print('\t'.join(value for value in row))

    def regions(self) -> list:
        """Devolve uma lista com as regiões de um tabuleiro"""

        regions=set()
        rows=len(self.grid)
        cols=len(self.grid[0])

        for i in range(rows):
            for j in range(cols): 
                regions.add(self.grid[i][j])

        return list(sorted(regions))

    def fits(self, region:int, form:list) -> list:
        """Verifica se uma peça cabe em determinada região"""

        tetro_rows=len(form)
        tetro_cols=len(form[0])
        rows=len(self.grid)
        cols=len(self.grid[0])
        pos=[]

        for x in range(rows - tetro_rows + 1):
            for y in range(cols - tetro_cols + 1):
                fits_here = True 
                for i in range(tetro_rows):
                    for j in range(tetro_cols):
                        if form[i][j] == 1:
                            pos_x = x + i
                            pos_y = y + j

                            if self.grid[pos_x][pos_y] != region:
                                fits_here = False 
                                break  # No need to continue inner loop
                    if not fits_here:
                        break  # No need to continue row loop
                if fits_here:
                    pos.append((x, y))  # Only add if it fits completely

        return pos
    
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
    def __init__(self, board: Board, goal=None):
        """O construtor especifica o estado inicial."""

        super().__init__(initial=board, goal=goal)
         
    def actions(self, state: NuruominoState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        rows=len(state.board.original)
        cols=len(state.board.original[0])
        reg_free=state.board.original.regions()

        tetros=[
            [[1, 0],[1, 0],[1, 1]]
            [[0, 1],[0, 1],[1, 1]]
            [[1, 1],[1, 0],[1, 0]]
            [[1, 1],[0, 1],[0, 1]]
            [[1, 1, 1], [0, 0, 1]]
            [[0, 0, 1], [1, 1, 1]]
            [[1, 1, 1], [1, 0, 0]]
            [[1, 0, 0], [1, 1, 1]]

            [[1, 1, 1, 1]]
            [[1], [1], [1], [1]]

            [[1,1,1],[0,1,0]]
            [[0,1,0],[1,1,1]]
            [[1, 0],[1, 1],[1, 0]]
            [[0, 1],[1, 1],[0, 1]]

            [[0, 1, 1], [1, 1, 0]]
            [[1, 1, 0], [0, 1, 1]]
            [[1, 0],[1, 1],[0, 1]]
            [[0, 1],[1, 1],[1, 0]] #tenho de dividir isto provavlemenete pelos bomes das peças
        ]

        for i in range(rows):
            for j in range(cols):
                if state.board.grid[i][j] != state.board.original[i][j]:
                    reg_free.remove(int(state.board.grid[i][j]))

        for r in reg_free:
            for tetro in tetros:
                if state.board.fits(r,tetro):




    
        
        #se tem la peça, se cabe, se ha alguma a tocar igual, se faz quadrado
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

        #cada regiao com uma e so uma peça
        #juntas ortoganalmente
        #n juntas iguais
        #quadrado

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

# Ler grelha do figura 1a:
board = Board.parse_instance()
print(board.adjacent_regions(1))
print(board.adjacent_regions(3))

# Mostrar os valores de posições adjacentes
print(board.adjacent_values(2,2))