def plural_form(n: int) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return "монета"
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        return "монеты"
    else:
        return "монет"
