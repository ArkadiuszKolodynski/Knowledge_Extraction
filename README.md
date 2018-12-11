# Knowledge_Extraction

TODO:

dodac do grafu takie tuple [przykladowe dla pierwszego pliku - file_1.ttl] (za pomocą funkcji add() np.

`g.add((rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=67,79'), rdflib.term.URIRef('http://www.w3.org/2005/11/its/rdf#taIdentRef'), rdflib.term.URIRef('http://aksw.org/notInWiki/James_Damore')))` )

`(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=67,79'), rdflib.term.URIRef('http://www.w3.org/2005/11/its/rdf#taIdentRef'), rdflib.term.URIRef('http://aksw.org/notInWiki/James_Damore'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=67,79'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#endIndex'), rdflib.term.Literal('79', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#nonNegativeInteger')))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=67,79'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#anchorOf'), rdflib.term.Literal('James Damore'))
(rdflib.term.BNode('ub1bL58C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#object'), rdflib.term.URIRef('http://dbpedia.org/resource/Google'))
(rdflib.term.BNode('ub1bL58C1'), rdflib.term.URIRef('http://www.w3.org/ns/oa#hasTarget'), rdflib.term.BNode('ub1bL62C18'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=0,6'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#Phrase'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=0,6'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#RFC5147String'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=0,6'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#String'))
(rdflib.term.BNode('ub1bL49C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://www.w3.org/ns/oa#Annotation'))
(rdflib.term.BNode('ub1bL58C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=11,24'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#anchorOf'), rdflib.term.Literal('Sundar Pichai'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=11,24'), rdflib.term.URIRef('http://gerbil.aksw.org/eaglet/vocab#hasUserDecision'), rdflib.term.URIRef('http://gerbil.aksw.org/eaglet/vocab#Added'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=11,24'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#RFC5147String'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=11,24'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#referenceContext'), rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=0,131'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=67,79'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#beginIndex'), rdflib.term.Literal('67', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#nonNegativeInteger')))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=0,6'), rdflib.term.URIRef('http://www.w3.org/2005/11/its/rdf#taIdentRef'), rdflib.term.URIRef('http://dbpedia.org/resource/Google'))
(rdflib.term.BNode('ub1bL49C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate'), rdflib.term.URIRef('http://dbpedia.org/ontology/employer'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=67,79'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#referenceContext'), rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=0,131'))
(rdflib.term.BNode('ub1bL58C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate'), rdflib.term.URIRef('http://dbpedia.org/ontology/employer'))
(rdflib.term.BNode('ub1bL49C1'), rdflib.term.URIRef('http://www.w3.org/ns/oa#hasTarget'), rdflib.term.BNode('ub1bL53C18'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=11,24'), rdflib.term.URIRef('http://www.w3.org/2005/11/its/rdf#taIdentRef'), rdflib.term.URIRef('http://dbpedia.org/resource/Sundar_Pichai'))
(rdflib.term.BNode('ub1bL40C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement'))
(rdflib.term.BNode('ub1bL44C18'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://www.w3.org/ns/oa#SpecificResource'))
(rdflib.term.BNode('ub1bL44C18'), rdflib.term.URIRef('http://www.w3.org/ns/oa#hasSource'), rdflib.term.URIRef('http://www.india.com/travel/agra/#char=0,80'))
(rdflib.term.BNode('ub1bL49C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#object'), rdflib.term.URIRef('http://dbpedia.org/resource/Google'))
(rdflib.term.BNode('ub1bL58C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#subject'), rdflib.term.URIRef('http://dbpedia.org/resource/Sundar_Pichai'))
(rdflib.term.BNode('ub1bL62C18'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://www.w3.org/ns/oa#SpecificResource'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=67,79'), rdflib.term.URIRef('http://gerbil.aksw.org/eaglet/vocab#hasUserDecision'), rdflib.term.URIRef('http://gerbil.aksw.org/eaglet/vocab#Added'))
(rdflib.term.BNode('ub1bL40C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate'), rdflib.term.URIRef('http://dbpedia.org/ontology/CEO'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=67,79'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#String'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=11,24'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#endIndex'), rdflib.term.Literal('24', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#nonNegativeInteger')))
(rdflib.term.BNode('ub1bL40C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://www.w3.org/ns/oa#Annotation'))
(rdflib.term.BNode('ub1bL40C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#subject'), rdflib.term.URIRef('http://dbpedia.org/resource/Google'))
(rdflib.term.BNode('ub1bL53C18'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://www.w3.org/ns/oa#SpecificResource'))
(rdflib.term.BNode('ub1bL62C18'), rdflib.term.URIRef('http://www.w3.org/ns/oa#hasSource'), rdflib.term.URIRef('http://www.india.com/travel/agra/#char=0,80'))
(rdflib.term.BNode('ub1bL49C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=11,24'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#Phrase'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=0,6'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#beginIndex'), rdflib.term.Literal('0', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#nonNegativeInteger')))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=11,24'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#String'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=0,6'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#endIndex'), rdflib.term.Literal('6', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#nonNegativeInteger')))
(rdflib.term.BNode('ub1bL53C18'), rdflib.term.URIRef('http://www.w3.org/ns/oa#hasSource'), rdflib.term.URIRef('http://www.india.com/travel/agra/#char=0,80'))
(rdflib.term.BNode('ub1bL49C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#subject'), rdflib.term.URIRef('http://aksw.org/notInWiki/James_Damore'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=0,6'), rdflib.term.URIRef('http://gerbil.aksw.org/eaglet/vocab#hasUserDecision'), rdflib.term.URIRef('http://gerbil.aksw.org/eaglet/vocab#Added'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=0,6'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#anchorOf'), rdflib.term.Literal('Google'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=0,6'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#referenceContext'), rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=0,131'))
(rdflib.term.BNode('ub1bL40C1'), rdflib.term.URIRef('http://www.w3.org/ns/oa#hasTarget'), rdflib.term.BNode('ub1bL44C18'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=67,79'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#RFC5147String'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=11,24'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#beginIndex'), rdflib.term.Literal('11', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#nonNegativeInteger')))
(rdflib.term.BNode('ub1bL58C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://www.w3.org/ns/oa#Annotation'))
(rdflib.term.URIRef('https://www.theverge.com/2018/1/19/16911482/james-damore-google-ceo-sundar-pichai-women-in-tech-memo-firing#char=67,79'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#Phrase'))
(rdflib.term.BNode('ub1bL40C1'), rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#object'), rdflib.term.URIRef('http://dbpedia.org/resource/Sundar_Pichai'))`

wypisac ten graf do pliku za pomoca funkcji serialize() np.

`file = open('result.ttl', 'w')`

`file.write(g.serialize(format='turtle'))`

Tworzenie bnodow i urirfsow:
https://rdflib.readthedocs.io/en/stable/rdf_terms.html
