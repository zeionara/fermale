import matplotlib.pyplot as plt


def draw_plot(x, y, x_label: str = None, y_label: str = None, title: str = None, path: str = None):
    plt.plot(x, y)
    if title is not None:
        plt.title(title)
    if x_label is not None:
        plt.xlabel(x_label)
    if y_label is not None:
        plt.ylabel(y_label)
    if path is None:
        plt.show()
    else:
        plt.savefig(path)
