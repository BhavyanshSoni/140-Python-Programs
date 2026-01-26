import re
from math import sqrt
from fractions import Fraction

class Class9MathSolver:
    def __init__(self):
        pass

    def solve_expression(self, expr: str):
        """
        Safely evaluate arithmetic expressions: +, -, *, /, **, fractions
        """
        try:
            expr = expr.replace('^', '**')
            # handle fractions
            expr = re.sub(r'(\d+)\s*/\s*(\d+)', r'Fraction(\1,\2)', expr)
            allowed = {
                'Fraction': Fraction,
                'sqrt': sqrt,
                'abs': abs,
                'round': round,
                '__builtins__': {}
            }
            result = eval(expr, allowed)
            return result
        except Exception as e:
            return f"Error: {e}"

    def solve_linear(self, equation: str):
        """
        Solve ax + b = c for x
        """
        try:
            eq = equation.replace(' ', '')
            left, right = eq.split('=')
            m = re.match(r'([+-]?\d*)x([+-]\d+)?', left)
            if not m:
                return "Unsupported format"
            a = m.group(1)
            b = m.group(2) or '0'
            a = int(a) if a not in ['', '+', '-'] else (1 if a in ['', '+'] else -1)
            b = int(b)
            c = int(right)
            x = Fraction(c - b, a)
            return f"x = {x}"
        except Exception as e:
            return f"Error: {e}"

    def solve_quadratic(self, equation: str):
        """
        Solve ax^2 + bx + c = 0, return roots
        """
        try:
            eq = equation.replace(' ', '').replace('^2', '**2')
            # extract a,b,c
            match = re.match(r'([+-]?\d*)x\*\*2([+-]\d*)x([+-]\d+)=0', eq)
            if not match:
                # fallback generic parse using regex
                coeffs = re.findall(r'([+-]?\d*)x\*\*2|([+-]?\d*)x|([+-]?\d+)', eq)
                # manual fallback not implemented
                return "Quadratic parsing error"
            a_str, b_str, c_str = match.group(1), match.group(2), match.group(3)
            a = int(a_str) if a_str not in ['', '+', '-'] else (1 if a_str in ['', '+'] else -1)
            b = int(b_str)
            c = int(c_str)
            d = b*b - 4*a*c
            if d < 0:
                return "No real roots"
            root1 = Fraction(-b + sqrt(d), 2*a)
            root2 = Fraction(-b - sqrt(d), 2*a)
            return f"Roots: {root1}, {root2}"
        except Exception as e:
            return f"Error: {e}"

if __name__ == '__main__':
    solver = Class9MathSolver()
    print("Class9 Math Solver")
    while True:
        print("\nChoose option:")
        print("1. Evaluate expression")
        print("2. Solve linear equation (ax + b = c)")
        print("3. Solve quadratic equation (ax^2 + bx + c = 0)")
        print("4. Exit")
        choice = input("Option: ")
        if choice == '1':
            expr = input("Enter expression: ")
            print("Result:", solver.solve_expression(expr))
        elif choice == '2':
            eq = input("Enter linear equation: ")
            print(solver.solve_linear(eq))
        elif choice == '3':
            eq = input("Enter quadratic equation: ")
            print(solver.solve_quadratic(eq))
        elif choice == '4':
            break
        else:
            print("Invalid option")
