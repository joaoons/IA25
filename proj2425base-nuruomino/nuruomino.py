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
        self.id = NuruominoState.state_id
        NuruominoState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id

class Board:
    """Representação interna de um tabuleiro do Puzzle Nuruomino."""

    def __init__(self, grid:list):
        self.grid = grid
        self.original = np.copy(grid).tolist()

    def adjacent_regions(self, region:int) -> list:
        """Devolve uma lista das regiões que fazem fronteira com a região enviada no argumento."""
        #!letras? ou regiao da letra?

        adj_r=set()
        rows=len(self.grid)
        cols=len(self.grid[0])

        for i in range(rows):
            for j in range(cols):
                if self.grid[i][j] == region:
                    if j+1 < cols and self.original[i][j+1] != region:
                        adj_r.add(self.grid[i][j+1])
                    
                    if j-1 >= 0 and self.original[i][j-1] != region:
                        adj_r.add(self.grid[i][j-1])

                    if i+1 < rows and self.original[i+1][j] != region:
                        adj_r.add(self.grid[i+1][j])

                    if i-1 >= 0 and self.original[i-1][j] != region:
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

        return self.grid[row-1][col-1]
    
    def print_instance(self):
        """Imprime a grelha no formato standard output (stout)"""

        for row in self.grid:
            print('\t'.join(value for value in row))

    def orthogonal_values(self, row:int, col:int) -> list:
        """Devolve os valores das celulas adjacentes à posição, nas direções ortogonais."""
        #1 index
        row=row-1
        col=col-1
        ort_v=[]

        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i==0 and j==0:
                    continue

                if abs(i) + abs(j) != 1:
                    continue
                
                if 0 <= row+i < len(self.grid) and  0 <= col+j < len(self.grid[0]):
                    ort_v.append(self.grid[row+i][col+j])

        return ort_v
    
    def orthogonal_positions(self, row:int, col:int) -> list:
        """Devolve as posições das celulas adjacentes à posição, nas direções ortogonais."""
        #1 index
        row=row-1
        col=col-1
        ort_p=[]

        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i==0 and j==0:
                    continue

                if abs(i) + abs(j) != 1:
                    continue
                
                if 0 <= row+i < len(self.grid) and  0 <= col+j < len(self.grid[0]):
                    ort_p.append((row+i,col+j))

        return ort_p

    def regions(self, use_original=False) -> list:
        """Devolve uma lista com as regiões de um tabuleiro"""

        grid_to_scan = self.original if use_original else self.grid
        
        regions=set()
        rows=len(grid_to_scan)
        cols=len(grid_to_scan[0])

        for i in range(rows):
            for j in range(cols): 
                regions.add(grid_to_scan[i][j])

        return list(sorted(regions))
    
    def copy(self):
        """Devolve uma cópia independente do tabuleiro."""

        new_grid = np.copy(self.grid).tolist()
        new_original = np.copy(self.original).tolist()
        new_board = Board(new_grid)
        new_board.original = new_original

        return new_board

    def fits(self, region:int, form:list) -> list: #! neste momento esta 0 index mas talvez mudar 
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
                    pos.append((x, y)) 

        return pos
    
    def square(self) -> bool: 

        rows = len(self.grid)
        cols = len(self.grid[0])

        for i in range(rows - 1):
            for j in range(cols - 1):
                if (
                    isinstance(self.grid[i][j],str) and
                    isinstance(self.grid[i+1][j],str) and
                    isinstance(self.grid[i][j+1],str) and
                    isinstance(self.grid[i+1][j+1],str)
                ):
                   return True  
        return False 

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""

        grid = []
        for line in sys.stdin:
            row = [
                int(cell) if cell.isdigit() else cell
                for cell in line.strip().split()
            ]
            grid.append(row)
        return Board(grid)

