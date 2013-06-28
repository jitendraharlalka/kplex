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
def get_kplex(graph, triangle, k):
    curr_plex = set(triangle)
    peripherals = set()
    for v in curr_plex:
        peripherals |= graph[v]
    peripherals -= curr_plex
    
    while True:
        n = len(curr_plex)+1    #+1 since we will be adding a peripheral vertex
        largest_common = n-k    #minimum necessary to be a kplex
        best_v = None
        for v in peripherals:
            common_count = len(curr_plex & graph[v])
            if common_count > largest_common:
                largest_common = common_count
                best_v = v
        if best_v == None:  #the current kplex is maximal
            break

        curr_plex.add(best_v)
        peripherals.remove(best_v)
    
    return curr_plex

#gets all the kplexes in the graph
def get_all_kplex(graph, k):
    triangles = find_triangles(graph)
    kplexes = set()
    while len(triangles) > 0:
        t = triangles.pop()
        kplex = list(get_kplex(graph, t, k))
        kplex.sort()
        kplex = tuple(kplex)
        kplexes.add(kplex)

        #here we remove triangles containing a vertex in the kplex to prevent duplicates
        #not sure what we should do about vertex belonging to multiple kplexes?
        #new_triangles = []
        #for t in triangles:
        #    is_valid = True
        #    for v in kplex:
        #        if v in t:
        #            is_valid = False
        #            break
        #    if is_valid:
        #        new_triangles.append(t)
        #
        #triangles = new_triangles

    
    return list(kplexes)

#merges any kplexes with p percentage of common vertices 
#common wrt what? combined vertices? min set?
#for now min set
def merge_kplexes1(kplexes, p):
    final_list = []
    while len(kplexes) > 0:
        k1 = set(kplexes.pop())
        used = []
        for k2 in kplexes:
            k2_set = set(k2)
            if len(k1&k2_set) > p*min(len(k1),len(k2)):
                k1 |= k2_set
                used.append(k2)
        
        for k in used:
            kplexes.remove(k)
        k1 = list(k1)
        k1.sort()
        k1 = tuple(k1)
        final_list.append(k1)
    
    return final_list

graph = load_graph(sys.argv[1])
kplexes = get_all_kplex(graph, 2)
kplex_merged = merge_kplexes1(kplexes[:], 0.5)
kplexes.sort()
kplex_merged.sort()

f = open("out.txt", 'w')
for k in kplex_merged:
    for v in k:
        f.write(str(v)+' ')
    f.write('\n')
f.close()
