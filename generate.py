import copy
import itertools

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


def cal_max_expectation(statu):
    remain_nums = get_remain_nums(statu)
    permu_it = itertools.permutations(remain_nums)
    while True:
        try:
            permutation = next(permu_it)
        except StopIteration:
            break

        


def search_next_step(statu, steps):
    statu_id = get_id(statu)
    if statu_id in dp:
        return dp[statu_id]

    if steps >= 3:
        tmp = (cal_max_expectation, -1, -1)
        dp[statu_id] = tmp
        return tmp
    
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
                    expectation, _, __ = search_next_step(statu, steps + 1)
                    avg_expectation += expectation
                avg_expectation /= len(remain_nums)

                if avg_expectation > max_expectation:
                    max_expectation = avg_expectation
                    step_x = i
                    step_y = i

                statu[i][j] = 0

    tmp = (max_expectation, step_x, step_y)
    dp[statu_id] = tmp
    return tmp

if __name__ == '__main__':
    statu = [[0 for j in range(3)] for i in range(3)]
    search_next_step(statu)
