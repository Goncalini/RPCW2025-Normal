from rdflib import Namespace, Literal, URIRef, XSD, OWL, Graph, RDF, RDFS

n = Namespace("http://www.semanticweb.org/gonca/ontologies/2025/historia_teste/")
g = Graph()
g.parse("sapientia_ind.ttl", format="ttl")

estudaCom = URIRef(n.estudaCom)

g.add((estudaCom, RDF.type, OWL.ObjectProperty))
g.add((estudaCom, RDFS.domain, n.Aprendiz))
g.add((estudaCom, RDFS.range, n.Mestre))

q1 = """
CONSTRUCT {
  ?a :estudaCom ?m .
}
WHERE {
  ?a :aprende ?disc .
  ?m :ensina ?disc .
}
"""

result = g.query(q1)

insert_q = """
INSERT {
  ?a :estudaCom ?m .
}
WHERE {
  ?a :aprende ?disc .
  ?m :ensina ?disc .
}
"""

g.update(insert_q)


g.serialize(destination="sapientia_ind_estudaCom.ttl", format="ttl")
print(len(g))

# --------------------

g = Graph() # depois de rodar em cima
g.parse("sapientia_ind_estudaCom.ttl", format="ttl")

daBasesPara = URIRef(n.daBasesPara)

g.add((daBasesPara, RDF.type, OWL.ObjectProperty))
g.add((daBasesPara, RDFS.domain, n.Disciplina))
g.add((daBasesPara, RDFS.range, n.Aplicacao))

query = """
CONSTRUCT {
  ?disc :daBasesPara ?app .
}
WHERE {
  ?disc :eEstudadoEm ?conceito .
  ?conceito :temAplicacaoEm ?app .
}
"""

result = g.query(query)

#for r in result: 
#    print(r)

insert_query = """
INSERT {
  ?disc :daBasesPara ?app .
}
WHERE {
  ?disc :eEstudadoEm ?conceito .
  ?conceito :temAplicacaoEm ?app .
}
"""

g.update(insert_query)

g.serialize("sapientia_ind_daBases.ttl", format="ttl")
print(len(g))



