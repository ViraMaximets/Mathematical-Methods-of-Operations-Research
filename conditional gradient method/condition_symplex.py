import copy
import sys

big_int = 1


def read_matrix():
    f = open("matrix", "r")
    mat = []
    Func = []  # функція цілі
    Function = f.readline()  # функція цілі
    for num in Function.split():
        Func.append(float(num))
    for line in f.readlines():
        mat.append([float(x) for x in line.split()])

    b = []
    for i in range(len(mat)):
        b.append(mat[i][len(mat[i]) - 1])
    for j in range(len(mat)):
        del (mat[j][len(mat[i]) - 1])
    f.close()
    return Func, mat, b


def addVector(Fm, Fc, A, q, pos, basis):
    if q == 1:
        for i in range(len(A)):
            if i != pos:
                A[i].append(0)
            else:
                A[i].append(1)
        Fm.append(0)
        Fc.append(0)
        basis.append(int(len(Fm) - 1))
    else:
        for i in range(len(A)):
            if i != pos:
                A[i].append(0)
            else:
                A[i].append(-1)
        Fm.append(0)
        Fc.append(0)

        for i in range(len(A)):
            if i != pos:
                A[i].append(0)
            else:
                A[i].append(1)
        Fm.append(big_int)
        Fc.append(0)
        basis.append(int(len(Fm) - 1))


def find_biggstM(summ):  # шукаємо найбільше по М
    biggest = -999999
    index = []
    for i in range(len(summ)):
        if summ[i] > biggest:
            biggest = summ[i]
            index.clear()
            index.append(i)
            continue
        if summ[i] == biggest:
            index.append(i)
    #if biggest <= 0:
     #   print("\nУсі delta задовольняють умову оптимальності! 67")
      #  return -1
    return index


def find_biggstC(index, sumc):  # якщо є 2 одн М, то шукаємо найбільше по числу
    biggestС = -9999999
    ind_col = -1
    for i in index:
        if sumc[i] > biggestС:
            biggestС = sumc[i]
            ind_col = i
    if biggestС <= 0:
        print("\nУсі delta задовольняють умову оптимальності! 80")
        return -1
    return ind_col


def find_ind_row(b, D, ind_col):  # знайти індекс напрямного рядка
    mins = []
    for i in range(len(b)):
        q = b[i] / D[i][ind_col]
        if q > 0:
            mins.append(q)
        else:
            mins.append(9999999)
    return mins.index(min(mins))


def symplex_method(D, b, Cc, Cm, Fc, Fm, ind_row, ind_col, basis, sumc, summ):
    for iterations in range(5):
        # 0.save
        b_old = copy.deepcopy(b)
        D_old = copy.deepcopy(D)

        # 1. new basis
        basis[ind_row] = ind_col

        # 2. new C
        Cc[ind_row] = Fc[ind_col]
        Cm[ind_row] = Fm[ind_col]

        # 3. new b
        for i in range(len(b_old)):
            if i != ind_row:
                b[i] = b_old[i] - (b_old[ind_row] / D_old[ind_row][ind_col]) * D_old[i][ind_col]
            else:
                b[i] = b_old[i] / D_old[ind_row][ind_col]

        # 4. new bsumc bsumm
        bsumc = 0
        for i in range(len(Cc)):
            bsumc += (Cc[i] * b[i])
        bsumm = 0
        for i in range(len(Cm)):
            bsumm += (Cm[i] * b[i])

        # 5. new Simplex matrix      D_old[ind_row][ind_col]
        for i in range(len(D)):
            D[i][ind_col] = 0

        D[ind_row][ind_col] = 1

        for i in range(len(D[ind_row])):
            if i != ind_col:
                D[ind_row][i] = D_old[ind_row][i] / D_old[ind_row][ind_col]

        for row in range(len(D)):
            if row != ind_row:
                for col in range(len(D[row])):
                    if col != ind_col:
                        D[row][col] = D_old[row][col] - (D_old[ind_row][col] / D_old[ind_row][ind_col]) * D_old[row][
                            ind_col]

        print("\n-------------------------------------------------------------------")
        print("Матриця коефіцієнтів: ")
        print('\n'.join(['\t'.join(['{:4}'.format(round(item, 2)) for item in row]) for row in D]))

        # 6. new sumc summ
        sumc.clear()
        summ.clear()

        for col in range(len(D[0])):
            sum = 0
            for row in range(len(D)):
                sum += (Cc[row] * D[row][col])
            sum -= Fc[col]
            sumc.append(sum)
        for col in range(len(D[0])):
            sum = 0
            for row in range(len(D)):
                sum += Cm[row] * D[row][col]
            sum -= Fm[col]
            summ.append(sum)
            # знайти індекс напрямного стовпця
        index = find_biggstM(summ)  # шукаємо найбільше по М
        if index == -1:
            return D, b, Cc, Cm, basis
        if len(index) > 1:  # якщо є 2 одн М, то шукаємо найбільше по числу
            ind_col = find_biggstC(index, sumc)
            if (ind_col == -1):
                return D, b, Cc, Cm, basis
        elif len(index) == 1:
            ind_col = index[0]

        # знайти індекс напрямного рядка
        ind_row = find_ind_row(b, D, ind_col)

        print("\nIндекс напрямного рядка: ", ind_row)
        print("Iндекс напрямного стовпця: ", ind_col)
        print("Напрямний елмент: ", D[ind_row][ind_col])

    print("\nЗавелика кількість ітерацій.")
    return D, b, Cc, Cm, basis


