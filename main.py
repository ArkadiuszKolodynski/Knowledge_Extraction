import rdflib
import nltk
from nltk.tag import StanfordNERTagger
from nltk.chunk import conlltags2tree
from SPARQLWrapper import SPARQLWrapper, JSON


FILENAME = 'request_data/file_1.ttl'
CLASSIFIER_PATH = 'stanford_ner/english.all.3class.distsim.crf.ser.gz'
NER_PATH = 'stanford_ner/stanford-ner.jar'


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
    # print(ne_chunked_sent, '\n')

    named_entities = []
    for tagged_tree in ne_chunked_sent:
        if hasattr(tagged_tree, 'label'):
            entity_name = ' '.join(c[0] for c in tagged_tree.leaves())
            entity_type = tagged_tree.label()
            named_entities.append((entity_name, entity_type))
    # print(named_entities, '\n')

    return [entity[0] for entity in named_entities]


def prepare_query(keyword):
    return """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>

        SELECT ?result WHERE {
            {
                ?result rdfs:label "$KEYWORD$"@en ;
                a dbo:Organisation .
            }
            UNION
            {
                ?result rdfs:label "$KEYWORD$"@en ;
                a dbo:Person .
            }
            UNION
            {
                ?result rdfs:label "$KEYWORD$"@en ;
                a dbo:Place .
            }
            UNION
            {
                ?altName rdfs:label "$KEYWORD$"@en ;
                dbo:wikiPageRedirects ?source .
                ?source rdf:type dbo:Organisation .
            }
            UNION
            {
                ?altName rdfs:label "$KEYWORD$"@en ;
                dbo:wikiPageRedirects ?source .
                ?source rdf:type dbo:Person .
            }
            UNION
            {
                ?altName rdfs:label "$KEYWORD$"@en ;
                dbo:wikiPageRedirects ?source .
                ?source rdf:type dbo:Place .
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
            return o


def get_entities_container(entities, sentence):
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


def main():
    g = rdflib.Graph()
    g.parse(FILENAME, format='n3')

    sentence = get_request_string(g)
    print('\nSent: ' + sentence + '\n')

    entities = get_entities(sentence)

    if len(entities):
        entity_container = get_entities_container(entities, sentence)

        for entity in entity_container:
            results = execute_query(entity)
            if entity.endswith('s') and results['results']['bindings'] == []:
                results = execute_query(entity[:-1])
            for result in results['results']['bindings']:
                if result != {} and result['result']['value']:
                    print(entity, result['result']['value'])

        # https://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html <= wynik wypisać do rdf'a
    else:
        print('No entities found!')


if __name__ == '__main__':
    main()
