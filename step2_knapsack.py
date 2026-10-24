# 第 6 次课 Step2：0-1 背包（至多装满变体：容量可以不花完）
# dp[i][c] 表示只考虑前 i 件、限重 c 时能获得的最大重要度

ITEMS = [
    ('帐篷', 300, 90),
    ('炉具', 200, 60),
    ('睡袋', 350, 115),
    ('食物', 400, 120),
    ('水具', 250, 80),
]
CAPACITY = 1000


def knapsack(items, capacity):
    """返回二维 dp 表，n+1 行，capacity+1 列"""
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w = items[i - 1][1]
        v = items[i - 1][2]
        for c in range(capacity + 1):
            # 不带第 i 件：直接继承正上方
            dp[i][c] = dp[i - 1][c]
            # 带第 i 件：容量扣减，重要度入账，取两者较大
            if c >= w and dp[i - 1][c - w] + v > dp[i][c]:
                dp[i][c] = dp[i - 1][c - w] + v
    return dp


def backtrack(dp, items, capacity):
    """从右下角回溯，取值发生变化的位置即为选中物品，返回 1 起编号"""
    chosen = []
    c = capacity
    for i in range(len(items), 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            chosen.append(i)
            c -= items[i - 1][1]
    chosen.reverse()
    return chosen


def summarize(items, chosen):
    weight = sum(items[i - 1][1] for i in chosen)
    value = sum(items[i - 1][2] for i in chosen)
    names = [items[i - 1][0] for i in chosen]
    return weight, value, names


def print_table(dp, items, capacity, step=100):
    """按每 100g 一档打印 dp 表，行是前 i 件"""
    cols = list(range(0, capacity + 1, step))
    print('dp 表（行：前 i 件；列：容量档位，每 100g 一档）')
    print('  i  ' + ''.join('%6d' % c for c in cols))
    for i in range(len(items) + 1):
        label = '  0 ' if i == 0 else '%3d ' % i
        print(label + ''.join('%6d' % dp[i][c] for c in cols))
    print('  物品编号：' + '，'.join('%d-%s' % (k + 1, it[0]) for k, it in enumerate(items)))


def solve_and_report(title, items, capacity):
    dp = knapsack(items, capacity)
    chosen = backtrack(dp, items, capacity)
    weight, value, names = summarize(items, chosen)
    print('===== %s =====' % title)
    print('容量：%dg，最优重要度：%d，组合编号：%s，物品：%s' % (capacity, value, chosen, names))
    print('实际重量：%dg（剩余 %dg）' % (weight, capacity - weight))
    return dp, chosen, value


def knapsack_must_include(items, capacity, must_no):
    """强制选中编号为 must_no 的物品，其余物品按 0-1 背包求解"""
    must_w = items[must_no - 1][1]
    must_v = items[must_no - 1][2]
    if must_w > capacity:
        return None, [], -1
    rest_items = [it for k, it in enumerate(items, 1) if k != must_no]
    rest_nos = [k for k in range(1, len(items) + 1) if k != must_no]
    rest_cap = capacity - must_w
    dp = knapsack(rest_items, rest_cap)
    rest_chosen = backtrack(dp, rest_items, rest_cap)
    chosen = sorted([must_no] + [rest_nos[k - 1] for k in rest_chosen])
    weight, value, names = summarize(items, chosen)
    return chosen, names, value


def main():
    print('变体说明：本程序采用“至多装满”，即容量可以不花完。')
    print()

    dp, chosen, value = solve_and_report('检查点：容量 1000g', ITEMS, CAPACITY)
    print()
    print_table(dp, ITEMS, CAPACITY)
    print()

    print('回溯路径（从 dp[5][1000] 往左上走）：')
    c = CAPACITY
    for i in range(len(ITEMS), 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            print('  (%d, %d) → 选中 %d-%s，剩余容量 %d' % (i, c, i, ITEMS[i - 1][0], c - ITEMS[i - 1][1]))
            c -= ITEMS[i - 1][1]
        else:
            print('  (%d, %d) → 不选 %d-%s，继承正上方' % (i, c, i, ITEMS[i - 1][0]))
    print()

    print('dp 表最后一行（i=5）：')
    print('  容量 c ：' + ''.join('%5d' % x for x in range(0, CAPACITY + 1, 100)))
    print('  dp[5][c]：' + ''.join('%5d' % dp[5][x] for x in range(0, CAPACITY + 1, 100)))
    print()

    solve_and_report('自主实践①：预算改为 800g', ITEMS, 800)
    print()

    chosen_m, names_m, value_m = knapsack_must_include(ITEMS, CAPACITY, 1)
    print('===== 自主实践②：必投项目约束（必投 1-帐篷），容量 1000g =====')
    print('最优重要度：%d，组合编号：%s，物品：%s' % (value_m, chosen_m, names_m))
    print()

    if value == 315 and chosen == [3, 4, 5]:
        print('检查点校验：通过（最优 315，组合 [3,4,5]）')
    else:
        print('检查点校验：未通过（实际 %d，%s）' % (value, chosen))


if __name__ == '__main__':
    main()
