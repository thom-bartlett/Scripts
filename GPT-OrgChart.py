import csv
import pygraphviz as pgv

# Read CSV data and create a dictionary of employees and their managers
org_data = {}
with open('org_data.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        employee = row['Employee']
        manager = row['Manager']
        if manager not in org_data:
            org_data[manager] = []
        org_data[manager].append(employee)

# Create a directed graph
org_graph = pgv.AGraph(directed=True)

# Recursively add nodes and edges to the graph
def add_nodes_and_edges(manager, graph):
    if manager in org_data:
        for employee in org_data[manager]:
            graph.add_node(employee)
            graph.add_edge(manager, employee)
            add_nodes_and_edges(employee, graph)

# Add the root nodes (top-level managers) to the graph
root_managers = [manager for manager in org_data.keys() if manager not in sum(org_data.values(), [])]
for root_manager in root_managers:
    org_graph.add_node(root_manager)
    add_nodes_and_edges(root_manager, org_graph)

# Visualize the org chart
output_file = "org_chart.png"
org_graph.layout(prog='dot')  # You can choose different layout algorithms
org_graph.draw(output_file)
print(f"Org chart saved as {output_file}")