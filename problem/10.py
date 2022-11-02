for i in range(5):
    for j in range(i):
        print(" ", end="")
    for j in range(5-i):
        print("*", end="")
    for j in range(4-i):
        print("*", end="")
    print()

for i in range(4):
    for j in range(3-i):
        print(" ", end="")
    for j in range(i+2):
        print("*", end="")
    for j in range(i+1):
        print("*", end="")
    print()
