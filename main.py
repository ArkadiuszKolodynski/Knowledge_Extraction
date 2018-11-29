import rdflib
import re
import nltk
from SPARQLWrapper import SPARQLWrapper, JSON


REGEX = re.compile('[%s]' % re.escape('!@#$%^&*()_+=[]{}\|;:,.<>/?'))
FILENAME = 'docs/2'


def get_tokens(sentence):
    # rozbicie zapytania na tokeny
    sentence = nltk.word_tokenize(sentence)
    # usuniecie pozostalych znakow specjalnych
    sentence = [REGEX.sub('', word) for word in sentence if REGEX.sub('', word) != '']
    # part-of-speech tagger (interesuja nas tylko tagi NNP - 'noun, proper, singular')
    query = nltk.pos_tag(sentence)

    # MACHINE LEARNING do znajdowania entities w tekscie:
    # https://www.commonlounge.com/discussion/2662a77ddcde4102a16d5eb6fa2eff1e
    #
    # ne_chunked_sents = nltk.ne_chunk(query)
    # named_entities = []
    # for tagged_tree in ne_chunked_sents:
    #     if hasattr(tagged_tree, 'label'):
    #         entity_name = ' '.join(c[0] for c in tagged_tree.leaves())
    #         entity_type = tagged_tree.label()
    #         named_entities.append((entity_name, entity_type))
    # print(named_entities)

    return [word[0] for word in query if word[1] == 'NNP']


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


def main():
    sentence = open(FILENAME, 'r', encoding='utf=8').read()
    print('\nDoc: ' + sentence + '\n')

    container = {}
    offset = 0
    tokens = get_tokens(sentence)

    if len(tokens):
        for token in tokens:
            index = sentence.find(token)
            sentence = sentence.replace(token, '', 1)
            indexes_dict = {'beginIndex': index + offset, 'endIndex': index + offset + len(token)}
            if token in container:
                container[token]['indexes'].append(indexes_dict)
            else:
                container.update({token: {'indexes': [indexes_dict]}})
            offset += len(token)
        print('Found tokens: ', tokens)
        print(container)
        print()

        for token in container:
            results = execute_query(token)
            for result in results['results']['bindings']:
                if result != {} and result['result']['value']:
                    print(token, result['result']['value'])
    else:
        print('Tokens not found!')


if __name__ == '__main__':
    main()
