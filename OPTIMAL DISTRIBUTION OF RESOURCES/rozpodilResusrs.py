from copy import deepcopy


def read_matrix():
    f = open("matrix", "r")
    mat = []
    Func = []  # Наявний парк автомобілів
    Function = f.readline()
    for num in Function.split():
        Func.append(int(num))
    for line in f.readlines():
        mat.append([float(x) for x in line.split()])

    f.close()
    return Func, mat


globalMaxProf = []
globalCarNeed = []


def condOpt(E, a, maxProf, carNeed):
    for pidpriemstvo in range(len(a[0]) - 2, -1, -1):
        maxProfNxt = [-1] * len(E)
        maxProfNxt[0] = 0
        carNeedNxt = [-1] * len(E)
        carNeedNxt[0] = 0
        print("All cars     Selected    Rest    Total profit")
        for i in range(len(E)):
            rest = []
            restProf = []

            prof = []
            fullProf = []

            hereCars = []
            for j in range(len(E)):
                if E[i] != 0 and j <= i:
                    if E[j] == 0:
                        prof.append(0)
                    else:
                        prof.append(a[j - 1][pidpriemstvo])
                    hereCars.append(E[j])
                    rest.append(E[i] - E[j])
                    restProf.append(maxProf[E.index(rest[j])])
                    fullProf.append(prof[j] + restProf[j])
                    print("{}           {}            {}            {:,.2f}".format(E[i], E[j], rest[j], fullProf[j]))
            print()

            if E[i] != 0:
                maxProfNxt[i] = max(fullProf)
                carNeedNxt[i] = hereCars[fullProf.index(max(fullProf))]
        print()

        maxProf = deepcopy(maxProfNxt)
        carNeed = deepcopy(carNeedNxt)
        globalMaxProf.append(maxProf)
        globalCarNeed.append(carNeed)


E, a = read_matrix()

maxProf = [-1] * len(E)
maxProf[0] = 0
carNeed = [-1] * len(E)
carNeed[0] = 0
pidpriemstvo = 3
print("All cars     Selected    Rest    Total profit")
for i in range(len(E)):
    prof = []
    fullProf = []
    hereCars = []
    for j in range(len(E)):
        if E[i] != 0 and j <= i:
            if E[j] == 0:
                prof.append(0)
            else:
                prof.append(a[j - 1][pidpriemstvo])
            hereCars.append(E[j])
            fullProf = prof  # only for first table
            print("{}           {}            {}            {}".format(E[i], E[j], E[i] - E[j], fullProf[j]))
    print()
    if E[i] != 0:
        maxProf[i] = max(fullProf)
        carNeed[i] = hereCars[fullProf.index(max(fullProf))]

globalMaxProf.append(maxProf)
globalCarNeed.append(carNeed)

condOpt(E, a, maxProf, carNeed)

totalCars = E[-1]
carsUsed = [-1] * len(a[0])

indexOfMxProf = globalMaxProf[-1].index(max(globalMaxProf[-1]))
maxMoney = globalMaxProf[-1][indexOfMxProf]
carsUsed[-1] = globalCarNeed[-1][indexOfMxProf]
totalCars -= carsUsed[-1]

for i in range(len(globalMaxProf) - 2, -1, -1):
    carsUsed[i] = globalCarNeed[i][E.index(totalCars)]
    totalCars -= carsUsed[i]

totalIncome = 0
for i in range(len(a[0]) - 1, -1, -1):
    print("Для підприємства ", (len(a[0]) - i), " потрібно виділити ", carsUsed[i], " машин з прибутком ", end="")
    if carsUsed[i] != 0:
        totalIncome += a[E.index(carsUsed[i]) - 1][len(a[0]) - i - 1]
        print(a[E.index(carsUsed[i]) - 1][len(a[0]) - i - 1])
    else:
        print(0)

print("Максимальний прибуток ", totalIncome)
