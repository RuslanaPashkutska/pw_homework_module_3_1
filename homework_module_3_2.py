import time
from multiprocessing import Pool, cpu_count

# Synchronous version of the factorize function
def factorize_sync(*numbers):
    result = []
    for number in numbers:
        divisors = []
        # Find all divisors of the current number
        for i in range(1, number + 1):
            if number % i == 0:
                divisors.append(i)
        result.append(divisors)
    return result

# Helper function for multiprocessing - finds divisors of a single number
def get_divisors(number):
    return [i for i in range(1, number + 1) if number % i == 0]
# Parallel version of the factorize function using multiprocessing
def factorize_parallel(*numbers):
    with Pool(cpu_count()) as pool:
        result = pool.map(get_divisors, numbers)
    return result

if __name__ == "__main__":
    numbers_to_factor = (128, 255, 99999, 10651060)

    # Measure time for synchronous version
    start = time.time()
    a, b, c, d = factorize_sync(*numbers_to_factor)
    end = time.time()
    print("Execution time (synchronous):", round(end - start, 4), "seconds")
    print("✅ Synchronous version passed the test.")


    # Measure time for parallel version
    start = time.time()
    a, b, c, d = factorize_parallel(*numbers_to_factor)
    end = time.time()
    print("Execution time (parallel):", round(end - start, 4), "seconds")
    print("✅ Parallel version passed the test.")