from cs50 import get_int

height = 0
# Condition to checks if the input is between 1 and 8
while height > 8 or height < 1:
    height = get_int("Height: ")
space = height
blocks = 0

for i in range(height):
    blocks += 1
    x = 0
    # Print Whitespaces
    while x < space:
        if x != space - 1:
            print(" ", end="")
        x += 1
    x = 0
    # Print Blocks
    while x < blocks:
        if x == blocks - 1:
            print("#")
        else:
            print("#", end="")
        x += 1
    space -= 1
