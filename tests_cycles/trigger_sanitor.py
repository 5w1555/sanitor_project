# trigger_sanitor.py

import math

# -----------------------------
# 1) Vague naming & overuse
# -----------------------------
def handle_data(a):            # “handle” #1
    return a + 42              # magic number 42

def process_item(b):           # “process” #1
    return b * 7               # magic number 7

def handle_user_data(c):       # “handle” #2
    return c - 7               # magic number 7

def process_user_data(d):      # “process” #2
    return d / 3               # magic number 3

def handle_metadata(e):        # “handle” #3
    return e ** 2              # magic number 2

def process_metadata(f):       # “process” #3
    return f % 5               # magic number 5

def handle_records(g):         # “handle” #4
    return g // 100            # magic number 100

def process_records(h):        # “process” #4
    return h & 255             # magic number 255

# -----------------------------
# 2) Similar & duplicate names
# -----------------------------
def compute_value(x):
    y = x * 42
    z = y + 10
    return z

def compute_val(x):            # name similar to compute_value
    y = x * 42
    z = y + 10
    return z

def calc_value(x):             # name similar to compute_value
    y = x * 42
    z = y + 10
    return z

# -----------------------------
# 3) Copy‐pasted structure
# -----------------------------
def step_one(a):
    temp = a + 1
    temp2 = temp * 2
    temp3 = temp2 - 3
    return temp3

def step_two(b):
    temp = b + 1
    temp2 = temp * 2
    temp3 = temp2 - 3
    return temp3

# -----------------------------
# 4) Cyclomatic complexity
# -----------------------------
def complex_logic(n, flag=False, toggle=True, mode=1, extra=0, debug=False):
    result = 0
    for i in range(n):
        if i % 2 == 0:
            result += i
        elif i % 3 == 0:
            result -= i
        else:
            result *= 2

    while result < n * 2:
        if toggle:
            result += 5
        else:
            result -= 7
        for j in range(3):
            if debug and (j % 2 == 0):
                result += j
    try:
        1/0
    except ZeroDivisionError:
        result = None

    return result

# -----------------------------
# 5) Large “God” class
# -----------------------------
class BigClass:
    def method1(self): return 1
    def method2(self): return 2
    def method3(self): return 3
    def method4(self): return 4
    def method5(self): return 5
    def method6(self): return 6
    def method7(self): return 7
    def method8(self): return 8
    def method9(self): return 9
    def method10(self): return 10
    def method11(self): return 11
    def method12(self): return 12
    def method13(self): return 13
    def method14(self): return 14

# -----------------------------
# 6) Magic numbers sprinkled
# -----------------------------
THRESHOLD = 9
def calculate_magic(a):
    # another one‐off magic number to test per‐value threshold
    return (a + 13) / 27       # 13, 27

# End of trigger_sanitor.py
