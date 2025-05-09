import networkx as nx
import sys
from collections import defaultdict
import matplotlib.pyplot as plt


class SDNController:

    # Initialize values
    def __init__(self):
        # Keeps track of the visual topology
        self.topology = nx.Graph()

        # Keeps track of the different flows in a list
        self.flow_table = defaultdict(list)

        # Keeps track of the failed links in a set
        self.failed_links = set()

    # Function to add a new node
    # Adds the node to the topology
    def add_node(self, node):
        self.topology.add_node(node)
        print(f'Added node: {node}')

    # Function to remove a node
    # Removes the node from the topology if it exists within it
    def remove_node(self, node):
        if node in self.topology:
            self.topology.remove_node(node)
            print(f'Removed node: {node}')
        else:
            print(f'Node {node} does not exist')

    # Function to add a link between nodes
    def add_link(self, src, dst, weight=1):

        # Call add_edge from Graph class to add an undirected edge between two defined
        # nodes along with the weight
        self.topology.add_edge(src, dst, weight=weight)

        # Handle output
        print(f'Added link: {src} - {dst} with weight {weight}')

    # Function to remove a link between nodes
    def remove_link(self, src, dst):

        # If an edge exists between two nodes:
        if self.topology.has_edge(src, dst):

            # Call remove_edge from Graph class to remove it
            self.topology.remove_edge(src, dst)

            # Handle output
            print(f'Removed link: {src} - {dst}')
        else:
            print(f'Link {src} - {dst} does not exist')

    # Function to compute the shortest path
    def compute_shortest_path(self, src, dst):
        try:
            # Call shortest_path function to use Dijkstra's algorithm to compute
            path = nx.shortest_path(self.topology, source=src, target=dst, weight='weight')

            # Handle output
            print(f'Shortest path from {src} to {dst}: {path}')
            return path
        except nx.NetworkXNoPath:
            print(f'No path between {src} and {dst}')
            return []

    # Function to visualize graph
    def visualize_topology(self):
        plt.figure(figsize=(8, 8))
        pos = nx.spring_layout(self.topology)
        nx.draw(self.topology, pos, with_labels=True, node_size=2000, font_size=15, font_weight='bold')
        edge_labels = nx.get_edge_attributes(self.topology, 'weight')
        nx.draw_networkx_edge_labels(self.topology, pos, edge_labels=edge_labels)
        plt.title('Network Topology')
        plt.show()

    # Function to generate a flow table
    def generate_flow_table(self, src, dst):

        # Get and output the shortest path
        path = self.compute_shortest_path(src, dst)

        # Error handling
        if not path:
            print("Invalid path for flow")
            return

        for i in range(len(path) - 1):

            # Initialize the list if the key does not exist
            if path[i] not in self.flow_table:
                self.flow_table[path[i]] = []

            # Append the next hop and the final destination
            self.flow_table[path[i]].append((path[i + 1], dst))
            print(f"Flow table generated for {src} -> {dst}: {dict(self.flow_table)}")

    # Function to simulate a link failure
    def sim_link_fail(self, src, dst):

        # If an edge exists between the src and dst, remove the link and add it to the
        # failed_links set
        if self.topology.has_edge(src, dst):
            self.failed_links.add((src, dst))
            self.remove_link(src, dst)

        # Handle output
            print(f"Link failure at: {src} - {dst}")
        else:
            print(f"link {src} - {dst} does not exist")

    # Function used to reconfigure the routes after a link failure
    def reconfigure_routes(self):

        # For each flow table entry:
        for src, entries in list(self.flow_table.items()):

            # For each next_hop and dst:
            for next_hop, dst in entries:

                # Check for link failure
                if (src, next_hop) in self.failed_links or (next_hop, src) in self.failed_links:
                    print(f"Reconfiguring route for broken link: {src} - {next_hop}")

                    # Recompute the shortest path
                    new_path = self.compute_shortest_path(src, dst)

                    # Update the table
                    if new_path:
                        self.flow_table[src] = [(new_path[1], dst)]
                        print(f"Updated flow table for {src} -> {dst}: {self.flow_table[src]}")
                    else:
                        print(f"No alternative path from {src} to {dst}")

    # Help function to display commands
    def print_help(self):
        print("         add_node {NODE}")
        print("         add_link {NODE} {NODE} {WEIGHT - INTEGER}")
        print("         remove_node {NODE}")
        print("         remove_link {NODE} {NODE}")
        print("         path {NODE} {NODE}")
        print("         show")
        print("         flow {NODE} {NODE}")
        print("         fail_link {NODE} {NODE}")
        print("         reconfigure")
        print("         exit")


controller = SDNController()


print('Enter "help" for list of commands')


# Function to create command line interface and handle input

# HASH: e045f215655df5b881c2f2222f3076386b0a5411b55de6473ca0c6c07084eb2c

def cli():
    while True:
        cmd = input("SDN> ").strip().split()
        if not cmd:
            continue
        if cmd[0] == 'add_node' and len(cmd) == 2:
            controller.add_node(cmd[1].upper())
        elif cmd[0] == 'add_link' and len(cmd) == 4:
            controller.add_link(cmd[1].upper(), cmd[2].upper(), int(cmd[3]))
        elif cmd[0] == 'remove_node' and len(cmd) == 2:
            controller.remove_node(cmd[1].upper())
        elif cmd[0] == 'remove_link' and len(cmd) == 3:
            controller.remove_link(cmd[1].upper(), cmd[2].upper())
        elif cmd[0] == 'path' and len(cmd) == 3:
            controller.compute_shortest_path(cmd[1].upper(), cmd[2].upper())
        elif cmd[0] == 'show':
            controller.visualize_topology()
        elif cmd[0] == 'flow' and len(cmd) == 3:
            controller.generate_flow_table(cmd[1].upper(), cmd[2].upper())
        elif cmd[0] == 'fail_link' and len(cmd) == 3:
            controller.sim_link_fail(cmd[1].upper(), cmd[2].upper())
        elif cmd[0] == 'reconfigure':
            controller.reconfigure_routes()
        elif cmd[0] == 'help':
            controller.print_help()
        elif cmd[0] == 'exit':
            sys.exit(0)
        else:
            print("Unknown command")


# Call cli
cli()

