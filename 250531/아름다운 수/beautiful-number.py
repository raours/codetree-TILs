n = int(input())

answer = []
result = 0
# Please write your code here.
def choose(cur):
    global result
    if cur == n+1:
        result += 1
        return
    elif cur>n+1:
        return

    for i in range(1,5):
        for j in range(i):
            answer.append(i)
        choose(cur+i)
        for j in range(i):
            answer.pop()

choose(1)
print(result)