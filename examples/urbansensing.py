import random
import matplotlib.pyplot as plt
from srds import ParameterizedDistribution
import srds

import ether.blocks.nodes as nodes
from ether.blocks.cells import (
    IoTComputeBox,
    Cloudlet,
    FiberToExchange,
    MobileConnection,
)
from ether.cell import SharedLinkCell, GeoCell
from ether.core import Node, Link
from ether.topology import Topology
from ether.vis import draw_basic

from utils import save_topology

lognorm = ParameterizedDistribution.lognorm


def node_name(obj):
    if isinstance(obj, Node):
        return obj.name
    elif isinstance(obj, Link):
        return f"link_{id(obj)}"
    else:
        return str(obj)


def main(seed: int, plot: bool):
    random.seed(seed)
    srds.seed(seed)

    topology = Topology()

    aot_node = IoTComputeBox(nodes=[nodes.rpi3, nodes.rpi3])
    neighborhood = lambda size: SharedLinkCell(
        nodes=[
            [aot_node] * size,
            IoTComputeBox([nodes.nuc] + ([nodes.tx2] * size * 2)),
        ],
        shared_bandwidth=500,
        backhaul=MobileConnection("internet_chix"),
    )
    city = GeoCell(5, nodes=[neighborhood], density=lognorm((0.82, 2.02)))
    cloudlet = Cloudlet(5, 2, backhaul=FiberToExchange("internet_chix"))

    topology.add(city)
    topology.add(cloudlet)

    save_topology(topology, f"urban_sensing.{seed}")

    if plot:
        draw_basic(topology)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        plt.show()  # display


if __name__ == "__main__":
    n_runs = 2
    for seed in range(n_runs):
        main(seed, n_runs == 1)
