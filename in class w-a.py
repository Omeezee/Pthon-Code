n1= int(input("what is the integer value for n1 "))
n2= int(input("what is the integer value for n2 (must be greater or less than n1) "))
#n1= int(n1)
#n2= int(n2)
x = list(range(n1,n2))
print(x)

if n1 > n2:
    print('because n1 is > than n2 we can not continue computing')
else:
    for n in x:
        if n1%3 == 0:
            print ('could not compute not a multiple of 3 for n1')

    if n2%3 == 0:
        print ('could not compute not a multiple of 3 for n2')
            
    else:
            s= sum(x)
            print(f"The sum of the integers from n1 to n2 is {s}")
            

    
