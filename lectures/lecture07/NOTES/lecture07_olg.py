"""
Lecture 7: Overlapping generations (OLG)

This module implements the solution for the general equilibrium economy 
with overlapping generations where 
    - households choose consumption when young and old, and 
    - firms have a Cobb-Douglas production function using capital and labor.
"""

import numpy as np
from dataclasses import dataclass
from scipy.optimize import root_scalar
import copy
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


@dataclass
class Parameters:
    """
    Parameters for the overlapping generations model.
    """
    alpha: float = 0.36     # Capital share in production function
    delta: float = 1.0      # Depreciation rate
    z: float = 1.0          # TFP 
    beta: float = 0.96**30  # Discount factor (0.96 per year, 30-year periods)
    gamma: float = 2.0      # RRA in utility
    N: int = 1              # Number of households per cohort  


@dataclass
class SteadyState:
    """
    Steady-state equilibrium of the OLG model.
    """
    par: Parameters = None      # Parameters used to compute equilibrium
    c_y: float = None           # Consumption when young
    c_o: float = None           # Consumption when old 
    a: float = None             # Savings when young
    s: float = None             # Savings rate when young
    r: float = None             # Interest rate (return on capital)
    w: float = None             # Wage rate
    K: float = None             # Aggregate capital stock
    L: float = None             # Aggregate labor demand
    I: float = None             # Aggregate investment
    Y: float = None             # Aggregate output


@dataclass
class Simulation:
    """
    Container to store simulation results
    """
    c_y: np.ndarray = None      # Time series for consumption when young
    c_o: np.ndarray = None      # Time series for consumption when old 
    a: np.ndarray = None        # Time series for savings when young
    s: np.ndarray = None        # Time series for savings rate when young
    r: np.ndarray = None        # Time series for interest rate (return on capital)
    w: np.ndarray = None        # Time series for wages
    K: np.ndarray = None        # Time series for aggregate capital stock
    Y: np.ndarray = None        # Time series for aggregate output
    z: np.ndarray = None        # Time series for TFP


def compute_prices(k, par: Parameters):
    """
    Return factor prices for a given capital-labor ratio and parameters.

    Parameters
    ----------
    k : float
        Capital-labor ratio
    par : Parameters
        Parameters for the given problem

    Returns
    -------
    r : float
        Return on capital after depreciation (interest rate)
    w : float
        Wage rate

    """

    # Return on capital after depreciation (interest rate)
    r = par.alpha * par.z * k**(par.alpha - 1) - par.delta

    # Wage rate
    w = (1-par.alpha) * par.z * k**par.alpha
    
    return r, w


def compute_savings_rate(r, par: Parameters):
    """
    Compute the savings rate using the analytical solution
    to the household problem.

    Parameters
    ----------
    r : float
        Return on capital after depreciation (interest rate)
    par : Parameters
        Parameters for the given problem

    Returns
    -------
    s : float
        Savings rate
    """

    s = 1/(1 + par.beta**(-1/par.gamma) * (1+r)**(1-1/par.gamma))

    return s


def compute_capital_ex_demand(k, par: Parameters):
    """
    Compute the excess demand for capital.

    Parameters
    ----------
    k : float
        Capital-labor ratio
    par : Parameters
        Parameters for the given problem

    Returns
    -------
    ex_demand : float
        Excess demand for capital
    """
    
    # Compute prices from firm's FOCs
    r, w = compute_prices(k, par)

    # Compute savings rate
    srate = compute_savings_rate(r, par)

    # Aggregate supply of capital by households (savings)
    A = srate * w * par.N

    # Aggregate labor supply
    L = par.N

    # Aggregate capital demand
    K = k * L

    # Excess demand for capital
    ex_demand = K - A

    return ex_demand


def compute_steady_state(par: Parameters):
    """
    Compute the steady-state equilibrium for the OLG model.

    Parameters
    ----------
    par : Parameters
        Parameters for the given problem

    Returns
    -------
    eq : SteadyState
        Steady-state equilibrium of the OLG model
    """

    # Find the equilibrium k=K/L with a root finder. Excess demand for capital
    # has to be zero in equilibrium.
    res = root_scalar(
        compute_capital_ex_demand, bracket=(1.0e-3, 10), args=(par, )
    )

    if not res.converged:
        print('Equilibrium root finder did not terminate successfully')

    # Equilibrium K
    K = res.root * par.N

    # Create instance of equilibrium class
    eq = SteadyState(par=par, K=K, L=par.N)

    # Equilibrium prices
    eq.r, eq.w = compute_prices(eq.K / eq.L, par)

    # Investment in steady state
    eq.I = eq.K * par.delta
    
    # Equilibrium household choices
    eq.s = compute_savings_rate(eq.r, par)
    eq.a = eq.s * eq.w
    eq.c_y = eq.w - eq.a
    eq.c_o = (1 + eq.r) * eq.a

    # Equilibrium output
    eq.Y = par.z * eq.K**par.alpha * eq.L**(1-par.alpha)

    # Aggregate consumption
    C = par.N * (eq.c_y + eq.c_o)
    # Check that goods market clearing holds using Y = C + I
    assert abs(eq.Y - C - eq.I) < 1.0e-8

    return eq