class Nuruomino(Problem):
    def __init__(self, board: Board, goal=None):
        """O construtor especifica o estado inicial."""

        super().__init__(initial=board, goal=goal)
         
    def actions(self, state: NuruominoState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        rows=len(state.board.original)
        cols=len(state.board.original[0])
        reg_free=set(state.board.regions(True))
        actions=[]

        L=[
            [[1, 0],[1, 0],[1, 1]],
            [[0, 1],[0, 1],[1, 1]],
            [[1, 1],[1, 0],[1, 0]],
            [[1, 1],[0, 1],[0, 1]],
            [[1, 1, 1], [0, 0, 1]],
            [[0, 0, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 0, 0]],
            [[1, 0, 0], [1, 1, 1]]
        ]

        I=[    [[1, 1, 1, 1]],
            [[1], [1], [1], [1]]
        ]

        T=[    [[1,1,1],[0,1,0]],
            [[0,1,0],[1,1,1]],
            [[1, 0],[1, 1],[1, 0]],
            [[0, 1],[1, 1],[0, 1]]
        ]

        S=[    [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 0], [0, 1, 1]],
            [[1, 0],[1, 1],[0, 1]],
            [[0, 1],[1, 1],[1, 0]] 
        ]

        tetros = {
            'L': L,
            'T': T,
            'I': I,
            'S': S
            }

        for i in range(rows): 
            for j in range(cols):
                if state.board.grid[i][j] != state.board.original[i][j]:
                    reg_free.discard(int(state.board.original[i][j])) #! se derem um board original com peças isso buga tudo
 
        for r in reg_free: #Check if a region is free
            for tetro_name, tetro_forms in tetros.items(): 
                for tetro in tetro_forms:
                    for pos in state.board.fits(r,tetro): #Check if a Tetromino fits in a region
                        valid=True
                        copy = state.board.copy()
                        for i in range(len(tetro)):
                            for j in range(len(tetro[0])):
                                if tetro[i][j] == 1:   
                                    pos_x = pos[0] + i
                                    pos_y = pos[1] + j

                                    #print(f"Checking cell ({pos_x}, {pos_y}), piece {tetro_name}")
                                    #print("Orthogonal values:", state.board.orthogonal_values(pos_x + 1, pos_y + 1))
                                    if tetro_name in state.board.orthogonal_values(pos_x + 1, pos_y + 1): #Check if is orthogonally connected to an equal Tetromino
                                        valid = False
                                        break                   
                                    copy.grid[pos_x][pos_y] = tetro_name
                            
                            if not valid:
                                break
                            
                        if valid and not copy.square():
                            actions.append((r,tetro_name,tetro,(pos[0]+1,pos[1]+1))) 

        #se tem la peça, se cabe, se ha alguma a tocar igual, se faz quadrado
        return actions

    def result(self, state: NuruominoState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        #action = (region,name,form,pos)
        name = action[1]
        form = action[2]
        pos = (action[3][0] - 1, action[3][1] - 1)

        if action not in self.actions(state):
            print("Generated actions:")
            for a in self.actions(state):
                print(a)
            raise ValueError("Invalid action: this move is not allowed.")
        
        new_board= state.board.copy()

        for i in range(len(form)):
            for j in range(len(form[0])):
                if form[i][j] == 1:
                    new_board.grid[pos[0] + i][pos[1] + j] = name
        
        return NuruominoState(new_board)

    def goal_test(self, state: NuruominoState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        rows=len(state.board.original)
        cols=len(state.board.original[0])

        #Verificar se existe algum quadrado
        if state.board.square:
            return False

        #Verificar se todas as regioes estão preenchidas e por apenas uma peça
        reg_free = set(state.board.regions(True))
        region_pieces = {}

        for i in range(rows):
            for j in range(cols):
                region = state.board.original[i][j]
                value = state.board.grid[i][j]

                if value != region:
                    reg_free.discard(region)

                    if region not in region_pieces:
                        region_pieces[region] = value
                    elif region_pieces[region] != value:
                        return False 

        if reg_free:
            return False  

        #Verificar se todas as peças estão ligadas ortogonalmente sem estar a uma igual
        for r in state.board.regions(True):
            connect = False
            for i in range(rows):
                for j in range(cols):
                    if state.board.original[i][j] == r and state.board.grid[i][j] != r:
                        
                        for x,y in state.board.orthogonal_positions(i + 1, j + 1):
                            neighbor = state.board.grid[x][y]
                            if (neighbor == state.board.grid[i][j] and  
                                state.board.original[x][y] != r) :
                                return False

                            if isinstance(neighbor, str) and neighbor != state.board.grid[i][j]:
                                connect = True
                                break
                        if connect:
                            break
                if connect:
                    break

            if not connect:
                return False 

        return True 

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass
'''
# Ler grelha do figura 1a:
board = Board.parse_instance()
print(board.adjacent_regions(1))
print(board.adjacent_regions(3))

#Exemplo2
# Criar uma instância de Nuruomino:
problem = Nuruomino(board)
# Criar um estado com a configuração inicial:
initial_state = NuruominoState(board)
# Mostrar valor na posição (2, 1):
print(initial_state.board.get_value(2, 1))

# Realizar ação de colocar a peça L, cuja forma é [[1, 1],[1, 0],[1, 0]] na região 1
result_state = s1 = problem.result(initial_state, (1, 'L', [[1, 1],[1, 0],[1, 0]],(1,1)))
# Mostrar valor na posição (2, 1):
print(result_state.board.get_value(2, 1))
# Mostrar os valores de posições adjacentes
print(result_state.board.adjacent_values(2,2))
'''

#Exemplo 3

# Ler grelha do figura 1a:
board = Board.parse_instance()
# Criar uma instância de Nuruomino:
problem = Nuruomino(board)
# Criar um estado com a configuração inicial:
s0 = NuruominoState(board)
# Aplicar as ações que resolvem a instância
s1 = problem.result(s0, (1, 'L', [[1, 1],[1, 0],[1, 0]],(1,1)))
print("Current board after s1:")
for row in s1.board.grid:
    print(row)
s2 = problem.result(s1, (2, 'S', [[1, 0], [1, 1],[0, 1]],(1,3)))
s3 = problem.result(s2, (3, 'T', [[1, 0],[1, 1],[1, 0]],(4,4)))
s4 = problem.result(s3, (4, 'L', [[1, 1, 1],[1, 0, 0]],(5,1)))
s5 = problem.result(s4, (5, 'I', [[1],[1],[1],[1]],(3,6)))
# Verificar se foi atingida a solução
print("Is goal?", problem.goal_test(s2))
print("Is goal?", problem.goal_test(s5))
print("Solution:\n", s5.board.print(), sep="")