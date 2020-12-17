import matplotlib.pyplot as plt

from ether.core import Connection
from ether.scenarios.industrialiot import IndustrialIoTScenario
from ether.topology import Topology
from ether.vis import draw_basic

import srds
import random
from utils import save_topology


def main(seed: int, plot: bool):
    random.seed(seed)
    srds.seed(seed)

    topology = Topology()

    IndustrialIoTScenario(num_premises=3, internet="internet_chix").materialize(
        topology
    )
    IndustrialIoTScenario(num_premises=1, internet="internet_nyc").materialize(topology)

    topology.add_connection(Connection("internet_chix", "internet_nyc", 10))

    save_topology(topology, f"iiot.{seed}")

    if plot:
        draw_basic(topology)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        plt.show()  # display


if __name__ == "__main__":
    n_runs = 2
    for seed in range(n_runs):
        main(seed, n_runs == 1)
