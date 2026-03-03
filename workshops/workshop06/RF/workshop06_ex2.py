"""
Template for workshop 6, exercise 2
"""

from dataclasses import dataclass
from workshop06_ex1 import solve_firm, solve_hh
from scipy.optimize import root_scalar

@dataclass
class Parameters:
    """
    Container to store the problem's parameters.
    """

    # TODO: Add model parameters
    alpha: float = 0.36 
    z: float = 1.0
    gamma: float = 2.0
    psi: float = 1.0
    theta: float = 0.5
    N1: float = 5.0
    N2: float = 5.0

@dataclass
class Equilibrium:
    """
    Container to store equilibrium allocations and prices.
    """

    par: Parameters = None  # Parameters used to solve the equilibrium
    c1: float = None  # Consumption of type 1 households
    h1: float = None  # Labor supply of type 1 households
    c2: float = None  # Consumption of type 2 households
    h2: float = None  # Labor supply of type 2 households
    pi2: float = None  # Per-capita profits of type 2 households
    w: float = None  # Equilibrium wage
    L: float = None  # Aggregate labor demand
    Y: float = None  # Aggregate output
    Pi: float = None  # Aggregate profits


def compute_labor_ex_demand(w, par: Parameters):
    """
    Compute the excess demand for labor.

    Parameters
    ----------
    w : float
        Wage rate.
    par : Parameters
        Model parameters.

    Returns
    -------
    float
        Excess demand for labor.
    """

    # TODO:
    # 1. compute labor demand, output, and profits using solve_firm()

    L, Y, Pi = solve_firm(w, par)
    # 2. compute optimal consumption and labor supply using solve_hh()

    c1_opt, h1_opt = solve_hh(w, pi=0, par=par) #For c1 consumption does not depend on profit
    c2_opt, h2_opt = solve_hh(w, pi=Pi, par=par)
    
    # 3. compute excess demand for labor
    excess_demand = L - par.N1 * h1_opt - par.N2 * h2_opt
    # 4. return excess demand
    return excess_demand


def compute_equilibrium(par):
    """
    Compute the equilibrium of the model.

    Parameters
    ----------
    par : Parameters
        Model parameters.

    Returns
    -------
    Equilibrium
        Equilibrium object containing the equilibrium values.
    """

    # TODO:
    # 1. call root-finder to find equilibrium wage

    res = root_scalar(compute_labor_ex_demand, x0=0.01, method='newton', args=(par,))

    eq = Equilibrium()

    w_eq = res.root
    eq.w = w_eq

    # 2. compute and store equilibrium values from firm problem

    eq.L, eq.Y, eq.Pi = solve_firm(w_eq, par)

    # 3. compute and store equilibrium values from type-1 household problem

    eq.c1, eq.h1 = solve_hh(w_eq, pi=0, par=par)

    # 4. compute and store equilibrium values from type-2 household problem
    eq.c2, eq.h2 = solve_hh(w_eq, pi=eq.Pi, par=par)

    # 5. return Equilibrium instance
    eq.par = par
    return eq

def print_equilibrium(eq: Equilibrium):
    """
    Print equilibrium prices, allocations, and excess demand.

    Parameters
    ----------
    eq : Equilibrium
        Equilibrium object containing the equilibrium values.
    """

    N1, N2 = eq.par.N1, eq.par.N2

    print('Equilibrium:')
    print('  Households:')
    print(f'    Type 1 (N = {N1}):')
    print(f'      c1 = {eq.c1:.5f}')
    print(f'      h1 = {eq.h1:.5f}')
    print(f'    Type 2 (N = {N2}):')
    print(f'      c2 = {eq.c2:.5f}')
    print(f'      h2 = {eq.h2:.5f}')
    print(f'      pi2 = {eq.pi2:.5f}')
    print('  Firms:')
    print(f'    Y = {eq.Y:.5f}')
    print(f'    L = {eq.L:.5f}')
    print(f'    Pi = {eq.Pi:.5f}')
    print('  Prices:')
    print(f'    w = {eq.w:.5f}')
    print('  Market clearing:')
    print(f'    Labor market: {eq.L - N1 * eq.h1 - N2 * eq.h2:.5e}')
    print(f'    Goods market: {N1 * eq.c1 + N2 * eq.c2 - eq.Y:.5e}')
    print(f'    Profits: {N2 * eq.pi2 - eq.Pi:.5e}')


def foc_error(x, par: Parameters):
    """
    Compute errors in first-order conditions of the household problem
    for type 1 and type 2.

    (for BONUS QUESTION)

    Parameters
    ----------
    x : array_like
        Candidate guess for labor supply (h1, h2).
    par : Parameters
        Model parameters.

    Returns
    -------
    numpy.ndarray
        Array containing the differences from the first-order conditions.
    """

    # TODO:
    # 1. extract candidate guess for labor supply (h1, h2)
    # 2. compute aggregate labor supply
    # 3. compute wage from firm's FOC
    # 4. compute aggregate firm profits
    # 5. compute FOC for HH type 1
    # 6. compute FOC for HH type 2
    # 7. return array with differences of the LHS and RHS of the FOCs


def compute_equilibrium_root(par):
    """
    Compute the equilibrium of the model by running a root finder on
    the household's first-order conditions.

    (for BONUS QUESTION)

    Parameters
    ----------
    par : Parameters
        Model parameters.

    Returns
    -------
    Equilibrium
        Equilibrium object containing the equilibrium values.
    """

    # TODO:
    # 1. call root-finder to find equilibrium labor supplies (h1, h2)
    # 2. compute and store equilibrium values from firm problem
    # 3. compute and store equilibrium values from type-1 household problem
    # 4. compute and store equilibrium values from type-2 household problem
    # 5. return Equilibrium instance


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

    # Use root finder based on households' first-order conditions (bonus question)
    eq_ = compute_equilibrium_root(par)
    print('\nEquilibrium computed using root finder:')
    print_equilibrium(eq_)
