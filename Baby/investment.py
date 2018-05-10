#!/usr/bin/env python3
amount = float(input("Enter amout:"))  #输入数额
inrate = float(input("Enter interest rate"))
period = int(input("Enter period"))
value = 0
year = 1
while year <= period:
    value = amount + (inrate * amount)
    print("Year {} Rs. {:.2f}".format(year,value))
    amount = value
    year = year+1

