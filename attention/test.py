from typing import List
import sys


class Solution:
    def partition(self, s: str) -> List[List[str]]:
        ans = []
        path = []
        n = len(s)

        def dfs(i, start):
            if i == n:
                ans.append(path.copy())
                return
            if i < n - 1:
                dfs(i + 1, start)
            t = s[start:i + 1]
            if t == t[::-1]:
                path.append(t)
                dfs(i + 1, i + 1)
                path.pop()

        dfs(0, 0)
        return ans


def main():
    sol = Solution()

    # 1. 读取测试用例数量
    n = int(input().strip())

    # 2. 循环处理每一组
    for _ in range(n):
        s = input().strip()  # 读取字符串
        result = sol.partition(s)
        # 笔试中通常直接打印即可，LeetCode的return在这里变成print
        print(result)


if __name__ == "__main__":
    main()