def print_steady_state(eq: SteadyState):
    """
    Print equilibrium prices, allocations, and excess demand.

    Parameters
    ----------
    eq : SteadyState
        SteadyState of the OLG model
    """

    # Number of households
    N = eq.par.N

    print('Steady-state equilibrium:')
    print('  Households:')
    print(f'    c_y = {eq.c_y:.5f}')
    print(f'    c_o = {eq.c_o:.5f}')
    print(f'    a = {eq.a:.5f}')
    print('  Firms:')
    print(f'    K = {eq.K:.5f}')
    print(f'    L = {eq.L:.5f}')
    print(f'    Y = {eq.Y:.5f}')
    print('  Prices:')
    print(f'    r = {eq.r:.5f}')
    print(f'    w = {eq.w:.5f}')
    print('  Market clearing:')
    print(f'    Capital market: {eq.K - eq.a * N:.5e}')
    print(f'    Goods market: {(eq.c_y + eq.c_o + eq.a) * N - eq.Y - (1-eq.par.delta) * eq.K:.5e}')


def initialize_sim(T, eq: SteadyState = None):
    """
    Initialize simulation instance (allocate arrays for time series).

    Parameters
    ----------
    T : int
        Number of periods to simulate
    eq : SteadyState, optional
        Steady-state equilibrium to use for initial period
    """

    # Initialize simulation instance
    sim = Simulation()

    # Initialize time series
    sim.c_y = np.empty(T+1)
    sim.c_o = np.empty(T+1)
    sim.a = np.empty(T+1)
    sim.s = np.empty(T+1)
    sim.r = np.empty(T+1)
    sim.w = np.empty(T+1)
    sim.K = np.empty(T+1)
    sim.Y = np.empty(T+1)
    sim.z = np.empty(T+1)

    if eq is not None:
        # Set initial values to steady-state values
        sim.c_y[0] = eq.c_y
        sim.c_o[0] = eq.c_o
        sim.a[0] = eq.a
        sim.s[0] = eq.s
        sim.r[0] = eq.r
        sim.w[0] = eq.w
        sim.K[0] = eq.K
        sim.Y[0] = eq.Y
        sim.z[0] = eq.par.z

    return sim


def simulate_olg(z_new, eq: SteadyState, T = 10):
    """
    Simulate the transition dynamics of the OLG model.

    Parameters
    ----------
    z_new : float
        New level of TFP after the shock.
    eq : SteadyState
        Initial steady-state equilibrium before the shock.
    T : int
        Number of periods to simulate.

    Returns
    -------
    sim : Simulation
        Simulation object containing the time series for each variable.
    """

    # Retrieve parameter object attached to steady-state equilibrium
    par = eq.par

    # The following code only works for log utility
    if par.gamma != 1:
        raise ValueError('Simulation only implemented for log utility')
    
    # Initialize simulation instance and allocate arrays
    sim = initialize_sim(T, eq)

    # TFP is assumed to be at new level for all remaining periods
    sim.z[1:] = z_new

    # Copy parameters to avoid changing the original instance
    par_ = copy.copy(par)

    # Savings rate is independent of r for gamma = 1 and constant over time
    s = par.beta / (1 + par.beta)
    sim.s[:] = s

    for t in range(1, T+1):
        # Update TFP with current value
        par_.z = sim.z[t]

        # Capital stock is predetermined by savings of old in previous period
        sim.K[t] = sim.a[t-1] * par.N

        # Prices given predetermined capital stock and current z
        sim.r[t], sim.w[t] = compute_prices(sim.K[t] / par.N, par_)

        # Savings by the young
        sim.a[t] = s * sim.w[t]
        # Consumption by the young
        sim.c_y[t] = (1-s) * sim.w[t]
        # Consumption by the old
        sim.c_o[t] = (1 + sim.r[t]) * sim.a[t-1]
        # Aggregate output
        sim.Y[t] = sim.z[t] * sim.K[t]**par.alpha * par.N**(1-par.alpha)

        # Verify that goods market clearing holds
        demand = par.N * (sim.c_y[t] + sim.c_o[t] + sim.a[t])
        supply = sim.Y[t] + (1 - par.delta) * sim.K[t]
        assert abs(demand - supply) < 1.0e-8

    return sim


