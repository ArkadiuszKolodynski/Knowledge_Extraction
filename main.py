import rdflib
from rdflib import *
from rdflib.namespace import *
import nltk
from nltk.tag import StanfordNERTagger
from nltk.chunk import conlltags2tree
from SPARQLWrapper import SPARQLWrapper, JSON
from tkinter import filedialog
from tkinter import *

nltk.download('averaged_perceptron_tagger')


FILENAME = ""
CLASSIFIER_PATH = 'stanford_ner/english.all.3class.distsim.crf.ser.gz'
NER_PATH = 'stanford_ner/stanford-ner.jar'
top = Tk()
text = Text(top, height=32, width=80)

def filePath():
    global FILENAME
    FILENAME = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("ttl file", "*.ttl"), ("all files", "*.*")))
    f = open(FILENAME, "r")
    text.insert(END, f.read())


def stanford_ne_2_ibo(tagged_sent):
    bio_tagged_sent = []
    prev_tag = "O"
    for token, tag in tagged_sent:
        if tag == "O":  # O
            bio_tagged_sent.append((token, tag))
            prev_tag = tag
            continue
        if tag != "O" and prev_tag == "O":  # Begin NE
            bio_tagged_sent.append((token, "B-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag == tag:  # Inside NE
            bio_tagged_sent.append((token, "I-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag != tag:  # Adjacent NE
            bio_tagged_sent.append((token, "B-"+tag))
            prev_tag = tag

    return bio_tagged_sent


def stanford_ne_2_tree(ne_tagged_sent):
    bio_tagged_sent = stanford_ne_2_ibo(ne_tagged_sent)
    sent_tokens, sent_ne_tags = zip(*bio_tagged_sent)
    sent_pos_tags = [pos for token, pos in nltk.pos_tag(sent_tokens)]

    sent_conlltags = [(token, pos, ne) for token, pos, ne in zip(sent_tokens, sent_pos_tags, sent_ne_tags)]
    ne_tree = conlltags2tree(sent_conlltags)
    return ne_tree


def get_entities(sentence):
    sentence = nltk.word_tokenize(sentence)

    st = StanfordNERTagger(CLASSIFIER_PATH, NER_PATH, encoding='utf-8')
    ne_tagged_sent = st.tag(sentence)

    ne_chunked_sent = stanford_ne_2_tree(ne_tagged_sent)
    print(ne_chunked_sent, '\n')

    named_entities = []
    for tagged_tree in ne_chunked_sent:
        if hasattr(tagged_tree, 'label'):
            entity_name = ' '.join(c[0] for c in tagged_tree.leaves())
            entity_type = tagged_tree.label()
            named_entities.append((entity_name, entity_type))
    print(named_entities, '\n')

    return [entity[0] for entity in named_entities]


def prepare_query(keyword):
    return """
        SELECT ?result WHERE {
            {
                ?result rdfs:label "$KEYWORD$"@en ;
                a owl:Thing .       
            }
            UNION
            {
                ?altName rdfs:label "$KEYWORD$"@en ;
                dbo:wikiPageRedirects ?result .
            }
        }
    """.replace('$KEYWORD$', keyword)


def execute_query(keyword):
    sparql = SPARQLWrapper('http://dbpedia.org/sparql')
    sparql.setQuery(prepare_query(keyword))
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def get_request_string(graph):
    predicate = rdflib.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#isString')
    for s, p, o in graph:
        if p == predicate:
            return s, o


def prepare_entities_container(entities, sentence):
    entity_container = {}
    offset = 0
    for entity in entities:
        index = sentence.find(entity)
        sentence = sentence.replace(entity, '', 1)
        indexes_dict = {'beginIndex': index + offset, 'endIndex': index + offset + len(entity)}

        if entity in entity_container:
            entity_container[entity]['indexes'].append(indexes_dict)
        else:
            entity_container.update({entity: {'indexes': [indexes_dict]}})
        offset += len(entity)

    print('Found entities:', entities, '\n', entity_container, '\n')
    return entity_container


def create_graph(entity_container, m_referenceContext):
    g = Graph()
    namespace_manager = rdflib.namespace.NamespaceManager(g)

    nif = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
    namespace_manager.bind('nif', nif)

    aksw = Namespace("http://aksw.org/notInWiki/")
    namespace_manager.bind('aksw', aksw)

    dbr = Namespace("http://dbpedia.org/resource/")
    namespace_manager.bind('dbr', dbr)

    itsrdf = Namespace("http://www.w3.org/2005/11/its/rdf#")
    namespace_manager.bind('itsrdf', itsrdf)

    nonNegativeInteger = URIRef('http://www.w3.org/2001/XMLSchema#nonNegativeInteger')
    typeUri = URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')

    k = m_referenceContext.rfind("#")
    contextUrlWithoutHash = m_referenceContext[:k]

    # let's do some rock'n'roll
    for entity in entity_container:
        # get results
        results = execute_query(entity)
        if entity.endswith('s') and results['results']['bindings'] == []:
            results = execute_query(entity[:-1])

        m_anchor = entity

        for occur in entity_container[entity]['indexes']:
            m_beginIndex = occur['beginIndex']
            m_endIndex = occur['endIndex']
            m_byte = contextUrlWithoutHash + ("#char=%d,%d" % (m_beginIndex, m_endIndex))
            m_taIdentRef = ""

            # TODO relations here
            if not results['results']['bindings']:
                m_taIdentRef = 'http://aksw.org/notInWiki/' + "_".join(m_anchor.split(" "))
                
            else:
                for result in results['results']['bindings']:
                    if result != {} and result['result']['value']:
                        m_taIdentRef = result['result']['value']

            # assembly all
            byte = URIRef(m_byte)

            g.add( (byte, typeUri, nif.RFC5147String ) )
            g.add( (byte, typeUri, nif.Phrase ) )
            g.add( (byte, typeUri, nif.String ) )

            #idk other way
            g.add( (byte, URIRef("http://gerbil.aksw.org/eaglet/vocab#hasUserDecision"), URIRef("http://gerbil.aksw.org/eaglet/vocab#Added") ) )

            g.add( (byte, nif.anchorOf, Literal(m_anchor) ) )
            g.add( (byte, nif.beginIndex, Literal(m_beginIndex, datatype=nonNegativeInteger) ) )
            g.add( (byte, nif.endIndex, Literal(m_endIndex, datatype=nonNegativeInteger) ) )
            g.add( (byte, nif.referenceContext, URIRef(m_referenceContext) ) )

            g.add( (byte, itsrdf.taIdentRef, URIRef(m_taIdentRef) ) )

    # graph output
    print('Output graph \n')
    print(g.serialize(format='turtle').decode('utf-8'))

    return g

def run():
    g = rdflib.Graph()
    g.parse(data=text.get("1.0",END), format='n3')

    context, sentence = get_request_string(g)
    g.remove((context, None, None))

    print('\nSent: ' + sentence + '\n')

    entities = get_entities(sentence)

    if entities:
        entity_container = prepare_entities_container(entities, sentence)
        output_graph = create_graph(entity_container, context)

        # https://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html <= wynik wypisać do rdf'a
    else:
        print('No entities found!')


def main():


    top.title("Knowledge Extraction")
    top.geometry("590x660")
    B = Button(top, text="Wczytaj plik", command=filePath, height=2, width=80)
    B.place(x=10, y=550)
    Btn = Button(top, text="Zatwierdź", command=run, height=2, width=80)
    Btn.place(x=10, y=600)

    scrollbar = Scrollbar(top)
    scrollbar.pack(side=RIGHT, fill=Y)


    text.place(x=10, y=10)

    text.pack()

    text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text.yview)

    top.mainloop()


if __name__ == '__main__':
    main()
