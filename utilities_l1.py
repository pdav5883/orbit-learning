import matplotlib.pyplot as plt
import math

RADIUS_EARTH = 6371008.0
MU_EARTH = 398600441500000.0

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


# compute orbit radius from polar equation for a single theta
def compute_orbit_radius(a, e, theta):
    return (a * (1 - e * e)) / (1 + e * math.cos(theta))


# convert from r/theta to x/y coordinates for a single value
def convert_polar_to_cartesian(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)

    return x, y


# compute a full orbit in x/y coordinates
def compute_complete_orbit(a, e, N):
    delta = 2 * math.pi / (N - 1)

    x_list = []
    y_list = []

    for i in range(N):
        theta = i * delta
        r = compute_orbit_radius(a, e, theta)

        x, y = convert_polar_to_cartesian(r, theta)

        x_list.append(x)
        y_list.append(y)

    return x_list, y_list
