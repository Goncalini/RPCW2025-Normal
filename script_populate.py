from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, XSD
import json
import csv
import os

g = Graph()
g.parse("sapientia_base.ttl", format="ttl")

n = Namespace("http://www.semanticweb.org/gonca/ontologies/2025/historia_teste/")

conceitoset = set()
disciplinaset = set()
mestreset = set()
obraset = set()
aplicacaoset = set()
periodoset = set()
tiposet = set()

with open("datasets/conceitos.json", "r", encoding="utf-8") as file:
    conceitos = json.load(file)

for conceito in conceitos["conceitos"]:
    conceitoURI = URIRef(f"{n}{conceito["nome"].replace(' ', '_')}")

    if conceitoURI not in conceitoset:
        g.add((conceitoURI, RDF.type, OWL.NamedIndividual))
    g.add((conceitoURI, RDF.type, n.Conceito))
    g.add((conceitoURI, n.nome, Literal(conceito["nome"], datatype=XSD.string)))
    conceitoset.add(conceitoURI)

    for app in conceito.get("aplicações", []):
        appURI = URIRef(f"{n}{app.replace(' ', '_')}")
        if appURI not in aplicacaoset:
            g.add((appURI, RDF.type, OWL.NamedIndividual))
            g.add((appURI, RDF.type, n.Aplicacao))
        g.add((appURI, n.nome, Literal(app, datatype=XSD.string)))
        aplicacaoset.add(appURI)
        g.add((conceitoURI, n.temAplicacaoEm, appURI))
    
    periodo = conceito.get("períodoHistórico")
    if periodo:
        periodoURI = URIRef(f"{n}{periodo.replace(' ', '_')}")
        if periodoURI not in periodoset:
            g.add((periodoURI, RDF.type, OWL.NamedIndividual))
            g.add((periodoURI, RDF.type, n.PeriodoHistorico))
        g.add((periodoURI, n.nome, Literal(periodo)))
        periodoset.add(periodoURI)
        g.add((conceitoURI, n.surgeEm, periodoURI))
    
    for rel in conceito.get("conceitosRelacionados", []):
        relURI = URIRef(f"{n}{rel.replace(' ', '_')}")
        if relURI not in conceitoset:
            g.add((relURI, RDF.type, OWL.NamedIndividual))
            g.add((relURI, RDF.type, n.Conceito))
        g.add((relURI, n.nome, Literal(rel, datatype=XSD.string)))
        conceitoset.add(relURI)
        g.add((conceitoURI, n.estaRelacionadoCom, relURI))


with open("datasets/disciplinas.json", "r", encoding="utf-8") as file:
    disciplinas = json.load(file)

for disc in disciplinas["disciplinas"]:
    nome = disc["nome"]
    discURI = URIRef(f"{n}{nome.replace(' ', '_')}")
    if discURI not in disciplinaset:
        g.add((discURI, RDF.type, OWL.NamedIndividual))
        g.add((discURI, RDF.type, n.Disciplina))
    g.add((discURI, n.nome, Literal(nome)))
    disciplinaset.add(discURI)

    for tipo in disc.get("tiposDeConhecimento", []):
        tipoURI = URIRef(f"{n}{tipo.replace(' ', '_')}")
        if tipoURI not in tiposet:
            g.add((tipoURI, RDF.type, OWL.NamedIndividual))
            g.add((tipoURI, RDF.type, n.TipoDeConhecimento))
        g.add((tipoURI, n.nome, Literal(tipo)))
        tiposet.add(tipoURI)
        g.add((discURI, n.pertenceA, tipoURI))
    
    for c in disc.get("conceitos", []):
        cURI = URIRef(f"{n}{c.replace(' ', '_')}")
        if cURI not in conceitoset:
            g.add((cURI, RDF.type, OWL.NamedIndividual))
            g.add((cURI, RDF.type, n.Conceito))
        g.add((cURI, n.nome, Literal(c)))
        conceitoset.add(cURI)
        g.add((cURI, n.eEstudadoEm, discURI))

