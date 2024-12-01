from collections import defaultdict
left = []
right = defaultdict(int)

with open('input.txt', 'r') as file:
    for line in file:
        curr = line.split()
        left.append(curr[0])
        right[int(curr[1])] += 1

ans = 0
for num in left:
    num = int(num)
    if num in right:
        ans += (num * right[num])
        del right[num]
print(ans)
