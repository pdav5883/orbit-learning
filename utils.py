import matplotlib.pyplot as plt

RE = 6371008.0
MU = 398600441500000.0

def draw_earth():
    fig, ax = plt.subplots()

    c = plt.Circle((0, 0), RE, color='k')
    ax.add_artist(c)
    ax.set_aspect("equal")
    ax.autoscale(True)

    return ax
