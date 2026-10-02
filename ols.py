# ols(V1.3-Alpha)
import time
import random
import config
from data import save_history

r = random.randint

def CreateNumber(order, start, end, quantity):
    if order in ["+", "-", "*"]:
        return [r(start, end) for _ in range(quantity)]
    elif order == "-op":
        res = []
        for _ in range(quantity):
            b = r(start, end)
            res.append(b)
            res.append(b + r(start, end))
        return res
    else:
        res = []
        for _ in range(quantity):
            b = r(start, end)
            while b == 0:
                b = r(start, end)
            mul_val = r(start, end)
            res.append(b)
            res.append(b * mul_val)
        return res

def BasicOperationJudge(order, NumberA, NumberB):
    orders = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "-op": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b
    }
    return orders[order](NumberA, NumberB)

def CreateDecimalNumber(order, start, end, decimals=2):
    factor = 10 ** decimals
    if order == "/":
        b = r(1, end) / factor
        quotient = r(start, end)
        a = round(b * quotient, decimals)
    else:
        a = r(start * factor, end * factor) / factor
        b = r(start * factor, end * factor) / factor
    return a, b


def CreateMixedNumber(start, end, difficulty=1, include_div=False, allow_neg=False):
    import random
    ops = ["+", "-", "*"]
    if include_div:
        ops.append("/")

    while True:
        n1 = r(start, end)
        n2 = r(start, end)
        n3 = r(start, end)
        op1 = random.choice(ops)
        op2 = random.choice(ops)

        if op1 == "/" and n2 == 0:
            n2 = 1
        if op2 == "/" and n3 == 0:
            n3 = 1
        if op1 == "/":
            n1 = n1 * n2
        if op2 == "/":
            n3 = n3 * r(1, 5)

        if difficulty <= 2:
            if difficulty == 1:
                expr = f"{n1} {op1} {n2} {op2} {n3}"
            else:
                expr = f"({n1} {op1} {n2}) {op2} {n3}"
        else:
            n4 = r(start, end)
            op3 = random.choice(ops)
            if op3 == "/" and n4 == 0:
                n4 = 1
            expr = f"({n1} {op1} {n2}) {op2} {n3} {op3} {n4}"

        try:
            answer = eval(expr)
        except ZeroDivisionError:
            continue

        if not allow_neg and answer < 0:
            continue

        return expr, answer
