"""
Template for workshop 6, exercise 1
"""

from dataclasses import dataclass
import numpy as np


@dataclass
class Parameters:
    """
    Container to store the problem's parameters.
    """

    # TODO: add model parameters


@dataclass
class Equilibrium:
    """
    Container to store equilibrium allocations and prices.
    """

    par: Parameters = None  # Parameters used to solve the equilibrium
    c: float = None  # Optimal consumption
    h: float = None  # Optimal labor supply
    w: float = None  # Equilibrium wage
    L: float = None  # Aggregate labor demand
    Y: float = None  # Aggregate output
    Pi: float = None  # Aggregate profits


def util(c, h, par: Parameters):
    """
    Compute the utility of a given consumption/labor supply choice.

    Parameters
    ----------
    c : float
        Consumption
    h : float
        Labor supply
    par : Parameters
        Parameter instance

    Returns
    -------
    u : float
        Utility
    """

    # Consumption utility
    if par.gamma == 1:
        # Log utility
        u = np.log(c)
    else:
        # General CRRA utility
        u = (c ** (1 - par.gamma) - 1) / (1 - par.gamma)

    # add disutility of labor
    u -= par.psi * h ** (1 + 1 / par.theta) / (1 + 1 / par.theta)

    return u


def solve_hh(w, pi, par: Parameters):
    """
    Solve household problem for given prices and parameters.

    Parameters
    ----------
    w : float
        Wage rate
    pi : float
        Firm profits distributed to households
    par : Parameters
        Parameter instance

    Returns
    -------
    c_opt : float
        Optimal consumption
    h_opt : float
        Optimal labor supply
    """

    # TODO:
    # 1. call minimizer to find the optimal hours choice
    # 2. compute optimal consumption from budget constraint
    # 3. return optimal consumption and labor supply


def solve_firm(w, par: Parameters):
    """
    Compute labor demand and profits implied by firm's first-order condition
    for given prices w.

    Parameters
    ----------
    w : float
        Wage rate
    par : Parameters
        Parameter instance

    Returns
    -------
    L : float
        Labor demand
    Y : float
        Aggregate output
    Pi : float
        Aggregate profits
    """

    # TODO:
    # 1. compute labor demand L from equation (1.1)
    # 2. compute output Y
    # 3. compute profits Pi
    # 4. return labor demand, output, and profits


def compute_labor_ex_demand(w, par: Parameters):
    """
    Compute excess demand for labor.

    Parameters
    ----------
    w : float
        Wage rate
    par : Parameters
        Parameter instance

    Returns
    -------
    ex_demand : float
        Excess demand for labor
    """

    # TODO:
    # 1. compute labor demand, output, and profits using solve_firm()
    # 2. compute optimal consumption and labor supply using solve_hh()
    # 3. compute excess demand for labor
    # 4. return excess demand


def compute_equilibrium(par):
    """
    Compute the equilibrium for given parameters.

    Parameters
    ----------
    par : Parameters
        Parameter instance

    Returns
    -------
    eq : Equilibrium
        Equilibrium instance containing equilibrium values
    """

    # TODO:
    # 1. call root-finder to find equilibrium wage
    # 2. compute and store equilibrium values from firm problem
    # 3. compute and store equilibrium values from household problem
    # 4. return Equilibrium instance


def print_equilibrium(eq: Equilibrium):
    """
    Print equilibrium prices, allocations, and excess demand.

    Parameters
    ----------
    eq : Equilibrium
        Equilibrium instance containing equilibrium values
    """

    print('Equilibrium:')
    print('  Households:')
    print(f'    c = {eq.c:.5f}')
    print(f'    h = {eq.h:.5f}')
    print('  Firms:')
    print(f'    Y = {eq.Y:.5f}')
    print(f'    L = {eq.L:.5f}')
    print(f'    Pi = {eq.Pi:.5f}')
    print('  Prices:')
    print(f'    w = {eq.w:.5f}')
    print('  Market clearing:')
    print(f'    Labor market: {eq.L - eq.h:.5e}')
    print(f'    Goods market: {eq.c - eq.Y:.5e}')


def compute_analytical_solution(par: Parameters):
    """
    Compute analytical solution for given parameters.

    Parameters
    ----------
    par : Parameters
        Parameter instance

    Returns
    -------
    L : float
        Analytical solution for labor supply
    """

    # Base from the analytical formula for L from (1.2)
    x = (1 - par.alpha) * par.z ** (1 - par.gamma) / par.psi
    # Exponent in the analytical formula for L
    xp = 1 / (1 / par.theta + par.alpha + par.gamma * (1 - par.alpha))

    L = x**xp

    return L


if __name__ == '__main__':
    """
    Main script to compute and print the equilibrium of the model.
    """

    # Get instance of default parameter values
    par = Parameters()

    # Solve for equilibrium
    eq = compute_equilibrium(par)

    # Print equilibrium quantities and prices
    print_equilibrium(eq)

    # Compare to analytical solution
    L = compute_analytical_solution(par)
    print(f'Analytical solution: h = L = {L:.5f}')
