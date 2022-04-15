import numpy as np
import matplotlib.pyplot as plt

DNA_SIZE = 10  # DNA length
POP_SIZE = 100  # population size
CROSS_RATE = 0.8  # mating probability (DNA crossover)
MUTATION_RATE = 0.003  # mutation probability
N_GENERATIONS = 60  # 有多少代
X_BOUND = [0, 5]  # 横坐标范围


def F(x):
    return np.sin(10 * x) * x + np.cos(2 * x) * x  # to find the maximum of this function


# find non-zero fitness for selection
# 可以拿到非负值
def get_fitness(pred):
    return pred + 1e-3 - np.min(pred)


# convert binary DNA to decimal and normalize it to a range(0, 5)
# 解码
def translateDNA(pop):
    """[2^9, 2^8, ..., 2^0]  对应除以 1023 再与dna列对应相乘并相加 最后扩大5倍"""
    return pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * X_BOUND[1]


def select(pop, fitness):  # nature selection wrt pop's fitness
    # 第一个参数np.arange(POP_SIZE)，是数组0-99，表示被抽样的数组
    # p是概率数组，这里是100个数
    idx = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True,
                           p=fitness / fitness.sum())
    # print("idx:", idx)
    return pop[idx]


def crossover(parent, pop):  # mating process (genes crossover)
    """随机生成10个bool型，True的位置表示被选中"""
    """将pop_copy被选中的部分赋值给pop被选中的部分， 从而完成交叉"""
    if np.random.rand() < CROSS_RATE:
        i_ = np.random.randint(0, POP_SIZE, size=1)  # select another individual from pop
        cross_points = np.random.randint(0, 2, size=DNA_SIZE).astype(np.bool)  # choose crossover points
        # print("cross_points:", cross_points)
        # print("parent: ", parent)
        # print("parent[cross_points]: ", parent[cross_points])
        # print("pop[i_, cross_points]: ", pop[i_, cross_points])
        parent[cross_points] = pop[i_, cross_points]  # mating and produce one child
    return parent


def mutate(child):
    """对每个基因进行判断，满足概率就变异 1->0, 0->1"""
    for point in range(DNA_SIZE):
        if np.random.rand() < MUTATION_RATE:
            child[point] = 1 if child[point] == 0 else 0
    return child


# 100个染色体，每个染色体10个DNA
pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))
plt.ion()  # 打开交互模式，防止图片生成后阻塞
x = np.linspace(*X_BOUND, 200)
plt.plot(x, F(x))


for i in range(N_GENERATIONS):
    F_values = F(translateDNA(pop))    # compute function value by extracting DNA

    # 逐代绘制,绘制前先清除上一代的
    if 'sca' in globals():
        sca.remove()
    # 画散点图
    sca = plt.scatter(translateDNA(pop), F_values, s=200, lw=0, c='red', alpha=0.5)
    plt.pause(0.05) # 控制每张图片暂停多少秒

    # GA part (evolution)
    fitness = get_fitness(F_values)
    print("{}th Most fitted DNA: {}".format(i + 1, pop[np.argmax(fitness), :]))
    print("the solution x is {}".format(translateDNA(pop[np.argmax(fitness), :])))
    pop = select(pop, fitness)
    pop_copy = pop.copy()
    for parent in pop:
        child = crossover(parent, pop_copy)
        child = mutate(child)
        parent[:] = child       # 父亲被孩子替代


# 显示前关掉交互模式
plt.ioff()
plt.show()
