N = int(input())
n = N
while(n > 0):
    a,b = input().split(" ")
    if(b == a[len(a) - len(b):]):
        print("encaixa")
    else:
        print ("não encaixa")    
    n -= 1        
