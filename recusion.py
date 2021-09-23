def sum(n):
    total = 0
    for index in range(n+1):
        total += index
    return total
result = sum(100)
print(result)