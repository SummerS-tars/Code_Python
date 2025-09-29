height = float(input("Please enter your height(m): "))
weight = float(input("Please enter your weight(kg): "))

bmi = weight / (height ** 2)
print(f"Your BMI is: {bmi:.2f}\n")
