def mod(a: int, b: int) -> int:
    q: int = a // b
    aq: int = b * q
    result: int = a - aq
    return result


def gcd(a: int, b: int) -> int:
    # .while.cond 
    while True:
        mod_result: int = mod(a, b)
        zero: int = 0
        is_term: bool = mod_result == zero 
        if is_term:
            # .while.body
            a: int = b 
            b: int = mod_result 
        else:
            break
    
    # .while.finish 
    return b

if __name__ == '__main__':
    print(gcd(9, 18))
