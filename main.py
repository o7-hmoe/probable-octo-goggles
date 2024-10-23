# Exercise
# Write a function that computes discharge from velocity and area

def flow_from_area(velocity, area):
    return velocity * area


def reynolds_number(velocity, diameter, nu=10**-6):
    """
    doc strings are good to have for documentation
    :param velocity:
    :param diameter:
    :param nu:
    :return:
    """
    re = velocity * diameter / nu
    if re < 2300:
        return "laminar"
    elif 2300 <= re <= 4000:
        return "transitional"
    else:
        return "turbulent"


v = 3
h = 1.5
b = 5
A = b * h

print("The discharge is {0}".format(str(flow_from_area(v, A))))
print("The flow is " + reynolds_number(1, 1))

#Challenge : create a script that calculates the Reynolds number and Froude numbers
# based on water depth and flow velocity. For discharge, the function should be able to use
# either trapezoidal, rectangular or circular cross sections.

