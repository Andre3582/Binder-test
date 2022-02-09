import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.widgets import Slider, Button


# The parametrized function to be plotted
def land_func(t, sea_level, ret_part='peaks'):
    p1 = stats.norm.pdf(t, -0.5, 0.14)
    p2 = stats.norm.pdf(t, 0.2, 0.08)
    p3 = stats.norm.pdf(t, 0.75, 0.25)

    landscape = np.sum([p1, p2, p3], axis=0)

    peaks = np.where(landscape > sea_func(t, sea_level), landscape, np.nan)
    seabed = np.where(landscape < sea_func(t, sea_level), landscape, np.nan)

    if ret_part == 'peaks':
        return peaks
    elif ret_part == 'seabed':
        return seabed


def sea_func(t, sea_level):
    return np.sin(t * 50) / 18 + sea_level


x = np.linspace(-1, 1, 500)

# Define initial parameters
init_sea_level = 2

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
peaks_line, = plt.plot(x, land_func(x, init_sea_level), lw=3, color='green')
sea_line, = plt.plot(x, sea_func(x, init_sea_level), lw=2, color='blue')
seabed_line, = plt.plot(x, land_func(x, init_sea_level, ret_part='seabed'), lw=1, ls='--', color='darkgreen')

plt.fill_between(x, sea_func(x, init_sea_level), land_func(x, init_sea_level), color='lightgreen')
plt.fill_between(x, 0, sea_func(x, init_sea_level), color='lightblue')

# set the x and y lims
plt.ylim(0, 6)
plt.xlim(-1, 1)

# add labels
plt.ylabel("(VWM) Representation Strength")
plt.xlabel("Location")
plt.xticks(np.linspace(-0.8, 0.8, 6), ["Loc " + str(i) for i in range(1, 7)])
plt.yticks(np.linspace(0.6, 5.4, 2), ["Weak", "Strong"])

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25, bottom=0.2)

# Make a vertically oriented slider to control the amplitude
axsea = plt.axes([0.1, 0.2, 0.0225, 0.68])
sea_level_slider = Slider(
    ax=axsea,
    label="Action Threshold\n(sea level)",
    valmin=0,
    valmax=6,
    valinit=init_sea_level,
    valstep=0.1,
    orientation="vertical"
)


# The function to be called anytime a slider's value changes
def update(val):
    peaks_line.set_ydata(land_func(x, sea_level_slider.val))
    sea_line.set_ydata(sea_func(x, sea_level_slider.val))
    seabed_line.set_ydata(land_func(x, sea_level_slider.val, ret_part='seabed'))

    ax.fill_between(x, 0, 6, color='white')
    ax.fill_between(x, sea_func(x, sea_level_slider.val), land_func(x, sea_level_slider.val), color='lightgreen')
    ax.fill_between(x, 0, sea_func(x, sea_level_slider.val), color='lightblue')

    fig.canvas.draw_idle()


sea_level_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    sea_level_slider.reset()


button.on_clicked(reset)

plt.show()
