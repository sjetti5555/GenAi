#def prime(num):
 #   if num <= 1:
#        return False
 #   for i in range(2, int(num**0.5) + 1):
#        if num % i == 0:
#            return False
#    return True

#print(prime(2))

def calculate_cost(material_costs):
    total_cost = 0
    for material, cost in material_costs.items():
        total_cost += cost
    return total_cost

material_costs = {'cement': 1000, 'steel': 2000, 'sand': 500}
print(f"Total Project Cost: ${calculate_cost(material_costs)}")

    