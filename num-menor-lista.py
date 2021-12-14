nums = [8, 6, 3, 9, 23, 54, 2, 65]

def find_min(nums):
    min_num = float("inf")

    for num in nums:
        if num < min_num:
            min_num = num
    return min_num
        
print (find_min(nums))