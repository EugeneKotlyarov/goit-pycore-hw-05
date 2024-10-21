import re
from typing import Callable

# function GENERATOR_NUMBERS accepts text string with info where revenues
# entered accurately as float numbers, so regex pattern will be:
# 1 or more digits + dot symbol + exactly 2 digits (ex: 1234.56, 12.21 and so on)
# collects all the numbers to list and returns them one by one as float
# (by yield because its generator)
#
# function SUM_PROFIT accepts as arguments:
# text to analyze and generator to do it; starts generator and returns sum of all
# elements in list from generator


def generator_numbers(text: str):
    pattern = re.compile(r"\d+\.\d{2}")
    res_list = re.findall(pattern, text)
    for a in res_list:
        yield float(a)


def sum_profit(text: str, func: Callable) -> float:
    gen_num = func(text)
    return sum([*gen_num])


# test
def main():
    # 1 (sum = 1351.46)
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")

    # 2 (sum = 4703.05)
    text = "Загальний дохід працівника складається з декількох частин: 4234.50 як основний дохід, доповнений додатковими надходженнями 344.55 і 124.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")


if __name__ == "__main__":
    main()
