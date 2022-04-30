import matplotlib.pyplot as plt
import math

RADIUS_EARTH = 6371008.0
MU_EARTH = 398600441500000.0
RADIAN_TO_DEGREE = 57.2957795131
DEGREE_TO_RADIAN = 0.01745329251


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


# convert from six orbital elements to cartesian position and velocity
def convert_kepler_to_cartesian(a, e, i, raan, argp, theta):

    p = a * (1 - e ** 2)
    h = math.sqrt(MU_EARTH * p)

    rmag = p / (1 + e * math.cos(theta))

    sin_incl = math.sin(i)
    cos_incl = math.cos(i)
    sin_raan = math.sin(raan)
    cos_raan = math.cos(raan)
    sin_argp_tanom = math.sin(argp + theta)
    cos_argp_tanom = math.cos(argp + theta)
    sin_tanom = math.sin(theta)

    rx = rmag * (cos_raan * cos_argp_tanom - sin_raan * sin_argp_tanom * cos_incl)
    ry = rmag * (sin_raan * cos_argp_tanom + cos_raan * sin_argp_tanom * cos_incl)
    rz = rmag * sin_incl * sin_argp_tanom

    vx = rx * h * e / rmag / p * sin_tanom - h / rmag * (cos_raan * sin_argp_tanom + sin_raan * cos_argp_tanom * cos_incl)
    vy = ry * h * e / rmag / p * sin_tanom - h / rmag * (sin_raan * sin_argp_tanom - cos_raan * cos_argp_tanom * cos_incl)
    vz = rz * h * e / rmag / p * sin_tanom + h / rmag * sin_incl * cos_argp_tanom

    return rx, ry, rz, vx, vy, vz


# convert from 3D cartesian to latitude, longitude, altitude
def convert_cartesian_to_lla(x, y, z):
    r = math.sqrt(x ** 2 + y ** 2 + z ** 2)

    lat = math.asin(z / r)
    lon = math.atan2(y / r, x / r)
    alt = r - RADIUS_EARTH

    return lat, lon, alt


# create earth 2D map on axes
def draw_map():
    # create figure and axis
    fig = plt.figure(figsize=(14,7))
    ax = fig.add_subplot(111)
    
    # overlay image of equirectangular map on axes
    im = plt.imread("images/world_equirectangular_1000px.png")
    ax.imshow(im, extent=(-180,180,-90,90))
    
    return ax


# add a latlon trajectory to 2D map
def add_latlon_trajectory(lat, lon, ax=None):
    """
    lat/lon in as radians, plotted in degrees
    """
    lat, lon = repair_rollover(lat, lon)
                          
    if ax is None:
        ax = draw_map()

    # compact list compreshension syntax
    lat_deg = [la * RADIAN_TO_DEGREE for la in lat]
    lon_deg = [lo * RADIAN_TO_DEGREE for lo in lon]
                          
    ax.plot(lon_deg, lat_deg, "r", linewidth=3)

    return ax


# solve pi to -pi rollover visualization
def repair_rollover(lat, lon):
    # create a copy of input variables since lists are pass by ref
    lat = list(lat)
    lon = list(lon)
    
    # loop to insert nan whenever there is a jump
    i = 1
    while i < len(lon):
        if abs(lon[i] - lon[i-1]) > math.pi:
            lat.insert(i, math.nan)
            lon.insert(i, math.nan)
            i += 2
        else:
            i += 1
    
    return lat, lon