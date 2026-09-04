
def fib_memo(n, memo=None):
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    
    if memo is None:
        memo = {}
    
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n in memo:
        return memo[n]
    
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

def fib_tab(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]

if __name__ == "__main__":
    try:
        n = int(input("Enter a non-negative integer n: "))
        
        print(f"Fibonacci({n}) using Memoization: {fib_memo(n)}")
        print(f"Fibonacci({n}) using Tabulation: {fib_tab(n)}")
    
    except ValueError as e:
        print("Error:", e)
