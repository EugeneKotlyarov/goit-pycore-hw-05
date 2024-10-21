import time as t

# function CACHING_FIBONACCI creates local dictionary for cache results and return
# modified recursive FIBONACCI function which in addition returns saved cached results (if any)


def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


# test, please change N_CONST for testing, any result will be cropped to less than 20 symbols
# and calculation time printed in nanoseconds
def main():

    N_CONST = 6

    fib = caching_fibonacci()
    start = t.time() * 1000000
    res1 = fib(N_CONST)
    end = t.time() * 1000000
    print(
        f"result fibonacci for n = {N_CONST} is {str(res1)[:20]}..., done in: {end - start} ns"
    )


if __name__ == "__main__":
    main()
