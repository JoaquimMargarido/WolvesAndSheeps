''' *************** CONTAINER ************** '''
from random import randrange
import tkinter as tk
from datetime import datetime
import random
import copy


class container():
    scenario = tk.Tk()
    scenario.resizable(width=False, height=False)

    ocupied_positions = []
    cell_size = 12
    agents_list = []  # lista com todos os agentes do cenário

    stopSimulation = 0

    def __init__(self, titulo=""):
        self.titulo = titulo
        self.DrawToolBar()
        self.scenario.title(titulo)
        # self.cells_data = { }
        self.infected_cells = {}

    # Posicionar os tijolos
    def setOccupiedCells(self):
        self.occupied = [[0 for j in range(self.width)] for i in range(self.height)]
        x = 0  # Contador de linhas
        with open(self.mazeFile, "r") as f:
            for line in f:
                linha = line.split(';')
                if (x < self.height):
                    z = 0
                    for li in linha:
                        if z < self.width:
                            self.occupied[x][z] = linha[z]
                            z += 1

                # print(linha)
                x += 1
        # ler linha a linha

        # print(self.occupied)
        # Paint the maze cells
        for x in range(self.width):
            for z in range(self.height):
                if (self.occupied[x][z] == '1'):
                    self.drawBrick(x, z, "#0000ff")
                else:
                    self.drawBrick(x, z, "#FFFFFF")
        # sys.exit()

    def grid(self, width=0, height=0, file=""):
        self.width = width
        self.height = height
        self.mazeFile = file

        # Criar o dicionário com as propriedades das celulas
        for i in range(0, width * height - 1):
            xx = i * self.cell_size
            if (xx > width * self.cell_size):
                xx = 0

            yy = int(i / width) * self.cell_size

        if (len(file) > 0):
            self.width, self.height = self.getMazeWidthAndHeight(file)
        else:
            self.labirinto = False

        # creates a 2D array with the position of each agent
        self.ocupied_positions = [[0 for x in range(self.height)] for y in range(self.width)]

        self.canvas = tk.Canvas(self.scenario, width=self.width * self.cell_size,
                                height=self.height * self.cell_size + 10,
                                bg="white")

        # desenhar as linhas das colunas
        for i in range(0, (self.width + 1) * self.cell_size, self.cell_size):
            self.canvas.create_line(i, 0, i, self.height * self.cell_size)  # coluna, linha

        # desenhar as linhas das linhas
        for i in range(0, (self.height + 1) * self.cell_size, self.cell_size):
            self.canvas.create_line(0, i, self.width * self.cell_size, i)  # coluna, linha

        self.canvas.pack(side=tk.LEFT, anchor=tk.N)

        if (len(self.mazeFile) > 0):
            self.setOccupiedCells()

    def DrawToolBar(self):
        self.toolbar = tk.Frame(self.scenario, bg="lightgray")

        self.stopButton = tk.Button(self.toolbar, text="Stop simulation", command=self.StopSimulation)
        self.stopButton.grid(row=0, column=0, sticky="W")

        self.population = tk.Label(self.toolbar, text="Population: ")
        self.population.grid(row=1, column=0, sticky="E")
        self.popNum = tk.Label(self.toolbar, text="50")
        self.popNum.grid(row=1, column=1, sticky="")

        self.infected = tk.Label(self.toolbar, text="Infected: ")
        self.infected.grid(row=2, column=0, sticky="E")
        self.infectedNum = tk.Label(self.toolbar, text="1")
        self.infectedNum.grid(row=2, column=1, sticky="W")

        self.deaths = tk.Label(self.toolbar, text="Deaths: ")
        self.deaths.grid(row=3, column=0, sticky="E")
        self.deathsNum = tk.Label(self.toolbar, text="0")
        self.deathsNum.grid(row=3, column=1, sticky="W")

        self.cells_infected = tk.Label(self.toolbar, text="Infected cells: ")
        self.cells_infected.grid(row=5, column=0, sticky="E")
        self.cells_infectedNum = tk.Label(self.toolbar, text="0")
        self.cells_infectedNum.grid(row=5, column=1, sticky="W")

        self.toolbar.pack(side=tk.LEFT, fill=tk.X)

    def StopSimulation(self):
        self.stopSimulation = 1;

    def iniciar(self):
        self.posicionar_agentes()
        self.animar()
        self.scenario.mainloop()

    def addAgents(self, agents_list):
        self.agents_list = agents_list

    def draw_agent(self, index, x, y):
        # x = column of the cell
        # y = line of the cell
        # ex: (5, 3) = célula na coluna 5 e linha 3
        # posição para desenhar col = 5 * self.cell_size, linha = 3 * self.cell_size
        cor = self.agents_list[index].getColor()
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        corpo = self.agents_list[index].getCorpo()
        if corpo == 'rect':
            self.rect(x1, y1, x1 + self.cell_size, y1 + self.cell_size, cor, "black")
        elif corpo == 'circulo':
            self.circulo(x1, y1, x1 + self.cell_size, y1 + self.cell_size, cor, "black")

    # posicionar os agentes aleatóriamente
    def posicionar_agentes(self):
        # Está aqui o erro
        zasc = len(self.ocupied_positions)
        if (len(self.mazeFile) > 0):
            zusca = len(self.occupied)
        for n in range(len(self.agents_list)):
            nao_existe = 0

            while nao_existe == 0:
                random.seed(datetime.now())
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

                if (len(self.mazeFile) > 0):
                    if self.ocupied_positions[x][y] == 0 and self.occupied[y][x] != '1':  # se esta celula estiver livre
                        self.agents_list[n].setPosition(x, y)
                        self.ocupied_positions[x][y] = self.agents_list[n]
                        x *= self.cell_size
                        y *= self.cell_size
                        nao_existe = 1
                        bk_color = self.agents_list[n].getColor()
                        self.rect(x, y, x + self.cell_size, y + self.cell_size, bk_color, "black")
                else:
                    if self.ocupied_positions[x][y] == 0:  # se esta celula estiver livre
                        self.agents_list[n].setPosition(x, y)
                        self.ocupied_positions[x][y] = self.agents_list[n]
                        x *= self.cell_size
                        y *= self.cell_size
                        nao_existe = 1
                        bk_color = self.agents_list[n].getColor()
                        self.rect(x, y, x + self.cell_size, y + self.cell_size, bk_color, "black")

    def rect(self, x, y, x1, y1, fill_, outline_):
        self.canvas.create_rectangle(x, y, x1, y1, fill=fill_, outline=outline_)

    def circulo(self, x, y, x1, y1, fill_, outline_):
        self.canvas.create_oval(x + 1, y + 1, x1 - 1, y1 - 1, fill=fill_, outline=outline_)

    def animar(self):
        num_agents = len(self.agents_list)
        counter = 0;

        while self.stopSimulation == 0:
            counter += 1
            n = random.randint(0, len(self.agents_list) - 1)  # é seleccionado um agente ao acaso é movido
            # ler a posiçao do agente seleccionado
            x, y = self.agents_list[n].getPosition()
            # Eliminar o agente na célula corrente
            x1 = x * self.cell_size
            y1 = y * self.cell_size

            # verificar se o agente está infectado
            infected = self.agents_list[n].getHealthState()
            if (infected == 1):  # if the agent is infected
                cor = 'red'
                # marcar a célula como infectada

                self.add_to_infected(x1, y1)
            else:
                cor = 'white'
                cor = self.cell_is_infected(x1, y1)
            # limpar a posição corrente do agente
            self.rect(x1, y1, x1 + self.cell_size, y1 + self.cell_size, cor, "black")
            # posicionar o agente em nova célula
            # consultar literatura para compreender como se move o agente

            # Nova posição do agente
            # x, y = self.NewPosition(x, y)

            ##################################################
            # Mover o agente

            x, y = self.agents_list[n].getNewPosition(self)
            ##################################################

            self.agents_list[n].setPosition(x, y)
            x1 = x * self.cell_size
            y1 = y * self.cell_size
            # mover o agente para a nova posição
            corpo = self.agents_list[n].getCorpo()
            # id = self.agents_list[n].getId()
            cor = self.agents_list[n].getColor()
            if corpo == 'rect':
                self.rect(x1, y1, x1 + self.cell_size, y1 + self.cell_size, cor, "black")
            elif corpo == 'circulo':
                self.circulo(x1, y1, x1 + self.cell_size, y1 + self.cell_size, cor, "black")

            # check if the agent moved to an infected cell
            self.evaluate_agent_infection(n, x1, y1)
            # check to see if this agent moved close to an infected agent
            risk_movement = self.getInfectedNeighbours(self.agents_list[n], n);
            if (risk_movement == 1):
                prob_infection = self.agents_list[n].get_infection_probability();
                rand_num = random.randint(0, 100)
                print("Infection probability: " + str(prob_infection) + "  - Random num: " + str(rand_num))
                if (rand_num > prob_infection):
                    print("Agent " + n + " infected")
                    self.agents_list[n].setHealthState()
            # self.InfluenceNeighbors(x, y, n)  # rotina para influenciar os vizinhos

            self.scenario.update()
            if (counter == num_agents * 2):
                # when the counter is equal to the number of agents it is time to change the color of the infected cells
                self.change_color_of_infected_cells()
                self.count_infected_agents()
                counter = 0
                # self.clean_infected_list()

    # def NewPosition(self, x, y):
    #     existe = 1
    #
    #     while existe == 1:
    #         random.seed(datetime.now())
    #         novo_local = random.randint(1, 8)
    #         if novo_local == 1:
    #             x -= 1
    #             y -= 1
    #             x, y = self.checkBounderies(x, y)
    #         elif novo_local == 2:
    #             y -= 1
    #             x, y = self.checkBounderies(x, y)
    #         elif novo_local == 3:
    #             x += 1
    #             y -= 1
    #             x, y = self.checkBounderies(x, y)
    #         elif novo_local == 4:
    #             x -= 1
    #             x, y = self.checkBounderies(x, y)
    #         elif novo_local == 5:
    #             x += 1
    #             x, y = self.checkBounderies(x, y)
    #         elif novo_local == 6:
    #             x -= 1
    #             y += 1
    #             x, y = self.checkBounderies(x, y)
    #         elif novo_local == 7:
    #             y += 1
    #             x, y = self.checkBounderies(x, y)
    #         else:
    #             x += 1
    #             y += 1
    #             x, y = self.checkBounderies(x, y)
    #
    #         # Verificar se a nova celula está ocupada
    #         for n in range(0, len(self.agents_list) - 1):
    #             x1, y1 = self.agents_list[n].getPosition()
    #             if (len(self.mazeFile) > 0):
    #                 if (x1 == x) and (y1 == y) or (self.occupied[x][y] == '1'):
    #                     existe = 1
    #                     break
    #                 else:
    #                     existe = 0
    #             else:
    #                 if (x1 == x) and (y1 == y):
    #                     existe = 1
    #                     break
    #                 else:
    #                     existe = 0
    #
    #     return x, y

    # O método checkBounderies verifica se a nova coordenada calculada não sai fora do ecrã
    def checkBounderies(self, x, y):
        if x < 0:
            x = self.width - 1  # 0
        if y < 0:
            y = self.height - 1  # 0
        if x >= self.width:
            x = 0  # self.width-1
        if y >= self.height:
            y = 0  # self.width-1

        return x, y

    def add_to_infected(self, x, y):
        add_new = 1
        # If this cell already exists in the list updates the turn to 3
        for p_id, p_info in self.infected_cells.items():
            if (p_info.get("x") == x and p_info.get("y") == y):
                p_info["turn"] = 3
                add_new = 0

        if (add_new == 1):
            s = 0
            for k, v in self.infected_cells.items():
                if (self.infected_cells[s]["turn"] > 0):
                    s += 1

            self.cells_infectedNum['text'] = s
            self.infected_cells[s] = {}
            self.infected_cells[s]["x"] = x
            self.infected_cells[s]["y"] = y
            self.infected_cells[s]["turn"] = 3

    def cell_is_infected(self, x, y):
        cor = "white"
        for p_id, p_info in self.infected_cells.items():
            if (p_info.get("x") == x and p_info.get("y") == y):
                if (p_info.get("turn") == 3):
                    cor = "red"
                    break
                elif (p_info.get("turn") == 2):
                    cor = "orange"
                    break
                elif (p_info.get("turn") == 1):
                    cor = "yellow"
                    break
                elif (p_info.get("turn") == 0):
                    cor = "white"
                    break
        return cor

    def change_color_of_infected_cells(self):
        for k, v in self.infected_cells.items():
            # print(k, v)
            v["turn"] = v["turn"] - 1
            x = v["x"]
            y = v["y"]
            cor = self.cell_is_infected(x, y)
            self.rect(x, y, x + self.cell_size, y + self.cell_size, cor,
                      "black")  # <==========================================
            # Redraw the agent in the cell if it is occupied
            self.redraw_agent(x, y);

        self.clean_infected_list()

        # remove the cells from the list which turn value is 0 - these ones are no longer infected
        tmp = copy.deepcopy(self.infected_cells)

        self.infected_cells = {}
        self.infected_cells = copy.deepcopy(tmp)
        # print("terminado: ", len(self.infected_cells))

    def clean_list_of_infected_cells(self):
        # remove cells not infected anymore
        tmp = copy.deepcopy(self.infected_cells)
        for k, v in self.infected_cells.items():
            if (v["turn"] == 0):
                x = v['x']
                y = v['y']
                self.rect(x, y, x + self.cell_size, y + self.cell_size, 'white',
                          "black")  # <==========================================
                del tmp[k]

        self.clean_infected_list()

        self.infected_cells = {}
        self.infected_cells = copy.deepcopy(tmp)

    def evaluate_agent_infection(self, index, x1, y1):
        # infects the agent when it moves to an infected cell

        for k, v in self.infected_cells.items():
            x = v["x"]
            y = v["y"]
            infected = v["turn"]
            if (x == x1 and y == y1 and infected > 0):
                # Calculate the probabilities of infection
                prob_infection = self.agents_list[index].get_infection_probability();
                rand_num = random.randint(0, 100)
                print("Infection probability: " + str(prob_infection) + "  - Random num: " + str(rand_num))
                if (rand_num > prob_infection):
                    self.agents_list[index].setHealthState()
                    # inf = self.agents_list[index].getHealthState()
                # print(inf)

    def redraw_agent(self, x, y):
        for n in range(len(self.agents_list)):
            x1, y1 = self.agents_list[n].getPosition()
            if (x == x1 and y == y1):
                self.draw_agent(n, x, y)

    def clean_infected_list(self):
        return
        list = []
        for k, v in self.infected_cells.items():
            if (v["turn"] == 0):
                list.append(k)

        for n in range(len(list)):
            cell = self.infected_cells.get(list[n])
            x = cell["x"]
            y = cell["y"]
            self.rect(x, y, x + self.cell_size, y + self.cell_size, "white",
                      "black")  # <==========================================
            del self.infected_cells[list[n]]
        # update label of infected cells
        num_infected = len(self.infected_cells)
        self.cells_infectedNum["text"] = num_infected

        # print("ok");

    def count_infected_agents(self):
        # update label of infected agents
        num_infected_agents = 0
        # for k, v in self.agents_list.items():
        for n in range(len(self.agents_list)):
            if (self.agents_list[n].getHealthState() == 1):
                num_infected_agents += 1

        self.infectedNum["text"] = num_infected_agents

    def getInfectedNeighbours(self, agent, index):
        infected_neighbour = 0
        x, y = agent.getPosition()
        for t in range(0, len(self.agents_list) - 1):
            if (t != index):
                if (self.agents_list[t].getHealthState == 1):
                    # calculate proximity
                    x1, y1 = self.agents_list[t].getPosition()
                    if (x1 == x + 1 or x1 == x - 1):
                        if (y1 == y or y1 == y + 1 or y1 == y - 1):
                            infected_neighbour = 1
                    # if the agents are in the extremes of the container
                    if (x == 0 and x1 == self.width - 1):
                        infected_neighbour = 1;
                    if (x == self.width - 1 and x1 == 0):
                        infected_neighbour = 1
                    if (y == 0 and y1 == self.height - 1):
                        infected_neighbour = 1
                    if (y == self.height - 1 and y1 == 0):
                        infected_neighbour = 1;

        return infected_neighbour
