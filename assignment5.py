def brute_force_lcs(seq1, seq2):
    def helper(i, j):
        if i == 0 or j == 0:
            return 0
        if seq1[i - 1] == seq2[j - 1]:
            return 1 + helper(i - 1, j - 1)
        return max(helper(i - 1, j), helper(i, j - 1))
    return helper(len(seq1), len(seq2))

def memoized_lcs(seq1, seq2):
    memo = {}
    def helper(i, j):
        if i == 0 or j == 0:
            return 0
        if (i, j) in memo:
            return memo[(i, j)]
        if seq1[i - 1] == seq2[j - 1]:
            result = 1 + helper(i - 1, j - 1)
        else:
            result = max(helper(i - 1, j), helper(i, j - 1))
        memo[(i, j)] = result
        return result
    return helper(len(seq1), len(seq2))

def build_lcs_table(seq1, seq2):
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp

def reconstruct_lcs(dp, seq1, seq2):
    i, j = len(seq1), len(seq2)
    result = []
    while i > 0 and j > 0:
        if seq1[i - 1] == seq2[j - 1]:
            result.append(seq1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    result.reverse()
    return "".join(result) if isinstance(seq1, str) else result

def lcs(seq1, seq2):
    dp = build_lcs_table(seq1, seq2)
    length = dp[len(seq1)][len(seq2)]
    subsequence = reconstruct_lcs(dp, seq1, seq2)
    return length, subsequence, dp

def print_dp_table(dp, seq1, seq2):
    header = "     " + " ".join(f"{c:>2}" for c in seq2)
    print(header)
    for i, row in enumerate(dp):
        label = seq1[i - 1] if i > 0 else " "
        print(f"  {label:>2} | " + " ".join(f"{v:>2}" for v in row))

if __name__ == "__main__":
    seq1 = "ABCBDAB"
    seq2 = "BDCABA"
    print(f"Sequence 1: {seq1}")
    print(f"Sequence 2: {seq2}\n")

    length, subsequence, dp = lcs(seq1, seq2)
    print("DP Table (dp[i][j] = LCS length of seq1[:i] and seq2[:j]):")
    print_dp_table(dp, seq1, seq2)
    print(f"\nLCS length      : {length}")
    print(f"LCS subsequence  : {subsequence}")

    print(f"\n[check] memoized_lcs length : {memoized_lcs(seq1, seq2)}")
    print(f"[check] brute_force_lcs length (small input 'ABC' vs 'AC') : "
          f"{brute_force_lcs('ABC', 'AC')}")

    list1 = ["walk", "to", "the", "store", "and", "buy", "milk"]
    list2 = ["drive", "to", "store", "buy", "some", "milk"]
    length2, subsequence2, _ = lcs(list1, list2)
    print("\nWord-list example:")
    print(f"List 1 : {list1}")
    print(f"List 2 : {list2}")
    print(f"LCS length : {length2}")
    print(f"LCS words  : {subsequence2}")