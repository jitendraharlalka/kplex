import sys
import itertools

#creat graph adj list from file
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

    
    graph = [set() for i in range(num_vertices+1)]  #+1 for 1 based indexing of vertices
    for e in edgelist:
        u,v = e
        graph[u].add(v)
        graph[v].add(u)
    return graph


#find all 3-cliques in a graph
def find_triangles(graph):
    triangles = []
    done_vertices = set()
    for v in range(1,len(graph)):
        Nv = list(graph[v]-done_vertices)
        if len(Nv) < 2: #no triangle containing this vertex
            continue
        for pair in list(itertools.combinations(Nv,2)):
            if pair[0] in graph[pair[1]]:
                triangle = list(pair)+[v]
                triangle.sort()
                triangles.append(triangle)

        done_vertices.add(v)
    return triangles       


#finds the best kplex for a triangle (3-clique)
def get_kplex(graph, triangle):
    print(triangle)
    curr_core = set(triangle)
    peripherals = set()
    for v in curr_core:
        peripherals |= graph[v]
    peripherals -= curr_core
    
    while True:
        break
    
    print(peripherals)


graph = load_graph(sys.argv[1])
triangles = find_triangles(graph)
triangle = triangles[0]
get_kplex(graph, triangle)
