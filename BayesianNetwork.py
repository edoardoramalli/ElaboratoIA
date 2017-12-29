import csv
import numpy as np
import random
import Function
import math


class Node:
    name = ""
    nickname = ""
    parents = []
    cpt = None
    cptLearned = None

    def __init__(self, na, ni, p, s, t):
        self.name = na
        self.nickname = ni
        self.parents = p
        self.addCpt(s)
        self.type = t

    def addCpt(self, string):
        self.cpt = np.array(list(csv.reader(open(string, "rb"), delimiter=" "))).astype("float")

    def getCpt(self, list, type):
        row = 0
        failure = 0
        if type == 0:
            table = self.cpt
        else:
            table = self.cptLearned

        for i in range(0, table.shape[0]):
            failure = 0
            for j in range(0, table.shape[1] - 1):
                if table[i][j] != list[j]:
                    failure = 1
                    break
            if failure == 0:
                row = i
                break
        return table[row][table.shape[1] - 1]

    def getParents(self):
        return self.parents


class NetWork:
    list = []
    listName = []

    def __init__(self):
        self.list = []

    def addNode(self, Node):
        self.list.append(Node)
        self.listName.append(Node.nickname)
        return self

    def getCP(self, index, list, type):
        # Se il nodo non ha padri bisogna mettere list =[1]
        mnode = self.list[index]
        return mnode.getCpt(list, type)

    def createRowOfDataSet(self):
        row = []
        for i in range(0, len(self.list)):
            var = self.list[i]
            genitori = var.getParents()
            if genitori is None:
                teta = self.list[i].getCpt([1], 0)
                num = random.random()
                if num <= teta:
                    row.append(1)
                else:
                    row.append(0)
            else:
                temp = []
                for k in range(0, len(genitori)):
                    temp.append(row[genitori[k]])
                teta = self.list[i].getCpt(temp, 0)
                num = random.random()
                if num <= teta:
                    row.append(1)
                else:
                    row.append(0)
        return row

    def createDataSet(self, n, add):
        self.dataSet = np.zeros((n, len(self.list)), dtype=np.int)

        for i in range(0, n):
            newrow = self.createRowOfDataSet()
            self.dataSet[i] = newrow
        np.savetxt(add, self.dataSet, delimiter=" ")

    def learning(self, add):
        data = np.array(list(csv.reader(open(add, "rb"), delimiter=" "))).astype("float")
        for i in range(0, len(self.list)):
            var = self.list[i]
            genitori = var.getParents()
            if genitori == None:

                results = np.zeros((1, 2))

                # print "Node: " + var.name + " Ha 0 Padri"

                num = 0.0
                den = data.shape[0]
                for j in range(0, den):
                    if data[j][var.type] == 1:
                        num = num + 1
                teta = (num + 1) / (den + 2) #Laplace Smoothing
                teta = round(teta, 3)

                # print "Teta of " + str(var.name) + " is " + str(teta)

                results[0][0] = 1
                results[0][1] = teta
                var.cptLearned = results
                # np.savetxt(var.nickname + "learned.csv", results, delimiter=" ")
            else:
                rif = Function.e(len(genitori))
                mask = Function.createMask(rif, var, self)
                numGen = len(genitori)

                # print "Node: " + var.name + " Ha " + str(numGen) + " Padri"

                results = np.zeros((mask.shape[0], numGen + 1))

                for j in range(0, mask.shape[0]):
                    currentMask = mask[j][:]
                    ex = []
                    ex = rif[j][:]
                    temp = Function.selectRow(data, currentMask)
                    den = temp.shape[0]
                    num = 0.0
                    for riga in range(0, den):
                        if temp[riga][var.type] == 1:
                            num = num + 1
                    teta = (num + 1) / (den + 2) #Laplace Smoothing
                    teta = round(teta, 3)

                    # print "Teta of " + str(var.name) + " is " + str(teta) + " with " + Function.readMask(currentMask,
                    #                                                                                     self)
                    ex.append(teta)
                    results[j][:] = ex
                    var.cptLearned = results
                    # np.savetxt(var.nickname + "learned.csv", results, delimiter=" ")
                    # print "--------------------------------------"

    def support(self, index, list):
        node = self.list[index]
        listParents = node.getParents()
        mask = []
        iter = 0
        for i in range(0, len(list)):
            if iter >= len(listParents):
                break
            if listParents[iter] == i:
                mask.append(list[i])
                iter = iter + 1
        return mask

    def CPD(self, list, type):
        num = 1.0
        for i in range(0, 6):
            value = self.getCP(i, [1], type)
            if list[i] == 0:
                value = 1 - value
            num = num * value

        for j in range(6, len(list)):
            val = self.getCP(j, self.support(j, list), type)
            if list[j] == 0:
                val = 1 - val
            num = num * val
        return num

    def divergenza(self):
        numNode = len(self.list)
        matrix = Function.e(numNode)
        div = 0
        for i in range(0, len(matrix)):
            myset = matrix[i][:]
            esatta = self.CPD(myset, 0)
            stimata = self.CPD(myset, 1)
            div = div + (esatta * (math.log10(esatta / stimata)))
        return div
