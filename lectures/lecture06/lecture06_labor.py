"""
Lecture 6: Consumption & labor supply

This module implements the solution for the general equilibrium economy where 
    - households choose consumption and labor supply, and 
    - firms have a Cobb-Douglas production function using capital and labor.
"""

from dataclasses import dataclass
import numpy as np
from scipy.optimize import minimize, root_scalar


@dataclass
class Parameters:
    """
    Container to store the problem's parameters.
    """
    alpha: float = 0.36     # Capital share in production function
    z: float = 1.0          # TFP 
    gamma: float = 2.0      # Relative risk aversion (RRA) in utility
    psi: float = 1.0        # Weight on disutility of working
    theta: float = 0.5      # Frisch elasticity of labor supply
    a: float = 5.0          # Initial assets (capital)


@dataclass
class Equilibrium:
    """
    Container to store equilibrium allocations and prices.
    """
    par: Parameters = None  # Parameters used to compute equilibrium
    c: float = None         # Optimal consumption
    h: float = None         # Optimal hours
    r: float = None         # Interest rate
    w: float = None         # Wage rate
    L: float = None         # Labor demand
    K: float = None         # Capital demand
    Y: float = None         # Output


def util(c, h, par: Parameters):
    """
    Compute the utility of a given consumption/labor supply choice.

    Parameters
    ----------
    c : float
        Consumption
    h : float
        Hours worked
    par : Parameters
        Parameters for given problem

    Returns
    -------
    u : float
        Utility level

    """

    # Consumption utility
    if par.gamma == 1:
        # Log utility
        u = np.log(c)
    else:
        # General CRRA utility
        u = (c**(1-par.gamma) - 1) / (1-par.gamma)

    # add disutility of labor
    u -= par.psi * h**(1 + 1/par.theta) / (1 + 1/par.theta)

    return u



def solve_hh(r, w, par: Parameters):
    """
    Solve household problem for given prices and parameters

    Parameters
    ----------
    r : float
        Return on capital
    w : float
        Wage rate
    par : Parameters
        Parameters for given problem

    Returns
    -------
    c_opt : float 
        Optimal consumption choice
    h_opt : float
        Optimal hours choice
    """

    # Initial guess for h
    h_guess = 0.5

    # Run minimizer to find optimal hours.
    # The budget constraint is inserted directly in the lambda expression.
    res = minimize(
        lambda h: -util(r*par.a + w * h, h, par),
        x0=h_guess,
        method='L-BFGS-B',
        bounds=((0, None), )
    )

    if not res.success:
        print('Minimizer did not terminate successfully')
        print(res.message)
        print(f'  Prices: {r}, {w}')

    # Recover optimal hours choice
    h_opt = res.x[0]
    # Optimal consumption follows from budget constraint
    c_opt = r * par.a + w * h_opt

    return c_opt, h_opt


def solve_firm(w, par: Parameters):
    """
    Return the solution to the firm's problem for given wage rate and parameters.

    Parameters
    ----------
    w : float
        Wage rate
    par : Parameters
        Parameters for given problem

    Returns
    -------
    L : float
        Firm labor demand
    Y : float
        Firm output
    r : float
        Interest rate implied by wage rate

    """

    # Capital market clearing condition
    K = par.a

    # Labor demand implied by firm FOC
    L = (w / (1-par.alpha) / par.z)**(-1/par.alpha) * K

    # Optimal capital-labor ratio
    k = K / L

    # Return on capital
    r = par.z * par.alpha * k**(par.alpha - 1)

    # Output
    Y = par.z * K**par.alpha * L**(1-par.alpha)
    
    return L, Y, r


def compute_labor_ex_demand(w, par: Parameters):
    """
    Compute excess labor demand for given wage rate and parameters.

    Parameters
    ----------
    w : float
        Wage rate
    par : Parameters
        Parameters for given problem

    Returns
    -------
    ex_demand : float 
        Excess labor demand (firm demand minus household supply)
    """

    # Solve firm problem for given wage rate
    L, Y, r = solve_firm(w, par)

    # Optimal household choices for given prices
    c_opt, h_opt = solve_hh(r, w, par)

    # Excess demand for labor
    ex_demand = L - h_opt

    return ex_demand


def compute_equilibrium(par: Parameters):
    """
    Compute the general equilibrium for given parameters.

    Parameters
    ----------
    par : Parameters
        Parameters for given problem

    Returns
    -------
    eq : Equilibrium
        Equilibrium allocation and prices
    """

    res = root_scalar(
        compute_labor_ex_demand, x0=1, method='newton', args=(par, )
    )

    if not res.converged:
        print('Equilibrium root finder did not terminate successfully')

    # Create instance of equilibrium class
    eq = Equilibrium(par=par, K=par.a, w=res.root)

    # Equilibrium firm choices and prices
    eq.L, eq.Y, eq.r = solve_firm(eq.w, par)
    # Equilibrium household choices
    eq.c, eq.h = solve_hh(eq.r, eq.w, par)

    return eq


def print_equilibrium(eq: Equilibrium):
    """
    Print equilibrium prices, allocations, and excess demand.

    Parameters
    ----------
    eq : Equilibrium
        Equilibrium allocation and prices
    """
    print('Equilibrium:')
    print('  Households:')
    print(f'    c = {eq.c:.5f}')
    print(f'    h = {eq.h:.5f}')
    print('  Firms:')
    print(f'    Y = {eq.Y:.5f}')
    print(f'    L = {eq.L:.5f}')
    print(f'    K = {eq.K:.5f}')
    print('  Prices:')
    print(f'    r = {eq.r:.5f}')
    print(f'    w = {eq.w:.5f}')    
    print('  Market clearing:')
    print(f'    Labor market: {eq.L - eq.h:.5e}')
    print(f'    Goods market: {eq.c - eq.Y:.5e}')


def compute_equilibrium_analytical(par: Parameters):
    """
    Compute the analytical equilibrium labor demand for given parameters.

    Parameters
    ----------
    par : Parameters
        Parameters for given problem

    Returns
    -------
    L : float
        Equilibrium labor demand
    """

    # Base in the analytical formula for L
    x = (1-par.alpha) * (par.z * par.a**par.alpha)**(1-par.gamma) / par.psi

    # Inverse exponent
    xp = 1/par.theta + par.alpha + par.gamma - par.alpha * par.gamma

    # Equilibrium labor
    L = x**(1/xp)

    return L


if __name__ == '__main__':

    # Create parameter instance
    par = Parameters()

    # Solve for the equilibrium numerically|
    eq = compute_equilibrium(par)

    print_equilibrium(eq)

    # Compute equilibrium L analytically
    L_exact = compute_equilibrium_analytical(par)

    # Print analytical L for comparison with numerical solution
    print(f'Exact equilibrium L: {L_exact:.5f}')
