for i in range(5):
    for j in range(4-i):
        print(" ", end="")
    for j in range(i+1):
        print("*", end="")
    for j in range(i):
        print("*", end="")
    print()
