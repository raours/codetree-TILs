''' 
코드트리 삼성기출
루돌프의 반란 문제
'''
import sys

from collections import deque
#sys.stdin = open("input3.txt", "r")
input = sys.stdin.readline
'''
N: 게임판의 크기 (3≤N≤50)
M: 게임 턴 수 (1≤M≤1000)
P: 산타의 수 (1≤P≤30)
C: 루돌프의 힘 (1≤C≤N)
D: 산타의 힘 (1≤D≤N)
'''
N, M, P, C, D = map(int, input().split())
rx, ry = map(int, input().split())
#lst = [list(map(int, input().split())) for _ in range(N)]
board = [[0] * N for _ in range(N)]
santa = [] #산타들 좌표저장

POINT = 4
wake = [0] * (P+1) #1번인덱스부터 유효

#board판에 산타 놓기
for _ in range(P):
    num , x, y = map(int, input().split())
    board[x-1][y-1] = num
    santa.append([num, x-1, y-1, True, 0]) #산타 번호, 좌표, 움직가능여부, 점수

santa.sort() #산타 번호순 정렬

visited = [[False]*N for _ in range(N)]
#상우하좌 + 대각선
dx = [-1,0,1,0,-1,-1,1,1] 
dy = [0,1,0,-1,-1,1,-1,1]

di = [-1,0,1,0]
dj = [0,1,0,-1]

#좌하우상 +대각선
# dx = [0,1,0,-1,-1,-1,1,1] 
# dy = [-1,0,1,0,-1,1,-1,1]
rx -=1
ry -=1
board[rx][ry] = -1
#print(board)
def con_santa(cur, si, sj, index, mul):
    q = [(cur,si,sj,mul)]
    #print(q)
    while q:
        cur, ci, cj, mul = q.pop(0)
        ni, nj = ci + mul*dx[index], cj +mul*dy[index] #밀려날 좌표
        if 0<= ni <N and 0<= nj <N : #범위 내 
            #산타끼리 충돌x
            if board[ni][nj] == 0:
                board[ni][nj] = cur+1
                santa[cur][1],santa[cur][2] = ni, nj
                return
            else: #산타끼리 충돌
                q.append((board[ni][nj]-1, ni, nj, 1))
                board[ni][nj] = cur+1
                santa[cur][1],santa[cur][2] = ni, nj

        else: #범위 밖 -> 탈락
            santa[cur][3] = False
            return


def rmove(turn):
    global rx, ry
    #루돌프의 움직임 -> 
    #가장 가까운 산타 구하고
    temp = 10000000
    min_lst = []
    for i in range(P):
        if santa[i][3] == False:
            continue
        #산타마다 루돌프 좌표랑 계산해서 가장 거리가 작은 애를 구해
        temp2 = (rx - santa[i][1])**2 + (ry - santa[i][2])**2
        if temp2 <= temp:
            temp = temp2
            min_lst.append((temp, i, santa[i][1], santa[i][2])) # 최소 거리 리스트(거리, 산타 번호, x,y)
    min_lst.sort(key=lambda x: (x[0], -x[2], -x[3]))
    min_santa_x = min_lst[0][2]
    min_santa_y = min_lst[0][3]

    # 8방향 체크하며 가장 최소 방향 구하기
    tmp = 10000000
    for index in range(8):
        rnx = rx + dx[index]
        rny = ry + dy[index]
        if 0<= rnx <N and 0<= rny <N :
            tmp2 = (rnx - min_santa_x)**2 + (rny - min_santa_y)**2
            if tmp2<tmp:
                tmp = tmp2
                #그 전보다 거리가 적으면 그 좌표 저장
                x , y = rnx, rny
                rd = index #산타 날릴 방향
    
    board[rx][ry] = 0 #루돌프 움직
    
    rx = x
    ry = y
    #print(board)
    if 1<=board[x][y]<=30 :
        p_s = board[x][y]
        santa[p_s-1][POINT] += C
        wake[p_s] = turn + 2 #기절
        con_santa(p_s-1, x, y, rd, C)
        # nx, ny = x + C*dx[rd], y+C*dy[rd] #밀려날 좌표
    board[x][y] = -1
         
    return


def smove(turn):
    global rx, ry
    for i in range(P):
        if santa[i][3] == False:
            continue #탈락한 산타면 skip
        if wake[i+1] > turn:
            continue #기절한 산타 skip

        sx, sy, score = santa[i][1], santa[i][2], santa[i][4]
        # min_x = sx #현재자리로 초기화
        # min_y = sy #현재자리가 최소라면 움직이지 않기 위함
        min_d = (rx - sx)**2 + (ry - sy)**2 #원래거리
        tlst = []
        for index in range(4):
            snx = sx + dx[index]
            sny = sy + dy[index]  
            d = (rx - snx)**2 + (ry - sny)**2
            
            if 0<=snx<N and 0<=sny<N and board[snx][sny] <= 0 and min_d>d:
                min_d = d
                tlst.append((snx, sny, index))
        
        if len(tlst) == 0: continue #제자리

        snx, sny, index = tlst[-1] #마지막에 추가된 것이 제일 짧은 거리


        # 루돌프와 충돌시 처리
        if (rx, ry) == (snx, sny):
            santa[i][4] += D
            wake[i+1] = turn +2
            board[sx][sy] = 0
            index = (index+2)%4
            con_santa(i, snx, sny, index, D)
        else:
            board[sx][sy] = 0
            board[snx][sny] = i+1
            santa[i][1], santa[i][2] = snx, sny
    return
        


for turn in range(1, M+1):
    check = list(zip(*santa))[3]
    if check.count(True) == 0:
        break
    rmove(turn)
    smove(turn)

    #점수획득
    for i in range(P):
        if santa[i][3] == True:
            santa[i][4] +=1
        
for num in range(P):
    print(santa[num][4],end=' ')