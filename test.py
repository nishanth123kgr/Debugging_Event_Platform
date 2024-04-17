import sys
def longest_palindromic_substring(s):
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    longest = ""
    for i in range(len(s)):
        palindrome_odd = expand_around_center(i, i)
        if len(palindrome_odd) > len(longest):
            longest = palindrome_odd

        palindrome_even = expand_around_center(i, i + 1)
        if len(palindrome_even) > len(longest):
            longest = palindrome_even

    return longest

print(longest_palindromic_substring(sys.argv[1])) # Don't touch this line