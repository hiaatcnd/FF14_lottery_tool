import json
from generate import get_id, cal_max_expectation
import os
from IPython import embed

if __name__ == "__main__":
    if not os.path.exists("data.json"):
        print("Please run generate.py first!!!")
        exit(0)

    with open("data.json", "r") as f:
        dp = json.load(f)


    statu = [[0 for j in range(3)] for i in range(3)]
    steps = int(input("Please enter the number of numbers you have opened: "))
    if steps > 0:
        print("Enter the numbers that have opend one by one in this format:")
        print("3 1 9 means that the number in column 1 of row 3 is 9.")
    for i in range(steps):
        x, y, num = map(int, input("Number {}: ".format(i + 1)).split())
        statu[x - 1][y - 1] = num
    
    while(steps < 3):
        statu_id = str(get_id(statu))
        print(statu_id)
        assert(statu_id in dp)
        exp, x, y = dp[statu_id]
        print("Choose ({}, {}), the expectation of coins is: {:.2f}".format(x + 1, y + 1, exp))
        num = int(input("The number you see is: "))
        statu[x][y] = num
        print(statu)
        steps += 1

    cal_max_expectation(statu, output_flag = True)
