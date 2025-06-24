# and, or, not

# Function to convert string input to boolean
def string_to_bool(value):
    if value.lower() in ['true', '1', 'yes', 'on']:
        return True
    elif value.lower() in ['false', '0', 'no', 'off']:
        return False
    else:
        raise ValueError(f"Invalid boolean value: {value}")

# Get boolean inputs with proper validation
while True:
    try:
        input1 = input("Enter a boolean value (True/False): ")
        thisShouldBeTrue = string_to_bool(input1)
        break
    except ValueError as e:
        print(f"Error: {e}. Please try again.")

while True:
    try:
        input2 = input("Enter another boolean value (True/False): ")
        thisShouldBeFalse = string_to_bool(input2)
        break
    except ValueError as e:
        print(f"Error: {e}. Please try again.")

print("thisShouldBeTrue: ", thisShouldBeTrue, "thisShouldBeFalse: ", thisShouldBeFalse)

if thisShouldBeTrue and not(thisShouldBeFalse):
    print("thisShouldBeTrue and not thisShouldBeFalse is satisfied")
else:
    print("you loose")

print("\n" + "="*50)
print("Quick demo of the original problem:")
print("="*50)
print("bool('True'):", bool('True'))   # True
print("bool('False'):", bool('False')) # True (This is the problem!)
print("bool(''):", bool(''))           # False