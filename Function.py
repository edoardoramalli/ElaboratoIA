import itertools
import numpy as np
import math


def e(n):
    result = []
    l = ["".join(seq) for seq in itertools.product("01", repeat=n)]
    for i in range(0, len(l)):
        result.append(map(int, str(l[i])))
    return result


def selectRow(matrix, mask):
    index = []
    for i in range(0, matrix.shape[0]):
        row = matrix[i][:]
        if checkRow(row, mask) == True:
            index.append(i)
    return matrix[index][:]


def checkRow(r, mask):
    for i in range(0, len(mask)):
        if not (math.isnan(mask[i])):
            if mask[i] != r[i]:
                return False
    return True


def createMask(l, nodo, net):
    numNodi = len(net.list)
    mask = np.zeros(shape=(len(l), numNodi))
    typeP = nodo.parents
    for el in range(0, len(l)):
        index = 0
        for k in range(0, mask.shape[1]):
            if index < len(typeP) and k == typeP[index]:
                mask[el][k] = int(l[el][index])
                index = index + 1
            else:
                mask[el][k] = None
    return mask


def translateBool(num):
    if num == 1:
        return "True"
    return "False"


def readMask(mask, net):
    s = ""
    for i in range(0, len(mask)):
        if not (math.isnan(mask[i])):
            s = s + " " + net.listName[i] + " = " + translateBool(mask[i]) + "  "
    return s


def varianza(x, avg):
    sum = 0
    for i in range(0, len(x)):
        sum = sum + ((x[i] - avg) ** 2)
    num = sum / (len(x) - 1)
    num = math.sqrt(num)
    return num


def diff(x, y):
    tmp = []
    for i in range(0, len(x)):
        tmp.append(x[i] - y[i])
    return tmp


def plus(x, y):
    tmp = []
    for i in range(0, len(x)):
        tmp.append(x[i] + y[i])
    return tmp
