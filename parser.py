# 2.10.2020
# Author: Martina Donadi
# This is a dummy class to allow get of specific pathway from the KEGG database through the REST api (http://rest.kegg.jp/)
# A parser function of the kgml file is available in the biopython package: https://github.com/biopython/biopython
# See https://www.genome.jp/kegg/xml/docs/ for kgml docs
import requests
from Bio.KEGG.KGML.KGML_parser import Relation,Graphics,Entry,Pathway,parse,read

ENDC = '\033[m' # reset to the defaults
TGREEN =  '\033[32m' # Green Text
def getPathway(pathName) :
    try:
        response = requests.get('http://rest.kegg.jp/get/' + pathName + '/kgml')
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    pathway = read(response.text)
    return pathway

pathway = getPathway('hsa00010')

for key in pathway.entries:
        # Use vars() to print the properties of an object in python
        # properties of an Entry object: _id, _names, type, image, link, graphics, components, alt, _pathway, reactions
        
        # for graphic in pathway.entries[key].graphics:
        #     print(graphic.x)
        #     print(graphic.y)
        #     print(graphic.name) # the label of the graphic object
        print(pathway.entries[key])
for relation in pathway.relations:
    # when the subtype element has attribute name with a directionality value like "activation" the interaction is from entry1 to entry2
    print(relation.subtypes)
    print(relation.entry1._id, relation.entry2._id)
    print(relation.entry1._names, relation.entry2._names)