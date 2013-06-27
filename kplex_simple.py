import sys

def load_graph(file_name):
    graph_file = open(file_name, 'r')
    num_vertices = 0
    num_edges = 0
    edgelist = []
    for line in graph_file:
        u,v,w = [int(l) for l in line.strip().split(' ')]
        edgelist.append((u,v))
        if u > num_vertices:
            num_vertices = u
        if v > num_vertices:
            num_vertices = v
        num_edges += 1

    graph_file.close()


load_graph(sys.argv[1])
