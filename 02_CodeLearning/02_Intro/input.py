# input() is used to get info from user
# ! attention: input() always return a string
user_age = input("Enter your age: ")

# if we wan to use it as a number, we can do
try:
    user_age = int(user_age)
    print(user_age, type(user_age))
    print(f"You are {user_age} years old!")
except ValueError:
    print(f"Error: '{user_age}' is not a valid number!")
    print("Please enter a numeric value for age.")

print("\n" + "="*50)
print("More robust version with input validation:")
print("="*50)

# More robust version - keep asking until valid input
while True:
    try:
        user_age_robust = input("Enter your age (robust version): ")
        user_age_robust = int(user_age_robust)
        print(f"Great! You are {user_age_robust} years old!")
        print(f"Type: {type(user_age_robust)}")
        break  # Exit the loop if conversion successful
    except ValueError:
        print(f"'{user_age_robust}' is not a valid number. Please try again!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        break