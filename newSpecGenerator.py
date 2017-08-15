import ontospy
from ontodocs.viz.viz_html_multi import *

class SpecGenerator():
    '''
    Generates specification from an ontology
    '''

    def __init__(self, rdf_path, output_path):
        RDFpath = rdf_path
        outputPath = "spec"

        # load current ontology from EthOn github
        g = ontospy.Ontospy(RDFpath)

        # invoke EthOn multi-HTML page visualizer
        v = KompleteViz(g, "EthOn: Ethereum Ontology", "paper")

        # build HTML
        v.build(outputPath)

def main():
    SpecGenerator(rdf_path="https://raw.githubusercontent.com/ConsenSys/EthOn/master/EthOn.rdf", output_path="spec")
    SpecGenerator(rdf_path="https://raw.githubusercontent.com/ConsenSys/EthOn/master/ERC20/EthOn_ERC20.rdf", output_path="spec/ERC20")
    SpecGenerator(rdf_path="https://raw.githubusercontent.com/ConsenSys/EthOn/master/Contracts/EthOn_Contracts.rdf", output_path="spec/Contracts")

main()