def plot_simulation(eq, sim, eq_new = None, deviations=True, filename=None):
    """
    Plot the selected simulated time series of the OLG model.

    Parameters
    ----------
    eq : SteadyState
        The equilibrium containing the initial steady-state parameters.
    sim : Simulation
        The simulation containing the time series data.
    eq_new : SteadyState, optional
        The equilibrium containing the new steady-state parameters.
    deviations : bool
        If True, plot deviations from the initial steady state instead
        of absolute values.
    filename : str, optional
        If provided, save the figure to this location.
    """

    fig, axes = plt.subplots(
        3, 2, figsize=(6, 6), sharex=True, sharey='row' if deviations else False
    )

    # Keyword arguments for time series plots
    kwargs = {
        'marker': 'o' if len(sim.K) < 30 else None,
        'markersize': 4,
        'color': 'steelblue',
    }

    # Keyword arguments for horizontal lines indicating (initial) steady state
    kwargs_init = {
        'color': 'black',
        'linewidth': 0.5,
        'linestyle': '--',
        'label': 'Steady state' if eq_new is None else 'Initial steady state'
    }

    # Keyword arguments for horizontal lines indicating new steady state
    kwargs_new = {
        'color': 'red',
        'linewidth': 0.5,
        'linestyle': '--',
        'label': 'New steady state'
    }

    if eq_new is not None:
        ylabel = "Deviation from initial SS" if deviations else None
    else:
        ylabel = "Deviation from SS" if deviations else None

    # Plot TFP time series
    yvalues = sim.z / eq.par.z - 1 if deviations else sim.z
    axes[0, 0].plot(yvalues, label="Time series", **kwargs)
    # Horizontal line at old steady state
    yvalues = 0 if deviations else eq.par.z
    axes[0, 0].axhline(yvalues, **kwargs_init)
    # Horizontal line at new steady state
    if eq_new is not None:
        yvalues = eq_new.par.z / eq.par.z - 1 if deviations else eq_new.par.z
        axes[0, 0].axhline(yvalues, **kwargs_new)
    axes[0, 0].set_ylabel(ylabel)
    axes[0, 0].set_title("TFP $z$")

    # Plot output time series
    yvalues = sim.Y / eq.Y - 1 if deviations else sim.Y
    axes[0, 1].plot(yvalues, **kwargs)
    # Horizontal line at old steady state
    yvalues = 0 if deviations else eq.Y
    axes[0, 1].axhline(yvalues, **kwargs_init)
    # Horizontal line at new steady state
    if eq_new is not None:
        yvalues = eq_new.Y / eq.Y - 1 if deviations else eq_new.Y
        axes[0, 1].axhline(yvalues, **kwargs_new)
    axes[0, 1].set_title("Output $Y$")

    # Plot capital time series
    yvalues = sim.K / eq.K - 1 if deviations else sim.K
    axes[1, 0].plot(yvalues, **kwargs)
    # Horizontal line at old steady state
    yvalues = 0 if deviations else eq.K
    axes[1, 0].axhline(yvalues, **kwargs_init)
    # Horizontal line at new steady state
    if eq_new is not None:
        yvalues = eq_new.K / eq.K - 1 if deviations else eq_new.K
        axes[1, 0].axhline(yvalues, **kwargs_new)
    axes[1, 0].set_title("Capital $K$")
    axes[1, 0].set_ylabel(ylabel)

    # Plot wage time series
    yvalues = sim.w / eq.w - 1 if deviations else sim.w
    axes[1, 1].plot(yvalues, **kwargs)
    # Horizontal line at old steady state
    yvalues = 0 if deviations else eq.w
    axes[1, 1].axhline(yvalues, **kwargs_init)
    # Horizontal line at new steady state
    if eq_new is not None:
        yvalues = eq_new.w / eq.w - 1 if deviations else eq_new.w
        axes[1, 1].axhline(yvalues, **kwargs_new)
    axes[1, 1].set_title("Wage $w$")

    # Plot interest rate time series
    axes[2, 0].plot(sim.r, **kwargs)
    # Horizontal line at old steady state
    axes[2, 0].axhline(eq.r, **kwargs_init)
    # Horizontal line at new steady state
    if eq_new is not None:
        axes[2, 0].axhline(eq_new.r, **kwargs_new)
    axes[2, 0].set_xlabel("Period")
    axes[2, 0].set_title("Interest rate $r$")
    axes[2, 0].yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))

    # Turn off last subplot
    axes[2, 1].axis('off')

    # Apply settings common to all axes
    if deviations:
        for ax in axes.flat[:-2]:
            # Set percent formatting for y-tick labels
            ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
            ax.set_ylim((-0.2, 0.02))

    axes[0, 0].legend()
    fig.tight_layout()

    # Optionally save the figure
    if filename:
        plt.savefig(filename)


if __name__ == '__main__':

    # Create parameter instance
    par = Parameters()

    # Solve for the equilibrium numerically
    eq = compute_steady_state(par)

    # Print equilibrium quantities and prices
    print_steady_state(eq)

    # Transition dynamics
    par = Parameters(gamma=1)

    # Initial steady state
    eq_init = compute_steady_state(par)

    # Number of periods to simulate
    T = 10

    # New TFP level (10% drop from steady state)
    z_new = 0.9 * par.z

    # Perform simulation
    sim = simulate_olg(z_new, eq_init, T=T)

    # Compute new steady state
    eq_new = compute_steady_state(par=Parameters(gamma=par.gamma, z=z_new))

    # Plot simulation results
    plot_simulation(eq_init, sim, eq_new)
