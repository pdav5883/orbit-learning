import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp 


RADIUS_EARTH = 6371008.0
MU_EARTH = 398600441500000.0

def throw_ball(altitude, speed, maxtime):
    """
    Throw a ball from +y axis (m) in +x direction (m/s), propagate to impact or maxtime
    """
    r0 = np.array([0, RADIUS_EARTH + altitude, 0])
    v0 = np.array([speed, 0, 0])
    
    if altitude < 1000:
        max_step = 0.1
    elif altitude < 100000:
        max_step = 0.5
    elif altitude < 200000:
        max_step = 1
    else:
        max_step = 10
    
    trajectory, t = propagate_twobody(r0, v0, maxtime, max_step)
    
    x = trajectory[:, 0]
    y = trajectory[:, 1]
    
    return x, y
    

def propagate_twobody(r0, v0, tmax, max_step=np.inf, use_impact=True):
    """
    Propagate cartesian state by integrating eom directly.
    
    r0: 3, t0 position
    v0: 3, t0 velocity
    tmax: the max propagation time for the trajectory
    max_tstep: max allowable time step, recommend using None to allow RK to pick time steps
    
    Return: N,6 np array of state; N, np array of time steps
    """
    y0 = np.concatenate([r0, v0])
    
    sol = solve_ivp(twobody_eom, (0, tmax), y0, method='RK45', events=[impact_event], max_step=max_step, rtol=1e-8)
    
    return sol.y.transpose(), sol.t


def twobody_eom(t, y):
    """
    y[0]: x position
    y[1]: y position
    y[2]: z position
    y[3]: x velocity
    y[4]: y vecolity
    y[5]: z vecolity
    """
    r = np.sqrt(y[0] ** 2 + y[1] ** 2 + y[2] ** 2)
    g = MU_EARTH / r ** 3

    return np.array([
        y[3],
        y[4],
        y[5],
        -g * y[0],
        -g * y[1],
        -g * y[2]
    ])


def impact_event(t, y):
    return y[0]**2 + y[1]**2 + y[2]**2 - RADIUS_EARTH**2

impact_event.terminal = True
impact_event.direction = -1


# this function creates an empty 2D plot with earth at center
def draw_earth():
    # create figure and axis objects using matplotlib library
    fig, ax = plt.subplots(figsize=(8,8))
    
    # create a black circle at origin
    c = plt.Circle((0,0), RADIUS_EARTH, color="k")
    ax.add_artist(c)
    
    # equal aspect ratio between x and y axes and axis limits
    ax.set_aspect("equal")
    ax.set_xlim([-1.05 * RADIUS_EARTH, 1.05 * RADIUS_EARTH])
    ax.set_ylim([-1.05 * RADIUS_EARTH, 1.05 * RADIUS_EARTH])
    
    # hide markers on axes
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # return the ax object to allow adding trajectories
    return ax


# add a trajectory to new or existing 2D plot
def add_trajectory(x, y, ax=None):
    if ax is None:
        ax = draw_earth()
    ax.autoscale(True)    
    ax.plot(x, y)
    
    return ax



