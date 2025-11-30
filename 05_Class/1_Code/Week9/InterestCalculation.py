import math

def calculate_EMI(principal, annual_rate, years):
    """
    Calculate the Equated Monthly Installment (EMI) for a loan.
    :param principal: The principal loan amount
    :param annual_rate: The annual interest rate (in percentage)
    :param years: The loan tenure (in years)
    :return: The calculated EMI
    """
    monthly_rate = annual_rate / 12 / 100
    months = years * 12
    emi = principal * monthly_rate * math.pow(1 + monthly_rate, months) / (math.pow(1 + monthly_rate, months) - 1)
    return emi

if __name__ == "__main__":
    principal = float(input("Enter the principal loan amount: "))
    annual_rate = float(input("Enter the annual interest rate (in %): "))
    years = int(input("Enter the loan tenure (in years): "))
    
    emi = calculate_EMI(principal, annual_rate, years)
    print(f"The Equated Monthly Installment (EMI) is: {emi:.2f}")
