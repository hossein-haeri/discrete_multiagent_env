import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns;


class Agent:
    def __init__(self, world_size, possible_actions, power, id):
        self.id = id
        self.A = possible_actions
        self.position = np.array([np.random.choice(world_size[0]-1), np.random.choice(world_size[1]-1)])
        self.action = self.A[np.random.choice(len(self.A))]
        self.power = power

    def select_action(self):
        self.action = self.A[np.random.choice(len(self.A))]

    def take_action(self):
        if np.random.rand() < self.power:
            self.position += self.action


class World:
    def __init__(self, size):
        self.world_length_x = size[0]
        self.world_length_y = size[1]
        self.is_collision = True


    def resolve_interactions(self, agents):
        self.is_collision = True
        while self.is_collision:
            self.is_collision = False
            for agent in agents:
                for neighbor in agents:
                    if (agent.position[0] == neighbor.position[0]) and (agent.position[1] == neighbor.position[1]) and (agent.id != neighbor.id):
                        self.is_collision = True
                        if np.random.rand() < agent.power/(agent.power + neighbor.power): # if agent wins:
                            neighbor.position -= agent.action
                        else:
                            agent.position -= neighbor.action

            for agent in agents:
                if not (0 <= agent.position[0] <= self.world_length_x-1):
                    self.is_collision = True
                    agent.position[0] = np.max([agent.position[0], 0])
                    agent.position[0] = np.min([agent.position[0], self.world_length_x-1])
                if not (0 <= agent.position[1] <= self.world_length_y-1):
                    self.is_collision = True
                    agent.position[1] = max([agent.position[1], 0])
                    agent.position[1] = min([agent.position[1], self.world_length_y-1])
                # print (agent.position)


num_agents = 80
world_size = [100, 100]
possible_actions = np.array([[0, 0], [0, 1], [0, -1], [1, 0], [-1, 0]])

world = World(world_size);

agents = []
for i in range(num_agents):
    if i < 40:
      power = 0.2
    else:
      power = 0.9
    agents.append(Agent(world_size,possible_actions, power, i))

while 1:
    for agent in agents:
        agent.select_action()
        agent.take_action()

    world.resolve_interactions(agents)

    # map = np.zeros(world_size)
    plt.cla()
    for agent in agents:
        # print(agent.position)
        plt.scatter(agent.position[0],agent.position[1], c='#1f77b4', alpha=agent.power, marker='s')

        # map[agent.position] = agent.power
    # plt.show()
    # ax = sns.heatmap(map)
    plt.xlim(-1,world_size[0])
    plt.ylim(-1,world_size[1])
    plt.pause(0.01)
