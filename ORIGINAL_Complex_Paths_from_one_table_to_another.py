                    ################################
                    #  To find all paths including #   
                    #  cyclic paths between two    #
                    #  nodes having multiple exit  #
                    #  points in a directed graph  #
                    ################################

import networkx as nx
import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '',
    database = 'test1'
    )

mycursor = mydb.cursor()

#mycursor.execute('SELECT Step_no,Next_Step,Org_code,Domain_code,Subdomain_code,Func_code FROM crmprocesssteps')
mycursor.execute('SELECT Step_no,Next_Step,Org_code,Domain_code,Subdomain_code,Step_Desc FROM pathtest1')
#List to store the nodes/vertices
node_list = []
edge_list = []
destinations = [] #exit point of a pair. We'll get the exit points here
for db in mycursor:
    a = list(db)
    node = str(a[0])
    exit_point = ''
    
    next_steps = a[1].split(',') #Next Step Column From Database

    if 'NULL' in next_steps:
        destinations.append(node)

    if 'NULL' not in next_steps:
        node_list.append(node)
        for i in next_steps:
            i = str(i)
            individual_edge = [] #Every initial and next step pair 
            individual_edge.extend([node,i])
            edge_list.append(tuple(individual_edge))
            


    org_code = a[2] #Value of Organisation Code
    domain_code = a[3] #Value of Domain Code
    subdomain_code = a[4] #Value of Subdomain Code
    #func_code = a[5] #Value of Function Code
    step_desc = a[5] #Value of Function Code

for i in  node_list:
    print('a',i)
for i in edge_list:    
    print('b',i)
print()    
for i in destinations:
    print('c',i)

    

#To initialize a directed graph G
G=nx.DiGraph()


#Add nodes to graph G
G.add_nodes_from(node_list)
#The graph has FOUR EXIT POINTS and TWO CYCLES
#Add edges 
G.add_edges_from(edge_list)

#print (G.nodes())
#print (G.edges())
#print (G.number_of_edges())
#print()
#print()

#List to determine whether exit point is single or multiple
exit_points = []
#Find all simple paths
simple_paths = []
#for path in nx.all_simple_paths(G, source=1000, target=99999):
    #print (path)
    #simple_paths.append(path)

#simple_paths.extend(list(nx.all_simple_paths(G, source=node_list[0], target=66666)))
#simple_paths.extend(list(nx.all_simple_paths(G, source=node_list[0], target=77777)))
#simple_paths.extend(list(nx.all_simple_paths(G, source=node_list[0], target=88888)))
#simple_paths.extend(list(nx.all_simple_paths(G, source=node_list[0], target=99999)))

for i in destinations:
    simple_paths.extend(list(nx.all_simple_paths(G, source=node_list[0], target=str(i))))

print('Total Simple Paths :',len(simple_paths))
'''
for i in simple_paths:
    #print(i)
    #print(i[-1])
    if i[-1] not in exit_points:
        exit_points.append(i[-1])
'''
print()
#print(exit_points)



#print(simple_paths)
print()

#Find all cycles in the graph
cycle_list = list(nx.simple_cycles(G))
#print (cycle_list)

#Algo to add cycles common to a non-cyclic path
all_paths = []
for path in simple_paths:
    all_paths.append(path)
    for node_A in path:
        for cycle in cycle_list:
            for node_B in cycle:
                if node_A == node_B:
                    #print (node_A,"->",path," Index:",path.index(node_A))
                    #print (path[:path.index(node_A)],cycle[cycle.index(node_B):],path[path.index(node_A):])
                    new_path = path[:path.index(node_A)]
                    new_path.extend(cycle[cycle.index(node_B):])
                    new_path.extend(path[path.index(node_A):])
                    all_paths.append(new_path)
                    #print (new_path)
                break;

print ("Total paths: ",len(all_paths))
#for path in all_paths:
    #print (path)


cyclic_paths = []
print('Total Cyclic Paths :',(len(all_paths)-len(simple_paths)))
for cyclic in all_paths:
    if cyclic not in simple_paths:
        print(cyclic)
        #print(cyclic[-1])
    #if i[-1] not in exit_points:
        #exit_points.append(i[-1])

print()
#print(exit_points)


path_code = 'PA00' #setting the string initials of path code
path_code_int = 0  #Initialising the path number

for i in all_paths: #i is the list of sequence of paths
    path_code_int += 1 #Incrementation of pathcode
    new_path_code = path_code + str(path_code_int) #New Pathcode
    #print(i)
    if i in simple_paths:
        for j in range(len(i)): #j is the individual path element in the path sequence
            sqlformula = "INSERT INTO crmpaths (Org_code,Domain_code,Subdomain_code,Func_code,Path_code,step_code,stepcodeseq,Straight_Paths,Cyclic_Paths) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            field_values = (org_code,domain_code,subdomain_code,func_code,new_path_code,str(i[j]),str(j+1),'YES','NO')
            mycursor.execute(sqlformula,field_values)
            mydb.commit()
    elif i not in simple_paths:
        for j in range(len(i)): #j is the individual path element in the path sequence
            sqlformula = "INSERT INTO crmpaths (Org_code,Domain_code,Subdomain_code,Func_code,Path_code,step_code,stepcodeseq,Straight_Paths,Cyclic_Paths) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            field_values = (org_code,domain_code,subdomain_code,func_code,new_path_code,str(i[j]),str(j+1),'NO','YES')
            mycursor.execute(sqlformula,field_values)
            mydb.commit()
    else:
        pass
        

