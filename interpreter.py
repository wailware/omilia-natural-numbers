DIGITS = set("0123456789")


def parse_tokens(text):
    tokens = text.split()
    if not tokens:
        raise ValueError("Please enter at least one number.")
    for token in tokens:
        if not set(token) <= DIGITS:
            raise ValueError(f"'{token}' is not a number. Use digits only, separated by spaces.")
        if len(token) > 3:
            raise ValueError(f"'{token}' has more than 3 digits.")
    return tokens


def join_tokens(tokens):
    return "".join(tokens)


def is_valid_greek_number(number):
    if len(number) == 10:
        return number.startswith(("2", "69"))
    if len(number) == 14:
        return number.startswith(("00302", "003069"))
    return False


def split_token(token):
    # Breaks a token into the number words it could have been spoken as:
    # 724 -> [700, 20, 4], 69 -> [60, 9], 16 -> [16], 30 -> [30]
    if len(token) > 1 and token[0] == "0":
        return [token]  # leading zeros ("05"): taken as they are
    n = int(token)
    if n < 20:
        return [n]
    if n < 100:
        tens, unit = n // 10 * 10, n % 10
        return [tens, unit] if unit else [tens]
    hundreds, rest = n // 100 * 100, n % 100
    if rest == 0:
        return [hundreds]
    return [hundreds] + split_token(str(rest))


def is_hundreds(x):
    return isinstance(x, int) and x >= 100


def is_tens(x):
    return isinstance(x, int) and 20 <= x <= 90


def is_teen(x):
    return isinstance(x, int) and 10 <= x <= 19


def is_unit(x):
    return isinstance(x, int) and 1 <= x <= 9


def is_number(group):
    # Can these consecutive words be said as one number?
    if len(group) == 1:
        return True
    if len(group) == 2:
        first, second = group
        if is_hundreds(first):
            return is_tens(second) or is_teen(second) or is_unit(second)
        return is_tens(first) and is_unit(second)
    if len(group) == 3:
        return is_hundreds(group[0]) and is_tens(group[1]) and is_unit(group[2])
    return False


def group_text(group):
    if isinstance(group[0], str):
        return group[0]
    return str(sum(group))


def interpretations(tokens):
    words = []
    for token in tokens:
        words += split_token(token)

    memo = {}

    def from_index(i):
        if i == len(words):
            return [""]
        if i in memo:
            return memo[i]
        results = []
        for size in (1, 2, 3):
            group = words[i:i + size]
            if len(group) == size and is_number(group):
                text = group_text(group)
                for rest in from_index(i + size):
                    results.append(text + rest)
        memo[i] = results
        return results

    # first one = the number exactly as it was recognized
    all_results = [join_tokens(tokens)] + from_index(0)
    return list(dict.fromkeys(all_results))
