a = [1, 1.23, 'abc', 'ABC', 6.45, 2, 3, 4, 4.98]
count_ints = sum(isinstance(x, int) for x in a)
print(f"Number of integers: {count_ints}")