with open("datasets/mestres.json", "r", encoding="utf-8") as file:
    mestres = json.load(file)

for mestre in mestres["mestres"]:
    nome = mestre["nome"]
    mestreURI = URIRef(f"{n}{nome.replace(' ', '_')}")
    if mestreURI not in mestreset:
        g.add((mestreURI, RDF.type, n.Mestre))
        g.add((mestreURI, RDF.type, OWL.NamedIndividual))
        g.add((mestreURI, n.nome, Literal(nome)))
        mestreset.add(mestreURI)
    # Período histórico
    periodo = mestre.get("períodoHistórico")
    if periodo:
        periodoURI = URIRef(f"{n}{periodo.replace(' ', '_')}")
        if periodoURI not in periodoset:
            g.add((periodoURI, RDF.type, n.PeríodoHistorico))
            g.add((periodoURI, RDF.type, OWL.NamedIndividual))
        g.add((periodoURI, n.nome, Literal(periodo)))
        periodoset.add(periodoURI)
        g.add((mestreURI, n.viveuEm, periodoURI))
    
    for disc in mestre.get("disciplinas", []):
        discURI = URIRef(f"{n}{disc.replace(' ', '_')}")
        if discURI not in disciplinaset:
            g.add((discURI, RDF.type, n.Disciplina))
            g.add((discURI, RDF.type, OWL.NamedIndividual))
        g.add((discURI, n.nome, Literal(disc)))
        disciplinaset.add(discURI)
        g.add((mestreURI, n.ensina, discURI))

with open("datasets/obras.json", "r", encoding="utf-8") as file:
    obras = json.load(file)

for obra in obras["obras"]:
    titulo = obra["titulo"]
    obraURI = URIRef(f"{n}{titulo.replace(' ', '_')}")
    if obraURI not in obraset:
        g.add((obraURI, RDF.type, n.Obra))
        g.add((obraURI, RDF.type, OWL.NamedIndividual))
    g.add((obraURI, n.titulo, Literal(titulo)))
    obraset.add(obraURI)

    autor = obra.get("autor")
    if autor:
        autorURI = URIRef(f"{n}{autor.replace(' ', '_')}")
        if autorURI not in mestreset:
            g.add((autorURI, RDF.type, n.Mestre))
            g.add((autorURI, RDF.type, OWL.NamedIndividual))
        g.add((autorURI, n.nome, Literal(autor)))
        mestreset.add(autorURI)
        g.add((obraURI, n.foiEscritoPor, autorURI))
    
    for c in obra.get("conceitos", []):
        cURI = URIRef(f"{n}{c.replace(' ', '_')}")
        if cURI not in conceitoset:
            g.add((cURI, RDF.type, n.Conceito))
            g.add((cURI, RDF.type, OWL.NamedIndividual))
        g.add((cURI, n.nome, Literal(c)))
        conceitoset.add(cURI)
        g.add((obraURI, n.explica, cURI))

with open("datasets/pg55944.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    for i, aprendiz in enumerate(data):
        aprendizURI = URIRef(f"{n}{aprendiz["nome"].replace(' ', '_')}_{i}")
        g.add((aprendizURI, RDF.type, n.Aprendiz))
        g.add((aprendizURI, n.nome, Literal(aprendiz["nome"], datatype=XSD.string)))
        g.add((aprendizURI, n.idade, Literal(aprendiz["idade"], datatype=XSD.integer)))
        for disc in aprendiz["disciplinas"]:
            discURI = URIRef(f"{n}{disc.replace(' ', '_')}")
            if discURI not in disciplinaset:
                g.add((discURI, RDF.type, n.Disciplina))
                g.add((discURI, RDF.type, OWL.NamedIndividual))
            g.add((discURI, n.nome, Literal(disc)))
            disciplinaset.add(discURI)
            g.add((aprendizURI, n.aprende, discURI))

g.serialize("sapientia_ind.ttl.", format="turtle")
print(len(g))