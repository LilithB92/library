from math import pi

r = 5
print(4 / 3 * pi * r ** 3)


def book_delivery(book_count: int, book_price: float = 249.5, sale: int = 40) -> float | None:
    book_real_price = book_price * sale / 100
    if book_count == 1:
        return book_real_price + 100
    elif book_count > 1:
        return (book_count * book_real_price) + (book_count - 1) * 49.5 + 100
    else:
        return None


print(book_delivery(60))
print(249.5*40/100)
print(60 * 99.8 + 59*49.5 + 100)
