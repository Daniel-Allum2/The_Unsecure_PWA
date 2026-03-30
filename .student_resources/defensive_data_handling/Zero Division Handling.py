while True:
    try:
        x = int(input("Please enter a number: "))
        y = int(input("Please enter a number: "))
        n = x / y
        print(n)
        break
    except ZeroDivisionError:
        print("Oops!  That was no valid number.  Try again...")
