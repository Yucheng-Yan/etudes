import time
import concurrent.futures
import os
import math

def is_prime(n):
    """Check if a number is a prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True  
    if n % 2 == 0 or n % 3 == 0:
        return False
    # Only need to check up to sqrt(n)
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w  # Alternate between adding 2 and 4
    return True

def sieve_segment(low, high):
    """Segmented Sieve of Eratosthenes to find primes in a given range."""
    # Adopted from https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
    limit = int(math.sqrt(high)) + 1
    primes = []
    is_prime_small = [True] * limit
    for i in range(2, limit):
        if is_prime_small[i]:
            for j in range(i * i, limit, i):
                is_prime_small[j] = False
            primes.append(i)

    is_prime_segment = [True] * (high - low)
    for prime in primes:
        # Find the minimum number in [low, high) that is a multiple of prime
        start = max(prime * prime, ((low + prime - 1) // prime) * prime)
        for j in range(start, high, prime):
            is_prime_segment[j - low] = False

    segment_primes = [low + i for i, val in enumerate(is_prime_segment) if val and (low + i) >= 2]
    return segment_primes

def long_computation():
    """Find the first 100,000 prime numbers."""
    total_primes_needed = 100000
    # Get the number of CPU cores to optimize the computation
    num_cores = os.cpu_count()
    # Estimate the upper bound for the nth prime number using the Prime Number Theorem
    n = total_primes_needed
    if n >= 6:
        upper_bound = int(n * (math.log(n) + math.log(math.log(n))))
    else:
        upper_bound = 541  # The 100th prime number

    # Divide the range [2, upper_bound) into num_cores segments
    segment_size = (upper_bound - 2) // num_cores + 1
    ranges = []
    for i in range(num_cores):
        low = 2 + i * segment_size
        high = min(low + segment_size, upper_bound)
        ranges.append((low, high))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(sieve_segment, low, high) for low, high in ranges]
        primes = []
        for future in concurrent.futures.as_completed(futures):
            primes.extend(future.result())

    primes = sorted(primes)[:total_primes_needed]
    print(f"Found {len(primes)} prime numbers.")
    return primes

if __name__ == "__main__":
    start_time = time.time()
    long_computation()
    print(f"Execution time: {time.time() - start_time:.2f} seconds")



