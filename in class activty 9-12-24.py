n=int(input('enter a number for n'))

if int(n)>0:
    print('n is positive')
    x = n**.5
    print(x)

else:
    m= abs(n)
    print(m)
    b=m%2
if int(b)==0:
    print('m is even')
    print(m/2)
else:
    print('m is odd')
    c = m**3
    print(c)
