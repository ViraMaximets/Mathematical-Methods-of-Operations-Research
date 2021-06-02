import math

from scipy import misc
from sympy import symbols, solve, Eq
import lab9.condition_symplex as symplex

eps = 0.1

# Початкове наближення
x = 1
y = 1


def func(x, y):
    return x * x + 2 * y * y - 2 * x * y + 5 * x


def partial_derivative(func, at, point):
    def wraps(x):
        point[at] = x
        return func(point[0], point[1])

    return misc.derivative(wraps, point[at], dx=0.0001)


X0 = func(x, y)
tmp_x0 = X0
B = symbols('b', real=True)
iters = 0
cond = eps + 1

while cond > eps:
    point = [x, y]
    print("\nStarting point", point)
    x0 = partial_derivative(func, 0, point)
    y0 = partial_derivative(func, 1, point)

    tochka = [x0, y0]
    coordinates = symplex.init(tochka)  # y0

    h0_x = coordinates[0] - x
    h0_y = coordinates[1] - y

    # градієнт у точці * B
    x_t = x + B * h0_x
    y_t = y + B * h0_y

    point_t = [x_t, y_t]

    # похідна по В == 0
    b_t = min(solve(Eq(func(point_t[0], point_t[1]).diff(B), 0)))

    if b_t > 1:
        b_t = 1

    xx_nxt = x + b_t * h0_x
    xy_nxt = y + b_t * h0_y

    cond = math.sqrt((float(func(x, y)) - float(func(xx_nxt, xy_nxt))) ** 2)

    iters += 1
    print("\nBeta =", float(b_t))
    print("x{}({:,.3f}; {:,.3f})".format(iters, float(xx_nxt), float(xy_nxt)))
    print("findOpt(x{}) = {:,.3f}".format(iters, float(func(xx_nxt, xy_nxt))))

    x = float(xx_nxt)
    y = float(xy_nxt)
