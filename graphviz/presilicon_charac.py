
import graphviz

g = graphviz.Digraph('G', filename='presilicon.gv')

g.edge('Cloud Workloads Characterization using\nPre silicon information\nand Clustering',\
'L. Eeckhout, H. Vandierendonck and K. De Bosschere, \n"Designing computer \
architecture research workloads," in Computer, vol. 36, no. 2, pp. 65-71, \
Feb. 2003, doi: 10.1109/MC.2003.1178050')

g.edge('Cloud Workloads Characterization using\nPre silicon information\nand Clustering',\
'R.T. Cheveresan, S. Holban., "Workload Characterization an Essential Step \nin \
Computer Systems Performance Analysis - Methodology and Tools," Advances in \nElectrical \
and Computer Engineering, vol.9, no.3, pp.100-106, 2009, doi:10.4316/AECE.2009.03018')

g.edge('Cloud Workloads Characterization using\nPre silicon information\nand Clustering',\
'K. Rupnow, A. Rodrigues, K. Underwood, and K. Compton, \n Scientific applications \
vs. spec-fp: A comparison of program behavior')
g.view()
