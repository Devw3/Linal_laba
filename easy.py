# Easy Level
import time
from collections import deque
from typing import List, Tuple, Dict
from sympy import factorint
from sympy import totient as euler_phi

# Task1
def is_palindrome(n) -> bool:
    s = str(n)
    return s == s[::-1]


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


# проверка циклической простоты
def is_circular_prime(p: int) -> bool:
    s = str(p)
    n = len(s)
    for digit in s:
        if n > 1 and digit in '024568':
            return False

    cur = s
    for _ in range(n):
        rotated_num = int(cur)
        if not is_prime(rotated_num):
            return False
        cur = cur[1:] + cur[0]
    return True


def palindromic_squares_and_circular_primes() -> Tuple[List[int], List[int]]:
    palindromic_squares = []
    circular_primes = []
    # палиндромы квадратов
    for a in range(1, 100000):
        if is_palindrome(a):
            a_squared = a * a
            if is_palindrome(a_squared):
                palindromic_squares.append(a)

    # циклические простые числа
    for p in range(1, 1000000):
        if is_prime(p) and is_circular_prime(p):
            circular_primes.append(p)

    return palindromic_squares, circular_primes


# print(palindromic_squares_and_circular_primes())

# Task2
def palindromic_cubes_and_palindromic_primes() -> Tuple[List[int], List[int]]:
    palindromic_cubes_list = []
    palindromic_primes_list = []
    # палиндромы кубов
    for a in range(1, 100000):
        if is_palindrome(a):
            a_cubed = a * a * a
            if is_palindrome(a_cubed):
                palindromic_cubes_list.append(a)

    # палиндромические простые числа
    for p in range(1, 10001):
        if is_palindrome(p) and is_prime(p):
            palindromic_primes_list.append(p)

    return palindromic_cubes_list, palindromic_primes_list


# print(palindromic_cubes_and_palindromic_primes())

# Task3
def generate_primes_from_digits(allowed_digits: str, count: int) -> List[int]:
    found_primes: List[int] = []
    # составляем очередь для генерации чисел из разрешённых цифр
    queue = deque(d for d in allowed_digits if d != '0')

    while queue and len(found_primes) < count:
        current_str = queue.popleft()
        current = int(current_str)

        if is_prime(current):
            found_primes.append(current)

        # генерация новых чисел и добавление в очередь на проверку
        if len(current_str) < 20:
            for digit in allowed_digits:
                queue.append(current_str + digit)

    return found_primes


def primes_with_two_digits() -> Dict[str, List[int]]:
    count_to_find = 100
    sets_to_check = {
        '13': '13',
        '15': '15',
        '17': '17',
        '19': '19'
    }
    res = {}
    for key, allowed_digits in sets_to_check.items():
        res[key] = generate_primes_from_digits(allowed_digits, count_to_find)

    return res


# print(primes_with_two_digits())

# Task4
def count_primes_up_to(n: int) -> int:
    count = 0
    for i in range(2, n + 1):
        if is_prime(i):
            count += 1
    return count


def twin_primes_analysis(limit_pairs: int = 1000) -> Tuple[List[Tuple[int, int]], List[float]]:
    twin_pairs: List[Tuple[int, int]] = []
    ratios: List[float] = []
    n = 3
    while len(twin_pairs) < limit_pairs:
        if is_prime(n) and is_prime(n + 2):
            twin_pairs.append((n, n + 2))
            n_max = n + 2

            pi_2_n = len(twin_pairs)
            pi_n = count_primes_up_to(n_max)

            if pi_n > 0:
                ratio = pi_2_n / pi_n
                ratios.append(ratio)
            else:
                ratios.append(0.0)
        n += 2

    return twin_pairs, ratios


# print(twin_primes_analysis())
# по мере роста n отношения простых чисел близнецов к общему числу простых чисел pi_2(n)/pi(n) уменьшается и стремится к нулю

# Task5
def factorial(n: int) -> int:
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res


def prime_factorial(n: int) -> Dict[int, int]:
    return factorint(n)


def factorial_plus_one_factors() -> Dict[int, Dict[int, int]]:
    all_factorizations: Dict[int, Dict[int, int]] = {}
    max_distinct_factors = 0
    n_with_max_factors = 0
    big_prime_cases: List[Tuple[int, int]] = []
    big_number = 10 ** 6

    for n in range(2, 51):
        num = factorial(n) + 1
        factors = prime_factorial(num)
        all_factorizations[n] = factors

        # макс кол простых делителей среди всех n
        if len(factors) > max_distinct_factors:
            max_distinct_factors = len(factors)
            n_with_max_factors = n

        # добавление больших простых делителей
        for p in factors:
            if p > big_number:
                big_prime_cases.append((n, p))

    print(f"максимальное количество различных простых делителей при n = {n_with_max_factors}: {max_distinct_factors}")
    if big_prime_cases:
        print("большие простые делители:")
        for n, p in big_prime_cases:
            print(f"n: {n}, простой делитель: {p}")

    return all_factorizations


# print(factorial_plus_one_factors())

# Task6
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def euler_phi_direct(n: int) -> int:
    if n <= 0:
        return 0
    count = 0
    for k in range(1, n + 1):
        if gcd(n, k) == 1:
            count += 1
    return count


def euler_phi_factor(n: int) -> int:
    if n <= 0:
        return 0

    factors = prime_factorial(n)
    res = n
    for p in factors.keys():
        res = res // p * (p - 1)

    return res


def compare_euler_phi_methods(test_values: List[int]) -> dict:
    times = {
        'direct': [],
        'factor': [],
        'sympy': []
    }

    for n in test_values:
        start = time.time()
        euler_phi_direct(n)
        end = time.time()
        times['direct'].append(end - start)

        start = time.time()
        euler_phi_factor(n)
        end = time.time()
        times['factor'].append(end - start)

        start = time.time()
        euler_phi(n)
        end = time.time()
        times['sympy'].append(end - start)

        print(times['direct'][-1], times['factor'][-1], times['sympy'][-1])

    return times


test = [
    10 ** 5,
    10 ** 6,
    10 ** 7
]

# print(compare_euler_phi_methods(test))

# 0.06747198104858398 0.0 0.0
# 0.7716782093048096 0.0 0.0005960464477539062
# 9.456411838531494 0.0 0.0
# 113.88878202438354 0.0 0.0010001659393310547
