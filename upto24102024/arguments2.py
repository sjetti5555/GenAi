def calculate_wages(basic_salary, *bonuses, **deductions):
    total_wages = basic_salary + sum(bonuses) - sum(deductions.values())
    return total_wages

basic_salary = 10000
wages = calculate_wages(basic_salary, 200, 300, health_insurance=150, tax=200)
print(f"Total Wages: ${wages}")
