def juego(n, cnt):
    i = int(n**0.5)
    while 0 < i**2 :
        cnt += 1
        aux, cnt = juego(n-i**2, cnt)
        if not aux:
            return (True, cnt)
        i -= 1
    return (False, cnt)

def winnerSquareGame(n):
    losers = {0}
    for x in range(1,n+1):
        flag = True
        for y in range(1,int(x**0.5)+1):
            if (x - y**2) in losers:
                flag = False
                break
        if flag:
            losers.add(x)
    return False if n in losers else True


import timeit
start = timeit.default_timer()

x = 100000
# aux, cnt = juego(x,0)
aux2 = winnerSquareGame(x)
# print(x,cnt)
#Your statements here

stop = timeit.default_timer()
print('Time: ', stop - start)  