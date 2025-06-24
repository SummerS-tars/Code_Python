a = int(input("Enter a number(a): "))
b = int(input("Enter another number(b): "))

print("a: ", a, "b: ", b)

if a >= b:
    print("a is not less than b")
    if a == b:
        print("a is equal to b")
    else:
        print("a is greater than b")
else:
    print("a is less than b")
