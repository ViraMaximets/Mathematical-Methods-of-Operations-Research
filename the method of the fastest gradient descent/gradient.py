from scipy import misc
from sympy import symbols, solve, Eq

eps = 0.000001

# Початкове наближення
x = 0
y = 0
z = 0


def func(x, y, z):
    return 7 * x * x + 4 * y * y + 6 * z * z - 3 * x * y + x * z - y * z + x - y + z


def partial_derivative(func, at, point):
    def wraps(x):
        point[at] = x
        return func(point[0], point[1], point[2])

    return misc.derivative(wraps, point[at], dx=0.0001)


X0 = func(x, y, z)
tmp_x0 = X0
B = symbols('b', real=True)
iters = 0
cond = eps + 1

while cond > eps:
    point = [x, y, z]

    # градієнт у точці * B
    x_t = x - B * partial_derivative(func, 0, point)
    y_t = y - B * partial_derivative(func, 1, point)
    z_t = z - B * partial_derivative(func, 2, point)

    point_t = [x_t, y_t, z_t]

    # похідна по В == 0
    b_t = min(solve(Eq(func(point_t[0], point_t[1], point_t[2]).diff(B), 0)))

    # градієнт у точці * `beta`
    x = x - b_t * partial_derivative(func, 0, point)
    y = y - b_t * partial_derivative(func, 1, point)
    z = z - b_t * partial_derivative(func, 2, point)

    X0 = func(x, y, z)
    cond = abs(tmp_x0 - X0)
    tmp_x0 = X0

    iters += 1
    print("\nBeta =", b_t)
    print("x{}({:,.3f}; {:,.3f}; {:,.3f})".format(iters, x, y, z))
    print("X0 =", X0)
