#Necessary libraries for drawing the Co-occurrence network
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import colors

#Parameters necessary to build the network.
#Excel file
archivo_red="Example_Red.xlsx"
#vertices sheet
hoja_vertices='vertices'
#directed edges sheet
hoja_red="edges"
#Name for the figure of the network
Name='Example_Red'
date='march6'
# The vertices and edges of the network are read
archivo=pd.read_excel(archivo_red, sheet_name=hoja_vertices)
archivo2=pd.read_excel(archivo_red, sheet_name=hoja_red)
#Vertices and attributes
nombre_nodo=archivo['nombre'].values.tolist()
clave_nodo=archivo['clave'].values.tolist()
tama_nodo=archivo['IAR'].values.tolist()
tama_nodo_big=list(np.array(tama_nodo)*250)

#Edges and attributes
# In: means the species A passed first
entrada=archivo2['In'].values.tolist()
#Out: means species B passes in a period of time after A.
salida=archivo2['Out'].values.tolist()
edge_colors=archivo2['Day'].values.tolist()

#Network construction
RedMami=nx.DiGraph()
for k in range(0,len(nombre_nodo),1):
   RedMami.add_node(clave_nodo[k], nombre=nombre_nodo[k], IAR=tama_nodo[k])

for k in range(0,len(salida),1):
    RedMami.add_edge(salida[k], entrada[k], Color_Aristas=edge_colors[k])
# Detele vertices with IAR==0
remover=[]
for node in RedMami.nodes():
	if RedMami.nodes[node]['IAR']==0.0:
    	   remover.append(node)
RedMami.remove_nodes_from(remover)
#vertices atributes for drawing the network
#Vertices size
Tamano=nx.get_node_attributes(RedMami,'IAR')
tama_nodo=[Tamano.get(node) for node in RedMami.nodes()]
tama_nodo_big=list(np.array(tama_nodo)*250)
#Edges colors
color_arista=nx.get_edge_attributes(RedMami,'Color_Aristas')
C_arista=[color_arista.get(edge) for edge in RedMami.edges()]
#Vertices name
nombres_nodo=nx.get_node_attributes(RedMami,'nombre')
nombres=[nombres_nodo.get(node) for node in RedMami.nodes()]
labels=dict(zip(list(RedMami.nodes()),nombres))
#Network drawing 
fig = plt.figure()
#Vertices position for the example use Graphviz from de Networkx layouts
pos=nx.nx_agraph.graphviz_layout(RedMami)
nodes = nx.draw_networkx_nodes(RedMami, pos, node_size=tama_nodo_big, node_color='blue', alpha=0.2)
edges = nx.draw_networkx_edges(RedMami, pos, node_size=tama_nodo_big, arrowstyle='->', arrowsize=40, connectionstyle='arc3, rad=0.2', width=6, edge_color=C_arista, edge_cmap=plt.cm.cividis)
nx.draw_networkx_labels(RedMami,pos,labels,font_size=13,font_weight='bold')
pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.cividis)
pc.set_array([0,4,8,12,16,20])
plt.colorbar(pc, cax=None, ax=None)
ax = plt.gca()
ax.set_axis_off()
fig = mpl.pyplot.gcf()
fig.set_size_inches(14, 9)
#Saving network
plt.savefig(Name+date+'.png', bbox_inches='tight', pad_inches=2,dpi=300)
plt.close()
