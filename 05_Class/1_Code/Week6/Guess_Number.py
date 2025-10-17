try:
    game_type = int(input(
        """Please choose your game difficulty:
1. Easy(1-10 and unlimited attempts)
2. Medium(1-100 and 10 attempts)
3. Hard(1-1000 and 10 attempts)
Choice (1-3): """))
    
    if game_type <= 0 or game_type > 3:
        raise ValueError("Invalid game type selected.")
except ValueError as e:
    print(f"Error input: {e}")
except EOFError:
    print("No Input")
except KeyboardInterrupt:
    print("Input interrupted")

min_value = 1
max_value = 0
max_attempts = 0

if game_type == 1:
    max_value = 10
    max_attempts = float('inf')  # Unlimited attempts
elif game_type == 2:
    max_value = 100
    max_attempts = 10
elif game_type == 3:
    max_value = 1000
    max_attempts = 10

import random
secret_number = random.randint(min_value, max_value)
attempts = 0

while True:
    try:
        if attempts >= max_attempts:
            print(f"Sorry, you've used all your attempts. The number was {secret_number}.")
            break

        guess = int(input("Enter your guess: "))
        attempts += 1
        if guess == secret_number:
            print("Congratulations! You've guessed the number.")
            break
        elif guess < secret_number:
            print("Too low!")
        else:
            print("Too high!")
    except ValueError as e:
        print(f"Input error: {e}")
