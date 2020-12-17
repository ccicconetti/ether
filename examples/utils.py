from ether.core import Node, Link
from ether.topology import Topology

import networkx as nx


def save_topology(topology, path):
    V = len(topology.get_nodes())
    E = len(topology.get_links())

    with open(f"{path}.graph", "wb") as outfile:
        nx.write_adjlist(topology, outfile, delimiter=";")

    getname = (
        lambda x: x.name
        if isinstance(x, Node)
        else x.tags["name"]
        if isinstance(x, Link)
        else x
    )

    with open(f"{path}.edges", "w") as outfile:
        G = nx.convert.to_dict_of_dicts(topology)
        for v, edges in G.items():
            outfile.write(f"{getname(v)}")
            for e in edges:
                outfile.write(f" {getname(e)}")
            outfile.write("\n")

    with open(f"{path}.nodes", "w") as outfile:
        for i, v in zip(range(V), topology.get_nodes()):
            outfile.write(
                (
                    f"{i};{v.name};{v.capacity.memory};{v.capacity.cpu_millis};{v.arch};"
                    f"{v.labels['ether.edgerun.io/type']};"
                    f"{v.labels['ether.edgerun.io/model']}\n"
                )
            )

    with open(f"{path}.links", "w") as outfile:
        for i, e in zip(range(E), topology.get_links()):
            outfile.write(f"{i};{e.bandwidth};{e.tags['name']};{e.tags['type']}\n")
