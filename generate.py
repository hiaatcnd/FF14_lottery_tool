#!/usr/bin python3

import copy
import itertools
import json
# from IPython import embed

lines = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)),
         ((2, 0), (2, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
         ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
         ((0, 0), (1, 1), (2, 2)), ((2, 0), (1, 1), (0, 2)))

coins = (
    0,
    0,
    0,
    0,
    0,
    0,  # 0-5: 0
    10000,
    36,
    720,
    360,
    80,
    252,
    108,
    72,
    54,
    180,
    72,
    180,
    119,
    36,
    306,
    1080,
    144,
    1800,
    3600)


def get_id(statu):
    the_id = 0
    for i in range(3):
        for j in range(3):
            the_id = the_id * 10 + statu[i][j]
    return the_id


def get_remain_nums(statu):
    used = [False for i in range(9)]
    for i in range(3):
        for j in range(3):
            if statu[i][j] > 0:
                used[statu[i][j] - 1] = True

    remain_nums = []
    for num in range(9):
        if not used[num]:
            remain_nums.append(num + 1)

    return tuple(remain_nums)


def cal_max_expectation(statu, output_flag=False):
    remain_nums = get_remain_nums(statu)

    max_exp = -1
    choose_line = ()
    for line in lines:
        cnt_blank = 0
        nums = []
        for x, y in line:
            nums.append(statu[x][y])
            if statu[x][y] == 0:
                cnt_blank += 1

        if cnt_blank == 0:
            exp = coins[sum(nums)]
            max_posiable = exp
            min_posiable = exp
        else:
            permu_it = itertools.permutations(remain_nums, cnt_blank)
            cnt_permu = 0
            max_posiable = -1
            min_posiable = 23333
            tot_coins = 0
            while True:
                try:
                    permutation = next(permu_it)
                except StopIteration:
                    break

                cnt_permu += 1

                permu_idx = 0
                cnt_points = 0
                for num in nums:
                    if num == 0:
                        cnt_points += permutation[permu_idx]
                        permu_idx += 1
                    else:
                        cnt_points += num
                max_posiable = max(max_posiable, coins[cnt_points])
                min_posiable = min(min_posiable, coins[cnt_points])
                tot_coins += coins[cnt_points]
            exp = tot_coins / cnt_permu

        if exp > max_exp:
            max_exp = exp
            choose_line = line

        if output_flag:
            line_real = [(x + 1, y + 1) for x, y in line]
            print(
                "line {} expectation: {:.2f}, max possible: {}, min possible: {}"
                .format(str(line_real), exp, max_posiable, min_posiable))

    if output_flag:
        line_real = [(x + 1, y + 1) for x, y in choose_line]
        print("Choose: " + str(line_real))
        print("expectation of coins: %.2f" % max_exp)

    return max_exp, choose_line


dp = {}


def search_next_step(statu, steps):
    statu_id = get_id(statu)
    if statu_id in dp:
        return dp[statu_id][0]

    if steps >= 4:
        tmp = cal_max_expectation(statu)
        dp[statu_id] = tmp
        return tmp[0]

    remain_nums = get_remain_nums(statu)
    max_expectation = -1
    step_x = -1
    step_y = -1

    for i in range(3):
        for j in range(3):
            if statu[i][j] == 0:
                avg_expectation = 0
                for num in remain_nums:
                    statu[i][j] = num
                    expectation = search_next_step(statu, steps + 1)
                    avg_expectation += expectation
                avg_expectation /= len(remain_nums)

                if avg_expectation > max_expectation:
                    max_expectation = avg_expectation
                    step_x = i
                    step_y = j

                statu[i][j] = 0

    dp[statu_id] = (max_expectation, step_x, step_y)
    return max_expectation


if __name__ == '__main__':
    statu = [[0 for j in range(3)] for i in range(3)]
    search_next_step(statu, 0)
    print("generate {} status".format(len(dp)))
    with open("data.json", "w") as f:
        json.dump(dp, f)
