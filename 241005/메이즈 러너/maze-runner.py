'''
삼성 코테 기출 문제
메이즈러너
'''

#입력 받기
N,M,K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
for _ in range(M):
    i, j = map(int, input().split())
    arr[i-1][j-1] -= 1 # 사람 표현

ei, ej = map(lambda x:int(x)-1, input().split())
arr[ei][ej] = -11 #비상구 -11
ans = 0
cnt =M

def find_square(arr):
    # [1] 최소 길이 mn를 구해준다.
    mn = N
    for i in range(N):
        for j in range(N):
            if -11<arr[i][j]<0:
                mn = min(mn, max(abs(ei-i),abs(ej-j)))
    # [2] (0,0)부터 men 정사각형 안에 탈출구,사람 있는 것 찾기
    for si in range(N-mn):
        for sj in range(N-mn):
            if si<=ei<=si+mn and sj<=ej<=sj+mn: #탈출구가 있고
                for i in range(si, si+mn+1):
                    for j in range(sj, sj+mn+1):
                        if -11<arr[i][j]<0:
                            return si,sj,mn+1

def find_exit(arr):
    for i in range(N):
        for j in range(N):
            if arr[i][j] ==-11:
                return i, j

for _ in range(K):
    narr = [x[:] for x in arr] #배열 복사
    for i in range(N):
        for j in range(N):
            if -11<arr[i][j]<0: #사람이면
                dis = abs(ei-i)+ abs(ej-j) #원래 자리와 비상구 거리
                for di, dj in ((-1,0), (1,0), (0,-1),(0,1)):
                    ni, nj = i+di, j+dj
                    if 0<=ni<N and 0<=nj<N and arr[ni][nj]<=0 and dis > (abs(ei-ni)+ abs(ej-nj)):
                        ans += arr[i][j] #이동거리 업데이트
                        narr[i][j] -=arr[i][j] #현재자리에서 제거

                        if arr[ni][nj] == -11: #비상구이면
                            cnt +=arr[i][j] #탈출!
                        else: #빈칸 or 다른 사람있는 자리
                            narr[ni][nj] += arr[i][j]  # 위치 이동
                        break

    arr = narr
    if cnt ==0:
        break

    si, sj, L = find_square(arr) #최소 정사각형 시작점과 한변 길이
    #그걸 이용해서 오른쪽으로 90도 회전

    narr = [x[:] for x in arr] #회전한 결과를 저장할 리스트
    for i in range(L):
        for j in range(L):
            narr[si+i][sj+j] = arr[si+L-1-j][sj+i]
            if narr[si+i][sj+j] >0 :
                narr[si + i][sj + j] -=1 #내구성 감소

    arr = narr
    ei,ej = find_exit(arr)

print(-ans)
print(ei+1, ej+1)