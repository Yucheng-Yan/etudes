left = []
right = []

with open('input.txt', 'r') as file:
    for line in file:
        curr = line.split()
        left.append(curr[0])
        right.append(curr[1])

left.sort()
right.sort()
ans = 0
i = 0
while i < len(left):
    ans += abs(int(left[i]) - int(right[i]))
    i += 1
print(ans)
