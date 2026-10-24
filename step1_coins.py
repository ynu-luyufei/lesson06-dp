# 第 6 次课 Step1：凑硬币——贪心与动态规划对比
# 面额 [1, 5, 11]，目标金额 15，两个函数各返回枚数与组合

def coin_greedy(coins, amount):
    """贪心：每步取不超过余额的最大面额"""
    coins = sorted(coins, reverse=True)
    remain = amount
    combo = []
    for c in coins:
        while remain >= c:
            remain -= c
            combo.append(c)
    if remain != 0:
        return -1, []
    return len(combo), combo


def coin_dp(coins, amount):
    """动规：dp[c] 表示凑出 c 元的最少枚数，记忆每一步的选择用于回溯"""
    INF = float('inf')
    dp = [INF] * (amount + 1)
    choice = [0] * (amount + 1)
    dp[0] = 0
    for c in range(1, amount + 1):
        for coin in coins:
            # 这一行是动规的心脏：最后一枚取 coin，余额 c-coin 沿用已算好的最优解
            if coin <= c and dp[c - coin] + 1 < dp[c]:
                dp[c] = dp[c - coin] + 1
                choice[c] = coin
    if dp[amount] == INF:
        return -1, []
    combo = []
    cur = amount
    while cur > 0:
        coin = choice[cur]
        combo.append(coin)
        cur -= coin
    return dp[amount], combo


def main():
    coins = [1, 5, 11]
    amount = 15
    g_count, g_combo = coin_greedy(coins, amount)
    d_count, d_combo = coin_dp(coins, amount)

    print('===== Step1 凑硬币：贪心 vs 动态规划 =====')
    print('面额：', coins, ' 目标金额：', amount)
    print('贪心：%d 枚，组合 %s' % (g_count, g_combo))
    print('动规：%d 枚，组合 %s' % (d_count, d_combo))
    print('检查点：贪心 %d 枚（应为 5），动规 %d 枚（应为 3）' % (g_count, d_count))


if __name__ == '__main__':
    main()
