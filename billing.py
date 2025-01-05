def calculate_bill(unit):
    price = 0

    if(unit <= 20):
        price = unit * 4

    elif(unit > 20 and unit <= 50):
        price = 20*4 +(unit - 20)*7.30

    elif(unit > 50 and unit <= 150):
        price =  20*4 +30*7.30+(unit-50)*8.60

    elif (unit > 150 ):
        price = 20*4 + 30*7.30 +100*8.60 +(unit - 150)*9.50

    else:
        print("Invalid input")

    return price
    
