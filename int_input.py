def int_input(validate=int) -> int:
    """Takes an int as ipt and validates it with the int() function and except ValueError.""" 
    while True:
        ipt = input()
        print()
        try:
            ipt = int(ipt)
        except ValueError:
            print(
                'Invalid input! Try again.'
            )
            continue
        return ipt