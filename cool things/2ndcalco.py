def add(x, y):
    return x + y
def subtract(x, y):
    return x - y
def multiply(x, y):
    return x * y
def divide(x, y):
    return x / y


num1 = float(input(" enter first number:   "))
num2 = float(input(" enter second number:   "))
op = input(" enter operation (+, -, *, /):   ")

if op == '+':
    print(float(add(num1, num2)))
elif op == '-':
    print(subtract(num1, num2))
elif op == '*':
    print(multiply(num1, num2))
elif op == '/':
    print(divide(num1, num2))
else:
    print("Invalid operation 👍")