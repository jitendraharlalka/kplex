import sys
import itertools
from collections import OrderedDict

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


    graph = [set() for i in range(num_vertices+1)] #+1 for 1 based indexing of vertices
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
    #print list(curr_plex)
    
    for v in curr_plex:
        peripherals |= graph[v]
    peripherals -= curr_plex
    
    #print list(peripherals)

    while True:
        n = len(curr_plex)+1    #+1 since we will be adding a peripheral vertex
        largest_common = n-k    #minimum necessary to be a kplex
        best_v = None
        for v in peripherals:
            common_count = len(curr_plex & graph[v])
            if common_count >= largest_common:
                largest_common = common_count
                best_v = v
        if best_v == None:  #the current kplex is maximal
            break

        peripherals.remove(best_v)
        curr_plex.add(best_v)
    
    #print
    #print list(curr_plex)
    #print list(peripherals)
    #print '------'
    
    return [list(curr_plex), list(peripherals)]

#gets all the kplexes in the graph
def get_all_kplex(graph, k):
    triangles = find_triangles(graph)
    kplexes=OrderedDict()
    while len(triangles) > 0:
        t = triangles.pop()
        [kplex, peripheral] = get_kplex(graph, t, k)
        kplex.sort()
        peripheral.sort()
        kplex = tuple(kplex)
        #peripheral = tuple(peripheral)
        kplexes.setdefault(kplex,set())
        kplexes[kplex]=kplexes[kplex].union(set(peripheral))
        
        #kplexes[kplex]=list(set(kplexes[kplex]))
        #kplexes.append(kplex)
        #peripherals.append(peripheral)
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
    return kplexes

#merges any kplexes with p percentage of common vertices 
#common wrt what? combined vertices? min set?
#for now min set
def merge_kplexes1(kplexes, p):
    mergedKplexes = OrderedDict()
    
    kplexCores=kplexes.keys()

    while len(kplexCores) > 0:
        k1 = kplexCores.pop()
        p1 = kplexes[k1]
        k1 = set(k1)
    
        usedCores = []
        usedPeriphery=[]

        counter=0
        for k2 in kplexCores:
            k2_set = set(k2)
            p2 = kplexes[k2]
            if len(k1&k2_set) > p*min(len(k1),len(k2)):
                k1 |= k2_set
                p1 |= p2
                usedCores.append(k2)
                usedPeriphery.append(p2)
            counter+=1


        for k in usedCores:
            del kplexes[k]
            kplexCores.remove(k)

        
        #for up in usedPeriphery:
        #    peripherals.remove(up)

        p1 -= k1
        k1 = list(k1)
        k1.sort()
        k1 = tuple(k1)
        
        p1 = list(p1)
        p1.sort()
        p1 = tuple(p1)
        mergedKplexes[k1]=p1
    
    return mergedKplexes

graph = load_graph(sys.argv[1])
kplexes = get_all_kplex(graph, 2)

# temp=open('temp.txt','w')
# for key in kplexes.keys():
#     temp.write('Cores:\n')
#     for v in key:
#         temp.write(str(v)+' ')
#     temp.write('\nPeripherals:\n')
#     for v in kplexes[key]:
#         temp.write(str(v)+' ')
#     temp.write('\n------------\n')
# temp.close()

mergedKplexes = merge_kplexes1(kplexes, 0.5)
# kplexes.sort()
# cores_merged.sort()

f = open("out.txt", 'w')
for key in mergedKplexes.keys():
    f.write('Cores:\n')
    for v in key:
        f.write(str(v)+' ')
    f.write('\nPeripherals:\n')
    for v in mergedKplexes[key]:
        f.write(str(v)+' ') 
    f.write('\n---------------\n')
f.close()