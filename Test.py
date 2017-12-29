import BayesianNetwork
import matplotlib.pyplot as plt
import time
import Function

myNet = BayesianNetwork.NetWork()

A = myNet.addNode(BayesianNetwork.Node("BreakUp", "BU", None, "bu.csv", 0))
B = myNet.addNode(BayesianNetwork.Node("RelativeLost", "RL", None, "rl.csv", 1))
C = myNet.addNode(BayesianNetwork.Node("FinancialProblem", "FNP", None, "fnp.csv", 2))
D = myNet.addNode(BayesianNetwork.Node("WorkStudyPressure", "WSP", None, "wsp.csv", 3))
E = myNet.addNode(BayesianNetwork.Node("NoFriends&Family", "NFF", None, "nff.csv", 4))
F = myNet.addNode(BayesianNetwork.Node("SeriousIllness", "SIL", None, "sil.csv", 5))
G = myNet.addNode(BayesianNetwork.Node("EmotionalShock", "ES", [0, 1], "es.csv", 6))
H = myNet.addNode(BayesianNetwork.Node("Depression", "DEP", [4, 6], "dep.csv", 7))
I = myNet.addNode(BayesianNetwork.Node("ChronicStress", "CST", [2, 3], "cst.csv", 8))
L = myNet.addNode(BayesianNetwork.Node("Insomnia", "INS", [8], "ins.csv", 9))
M = myNet.addNode(BayesianNetwork.Node("PriorStroke", "PS", [5], "ps.csv", 10))
N = myNet.addNode(BayesianNetwork.Node("Suicide", "SU", [7, 8, 10], "su.csv", 11))

dim = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 900, 1000, 1250, 1500, 2000]
results = []
varianza = []

tempo_iniziale = time.time()

for i in range(0, len(dim)):
    tmp = []
    for j in range(0, 10):
        myNet.createDataSet(dim[i], "dataset.csv")
        myNet.learning("dataset.csv")
        tmp.append(myNet.divergenza())
    print "Test con Dim = " + str(dim[i]) + " Terminato"

    avg = sum(tmp) / len(tmp)
    varianza.append(Function.varianza(tmp, avg))

    results.append(avg)

tempo_finale = time.time()
print "Impiegati", str(tempo_finale - tempo_iniziale), "secondi."

plt.plot(dim, results, color='lightblue', linewidth=2)
plt.fill_between(dim, Function.diff(results, varianza), Function.plus(results, varianza), alpha=0.5,
                 edgecolor='#CC4F1B', facecolor='#FF9848')
plt.grid()
plt.ylabel('Kullback-Leibler Divergence')
plt.xlabel('Dimension of DataSet')
plt.title('Learning Curve')
plt.show()