def showRes(Fc, basis, b):
    print()
    xxx = [0] * len(Fc)
    for i in range(len(basis)):
        xxx[basis[i]] = round(b[i], 2)
    for i in range(len(xxx)):
        print("X{} = {}".format(i + 1, xxx[i]))

    print("\nЗначення цільової функції: \nZ=", end=" ")
    p = 0.0
    for i in range(len(b)):
        print("+", end="")
        p += Fc[i] * xxx[i]
        print(" {:,.3f} * {:,.3f} ".format(Fc[i], xxx[i]), end="")
    print("=", round(p, 3))
    return xxx



def init(funcPoint):
    F, A, b = read_matrix()
    signs = [-1, -1]  # -1 is <=       0 is =      1 is >=

    Fc = funcPoint  # stala
    Fm = []  # stala
    for i in range(len(Fc)):
        Fm.append(0)
    basis = []  # basis
    for i in range(len(signs)):
        if signs[i] == -1:  # add 1 vector
            addVector(Fm, Fc, A, 1, i, basis)
        elif signs[i] == 1:  # add -1 vector + M*1 vector
            addVector(Fm, Fc, A, -1, i, basis)

            # C i b
    Cc = []
    Cm = []
    for i in range(len(A)):
        Cc.append(Fc[basis[i]])
        Cm.append(Fm[basis[i]])
    bsumc = 0
    for i in range(len(Cc)):
        bsumc += (Cc[i] * b[i])
    bsumm = 0
    for i in range(len(Cm)):
        bsumm += (Cm[i] * b[i])

    D = copy.deepcopy(A)  # Симплекс таблиця
    sumc = []  # sum chisla
    for col in range(len(D[0])):
        sum = 0
        for row in range(len(D)):
            sum += (Cc[row] * D[row][col])
        sum -= Fc[col]
        sumc.append(sum)
    summ = []  # sum M
    for col in range(len(D[0])):
        sum = 0
        for row in range(len(D)):
            sum += Cm[row] * D[row][col]
        sum -= Fm[col]
        summ.append(sum)

    print("\nМатриця коефіцієнтів: ")
    print('\n'.join(['\t'.join(['{:3}'.format(round(item, 2)) for item in row]) for row in D]))

    # знайти індекс напрямного стовпця
    index = find_biggstM(summ)  # шукаємо найбільше по М

    if index == -1:
        return showRes(Fc, basis, b)

    if len(index) > 1:  # якщо є 2 одн М, то шукаємо найбільше по числу
        ind_col = find_biggstC(index, sumc)
        if ind_col == -1:
            return showRes(Fc, basis, b)

    elif len(index) == 1:
        ind_col = index[0]
        # знайти індекс напрямного рядка
    ind_row = find_ind_row(b, D, ind_col)

    # print("\nIндекс напрямного рядка: ", ind_row)
    # print("Iндекс напрямного стовпця: ", ind_col)
    # print("Напрямний елмент: ", D[ind_row][ind_col])

    D, b, Cc, Cm, basis = symplex_method(D, b, Cc, Cm, Fc, Fm, ind_row, ind_col, basis, sumc, summ)
    return showRes(Fc, basis, b)





