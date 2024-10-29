# CHALLENGE: Create a script that calculates the discharge, Reynolds and Froude numbers
# based on flow velocity and water depth. For discharge, the function should be able to
# use either trapezoidal, rectangular or circular cross-sections.

def flow_calculator(velocity, area):
    """
    :param velocity: flow velocity of water
    :param area: area of cross-section
    :return: returns flow
    """
    flow = velocity * area
    if flow > 0.01:
        return f"{round(flow,4)} m3/s"
    else:
        flow = flow * 1000
        return f"{round(flow,4)} L/s"


def reynolds_calculator(velocity, length, nu=10**-6):
    re = round(velocity * length / nu, 5)
    if re < 2300:
        return f"{re} (laminar)"
    elif 2300 <= re <= 4000:
        return f"{re} (transitional)"
    else:
        return f"{re} (turbulent)"


def froude_calculator(velocity, flow_depth, g=9.81):
    froude = velocity / ((flow_depth * g)**1/2)
    return froude

def get_numeric_input(prompt):
    while True:
        try:
            value = float(input(prompt))  # using float to allow decimal values
            if value > 0:
                return value
            else:
                print("Please enter a positive number.")
        except ValueError:  # value error occurs when anything other than number is entered
            print("Invalid input! Please enter a numeric value.")

def get_shape_input():
    while True:
        shape = input("Select a cross section (trapezoid, triangular, circular): ").lower()
        if shape in ["trapezoid", "triangular", "circular"]:
            return shape
        else:
            print("Invalid shape selection! Please choose trapezoid, triangular, or circular.")

# Main program
shape = get_shape_input()

if shape == "trapezoid":
    base = get_numeric_input("Enter a base length (m): ")
    height = get_numeric_input("Enter a height (m): ")
    surface = get_numeric_input("Enter a surface length (m): ")
    area = (base + surface) / 2 * height
    flow_depth = height

elif shape == "triangular":
    base = get_numeric_input("Enter a base length (m): ")
    height = get_numeric_input("Enter a height (m): ")
    area = base * height / 2
    flow_depth = height

elif shape == "circular":
    base = get_numeric_input("Enter a diameter (m): ")
    area = (base ** 2 / 4) * 3.1415
    flow_depth = base

else:
    print("Invalid shape selection")
    exit()


velocity = get_numeric_input("Enter a flow velocity (m/s): ")


print(f"Flow: {flow_calculator(velocity, area)}, Reynolds number: {reynolds_calculator(velocity, base)}, Froude number: {round(froude_calculator(velocity, flow_depth),4)}")
