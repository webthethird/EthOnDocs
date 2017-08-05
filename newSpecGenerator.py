import ontospy
from ontodocs.viz.viz_html_multi import *

RDFpath = "https://raw.githubusercontent.com/ConsenSys/EthOn/master/EthOn.rdf"
outputPath = "EthOnHTML"

# load current ontology from EthOn github
g = ontospy.Ontospy(RDFpath)

# invoke EthOn multi-HTML page visualizer
v = KompleteViz(g, "EthOn: Ethereum Ontology", "paper")

# build HTML
v.build(outputPath)
