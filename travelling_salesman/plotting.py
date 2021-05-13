import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


def plot_route(route, title=None) -> None:
    for i in range(len(route)):
        city = route[i]
        next_city = route[(i + 1) % len(route)]
        plt.scatter(city.x, city.y, c="red")
        plt.plot((city.x, next_city.x), (city.y, next_city.y), c="black")

    if title:
        plt.title(title)

    plt.show()
