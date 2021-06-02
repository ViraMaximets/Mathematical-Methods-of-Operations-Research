from math import floor

masa = [1, 2, 3]
maxMasa = 9

mat = [[0, 30, 70, 90, 140, 180, 260, 370, 400, 450],
       [0, 210, 335, 440, 500, -1, -1, -1, -1, -1],
       [0, 300, 400, 600, -1, -1, -1, -1, -1, -1]]


def findOpt(x, r, maxMasa):
    if r == 3:
        return mat[2][x]
    if r == 2:
        if maxMasa - x * 2 - 1 < 0:
            z3 = 0
        else:
            z3 = masasFor3[maxMasa - x * 2 - 1][1]
        return mat[1][x] + z3
    if r == 1:
        if maxMasa - x - 1 < 0:
            z2 = 0
        else:
            z2 = masas2i3[maxMasa - x - 1][1]
        return mat[0][x] + z2


masasFor3 = []
masas2i3 = []
masas1i2i3 = []

# find max optimal for 3 vantaj
for s in range(1, maxMasa + 1):
    tZ3 = [[x, findOpt(x, 3, s)] for x in range(floor(s / masa[2]) + 1)]
    masasFor3.append(max(tZ3, key=lambda item: item[1]))

# find max optimal for 2 vantaj
for s in range(1, maxMasa + 1):
    tZ2 = [[x, findOpt(x, 2, s)] for x in range(floor(s / masa[1]) + 1)]
    masas2i3.append(max(tZ2, key=lambda item: item[1]))


# find max optimal for 1 vantaj
tZ1 = [[x, findOpt(x, 1, maxMasa)] for x in range(floor(maxMasa / masa[0]) + 1)]
masas1i2i3.append(max(tZ1, key=lambda item: item[1]))

print("Максимальний прибуток ", masas1i2i3[0][1], " млн грн при завантаженні:")

print("Вантаж №1 у кількості ", masas1i2i3[0][0], " одниць сумарною вагою ", masa[0] * masas1i2i3[0][0], "тонн")

maxMasa -= masa[0] * masas1i2i3[0][0]
print("Вантаж №2 у кількості ", masas2i3[maxMasa - 1][0], " одниць сумарною вагою ", masa[1] * masas2i3[maxMasa - 1][0],
      "тонн")

maxMasa -= masa[1] * masas2i3[maxMasa - 1][0]
print("Вантаж №3 у кількості ", masasFor3[maxMasa - 1][0], " одниць сумарною вагою ",
      masa[2] * masasFor3[maxMasa - 1][0], "тонн")
