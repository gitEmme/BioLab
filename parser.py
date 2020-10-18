# 2.10.2020
# Author: Martina Donadi
# This is a dummy class to allow get of specific pathway from the KEGG database through the REST api (http://rest.kegg.jp/)
# A parser function of the kgml file is available in the biopython package: https://github.com/biopython/biopython
# See https://www.genome.jp/kegg/xml/docs/ for kgml docs
# To connect to Neo4j browser interface go to http://localhost:7474/browser/
import requests
from Bio.KEGG.KGML.KGML_parser import Reaction,Relation,Graphics,Entry,Pathway,parse,read
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
db = GraphDatabase.driver(uri, auth= None)

def run_statement(db, stat):
    with db.session() as session:
        with session.begin_transaction() as tx:
            tx.run(stat)

def create_unique_labeled(db,n_type,name):
    n_type = n_type.capitalize()
    with db.session() as session:
        with session.begin_transaction() as tx:
            tx.run(f"MERGE (s:{n_type} {{name: '{name}'}})")

def delete_all(db):
    run_statement(db, "MATCH (n) DETACH DELETE n")


def getPathway(pathName) :
    try:
        response = requests.get('http://rest.kegg.jp/get/' + pathName + '/kgml')
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    pathway = read(response.text)
    return pathway

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth= None)

def create_labeled(d,name):
    with d.session() as session:
        with session.begin_transaction() as tx:
            tx.run("CREATE (s:Module {name: $name})", name=name)


pathway = getPathway('hsa00010')

delete_all(db)
# for key in pathway.entries:
        # Use vars() to print the properties of an object in python
        # properties of an Entry object: _id, _names, type, image, link, graphics, components, alt, _pathway, reactions
        
        # for graphic in pathway.entries[key].graphics:
        #     print(graphic.x)
        #     print(graphic.y)
        #     print(graphic.name) # the label of the graphic object
        # print(pathway.entries[key])
for reaction in pathway.reactions:
    # when the subtype element has attribute name with a directionality value like "activation" the interaction is from entry1 to entry2
    # properties of a Reaction object: _id, _names, type, _substrates, _products, _pathway
    print(reaction.id)
    # print(pathway.entries[reaction.id]._names)
    # print(pathway.entries[reaction.id].type)
    print(reaction.type)
    print(reaction.name)
    print(pathway.entries[reaction.id].name)
    create_unique_labeled(db,'Reaction', pathway.entries[reaction.id].name)
    # print(reaction.substrates[0].id, reaction.products[0].id)
    for substrate in reaction.substrates:
        print(pathway.entries[substrate.id].name)
        create_unique_labeled(db,pathway.entries[substrate.id].type + ":Substrate", pathway.entries[substrate.id].name)

    for product in reaction.products:
        print(pathway.entries[product.id].name)
        create_unique_labeled(db,pathway.entries[product.id].type + ":Product", pathway.entries[product.id].name)



    # print(pathway.entries[reaction.substrates[0].id].type, pathway.entries[reaction.products[0].id].type)
