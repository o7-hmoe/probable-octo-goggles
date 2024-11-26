import math


def calc_discharge(b, h, k_st, m_bank, S):
    area = h * (b + h * m_bank)
    wetted_perimeter = b + 2 * h * math.sqrt(m_bank**2 + 1)
    hydraulic_radius = area / wetted_perimeter
    discharge = k_st * math.sqrt(S) * hydraulic_radius**(2/3) * area
    return discharge


def calc_discharge2(b, h, m_bank, S, **kwargs):
    for k in kwargs.items():
        if "n_m" in k[0]:
            k_st = 1 / k[1]
        if "D_90" in k[0]:
            k_st = 26 / k[1]**(1/6)
        if "k_st" in k[0]:
            k_st = k[1]
    area = h * (b + h * m_bank)
    wetted_perimeter = b + 2 * h * math.sqrt(m_bank**2 + 1)
    hydraulic_radius = area / wetted_perimeter
    discharge = k_st * math.sqrt(S) * hydraulic_radius**(2/3) * area
    return discharge


def interpolate_h(Q, b, m_bank, S):
    h = 1.0
    eps = 1.0
    iteration_count = 0
    while eps > 10**-3 and iteration_count < 100:
        A = h * (b + h * m_bank)
        P = b + 2 * h * math.sqrt(m_bank ** 2 + 1)
        Qk = A ** (5 / 3) * math.sqrt(S) / (n_m * P ** (2 / 3))
        eps = abs(Q - Qk) / Q
        dA_dh = b + 2 * m_bank * h
        dP_dh = 2 * math.sqrt(m_bank ** 2 + 1)
        F = n_m * Q * P ** (2 / 3) - A ** (5 / 3) * math.sqrt(S)
        dF_dh = 2 / 3 * n_m * Q * P ** (-1 / 3) * dP_dh - 5 / 3 * A ** (2 / 3) * math.sqrt(S) * dA_dh
        h = abs(h - F / dF_dh)
        iteration_count += 1
    return h, eps, Qk, iteration_count


if __name__ == '__main__':
    # input parameters
    Q = 15.5        # discharge in (m3/s)
    b = 5.1         # bottom channel width (m)
    m_bank = 2.5    # bank slope
    k_st = 20       # Strickler value
    n_m = 1 / k_st  # Manning's n
    S_0 = 0.005     # channel slope

print(calc_discharge(b, 2.0, k_st, m_bank, S_0))
print(calc_discharge2(b, 2.0, m_bank, S_0,k_st=20))
print(interpolate_h(Q, b, m_bank, S_0))

    # call the solver with user-defined channel geometry and discharge
    #h_n = interpolate_h(Q, b, n_m=n_m, m_bank=m_bank, S0=S_0)
