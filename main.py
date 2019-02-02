import rdflib
from rdflib import *
from rdflib.namespace import *
import nltk
from nltk.tag import StanfordNERTagger
from nltk.chunk import conlltags2tree
from SPARQLWrapper import SPARQLWrapper, JSON
from tkinter import filedialog
from tkinter import *
from nltk.sem import relextract
import collections
import threading

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

FILENAME = ""
CLASSIFIER_PATH = 'stanford_ner/english.all.3class.distsim.crf.ser.gz'
NER_PATH = 'stanford_ner/stanford-ner.jar'
top = Tk()
Btn = None
inputText = Text(top, height=16, width=80)
outputText = Text(top, height=16, width=80)

# Function used for own relation extractions

from six.moves import html_entities
def descape_entity(m, defs=html_entities.entitydefs):
    """
    Translate one entity to its ISO Latin value.
    Inspired by example from effbot.org
    """
    try:
        return defs[m.group(1)]

    except KeyError:
        return m.group(0)  # use as is

def list2sym(lst):
    """
    Convert a list of strings into a canonical symbol.
    :type lst: list
    :return: a Unicode string without whitespace
    :rtype: unicode
    """
    sym = _join(lst, '_', untag=True)
    sym = sym.lower()
    ENT = re.compile("&(\w+?);")
    sym = ENT.sub(descape_entity, sym)
    sym = sym.replace('.', '')
    return sym

def _join(lst, sep=' ', untag=False):
    """
    Join a list into a string, turning tags tuples into tag strings or just words.
    :param untag: if ``True``, omit the tag from tagged input strings.
    :type lst: list
    :rtype: str
    """
    try:
        return sep.join(lst)
    except TypeError:
        if untag:
            return sep.join(tup[0] for tup in lst)
        from nltk.tag import tuple2str

        return sep.join(tuple2str(tup) for tup in lst)

def rel2dict(pairs):

    result = []
    for x in range(0, len(pairs)):
        for y in range(x, len(pairs)):
            if y == x:
                continue

            subject = ' '.join(c[0] for c in pairs[x][1].leaves())

            predicate = []
            if x < y:
                predicate = pairs[y][0]
            else:
                predicate = pairs[x][0]

            obj = ' '.join(c[0] for c in pairs[y][1].leaves())

            result.append((subject, predicate, obj))
    return result

def getGrammarRelations(tree):
    pairs = relextract.tree2semi_rel(tree)
    reldicts = rel2dict(pairs)
    return reldicts

# // Function used for own relation extractions

def filePath():
    """Method used to get a file path"""

    global FILENAME
    top.update()

    FILENAME = filedialog.askopenfilename(parent=top, initialdir="/", title="Select file",
                                          filetypes=(("ttl file", "*.ttl"), ("all files", "*.*")))

    if len(FILENAME) > 0:
        inputText.delete('1.0', END)
        outputText.delete('1.0', END)
        f = open(FILENAME, 'r', encoding='utf-8')
        inputText.insert(END, f.read())
        Btn.config(state="normal")


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
    """Method used to get entities from sentence

        Parameters
        ----------
        sentence : str
            phrase with sentence
      
        Returns
        -------
        named_entities : list
            list of named entities
        """
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

    grammarRelations = getGrammarRelations(ne_chunked_sent)

    return (named_entities, grammarRelations)

def prepare_query_relation(res1, res2):
    return """
        SELECT ?verb1 WHERE {
            <%s> ?verb1 <%s>.
        }
    """ % (res1, res2)

# target => ("label", "type", ?)
# others => [("label", "type", "url"), ("label", "type", "url")]
def getBlock(target, others):

    # ID, LABEL, TYPE
    # ID => "entity_name" (without question mark)
    unknown_entity_template = """
        ?$ID$ rdfs:label ?label_$ID$ .
        ?$ID$ a owl:Thing, dbo:$TYPE$ .  

        filter strStarts(?label_$ID$, "$LABEL$")  
        filter (lang(?label_$ID$) = 'en')
    """

    # LEFT, REL_ID, RIGHT
    # LEFT, RIGHT => "?ent_$ID$" or "<$URL$>"
    raw_relation_template = """
       $LEFT$ ?rel_$REL_ID$ $RIGHT$ .
    """

    entire_query = ""

    print(target)
    print(others)

    # result template
    entire_query += unknown_entity_template.replace('$ID$', "result").replace('$TYPE$', target[1]).replace('$LABEL$', target[0])

    # add unknowns
    for ent_i, (label, dbotype, url) in enumerate(others):
        if not url:
            entire_query += unknown_entity_template.replace('$ID$', "ent_%s" % ent_i).replace('$TYPE$', dbotype).replace('$LABEL$', label)

    # add relations
    rel_i = 1

    # target relations
    for ent_i, (label, dbotype, url) in enumerate(others):
        if not url:
            entire_query += raw_relation_template.replace('$LEFT$', "?result").replace('$REL_ID$', str(ent_i)).replace('$RIGHT$', "?ent_%s" % ent_i)
        else:
            entire_query += raw_relation_template.replace('$LEFT$', "?result").replace('$REL_ID$', str(ent_i)).replace('$RIGHT$', "<%s>" % url)

        rel_i += 1

    # multi others relations
    for left_i in range(len(others)):
        (label_left, dbotype_left, url_left) = others[left_i]

        for right_i in range(left_i + 1, len(others)):
            (label_right, dbotype_right, url_right) = others[right_i]

            part = raw_relation_template.replace('$REL_ID$', str(rel_i))

            if url_left:
                part = part.replace('$LEFT$', "<%s>" % url_left)
            else:
                part = part.replace('$LEFT$', "?ent_%s" % left_i)

            if url_right:
                part = part.replace('$RIGHT$', "<%s>" % url_right)
            else:
                part = part.replace('$RIGHT$', "?ent_%s" % right_i)

            entire_query += part
            rel_i += 1

    return entire_query

# target => ("label", "type", ?)
def first_query(target):
    query = """
        { 
            ?result rdfs:label "$LABEL$"@en ;
            a owl:Thing, dbo:$TYPE$ .  
        }
    """

    return query.replace('$LABEL$', target[0]).replace('$TYPE$', target[1])

# target => ("label", "type", ?)
def fallback_query(target):
    query = """
        UNION { 
            ?altName rdfs:label "$LABEL$"@en ;	
            dbo:wikiPageRedirects ?result .	
        }
    """

    return query.replace('$LABEL$', target[0]).replace('$TYPE$', target[1])

def generateSmallerBlocks(target, others):
    query = ""

    if not others:
        return query

    for id in range(0, len(others)):
        query += "UNION {"
        query += getBlock(target, [others[id]])
        query += "}"

    return query

# entities => [("label", "type", "url"), ("label", "type", "url")]
def resolve_entity(target, others):
    query = "SELECT DISTINCT ?result WHERE {"

    #query += getBlock(target, others)
    query += first_query(target)
    query += generateSmallerBlocks(target, others)
    query += fallback_query(target)

    query += "} LIMIT 1"

    # push
    sparql = SPARQLWrapper('http://dbpedia.org/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    if results['results']['bindings']:
        return results['results']['bindings'][0]['result']['value']
    else:
        return ""


def execute_query(label, dbotype):
    
    query = """
        SELECT DISTINCT ?result WHERE {
            {
                ?result rdfs:label "$KEYWORD$"@en ;
                a owl:Thing, dbo:$TYPE$ .  
            }
            UNION	
            {	
                ?altName rdfs:label "$KEYWORD$"@en ;	
                dbo:wikiPageRedirects ?result .	
            }
            UNION
            {
                ?result rdfs:label ?label ;
                a owl:Thing, dbo:$TYPE$ .   

                ?altName rdfs:label ?label2 .
                ?altName dbo:artist ?result ;
                a owl:Thing .     
 
                filter strStarts(?label2, "$KEYWORD$")  
                filter (lang(?label2) = 'en')
            }
        }
        LIMIT 1
    """.replace('$KEYWORD$', label).replace('$TYPE$', dbotype)

    sparql = SPARQLWrapper('http://dbpedia.org/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    return sparql.query().convert()

def execute_query_relation(query):
    sparql = SPARQLWrapper('http://dbpedia.org/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    return sparql.query().convert()

def get_request_string(graph):
    """Method used to get request string
              Parameters
              ----------
              graph : Graph
                  graph 

              Returns
              -------
              entities : list
                    list of entities
              sentence : rdflib.term.Literal
                    sentence from triple
              """
    predicate = rdflib.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#isString')
    for s, p, o in graph:
        if p == predicate:
            return s, o

def getBytesToRelation(label, dbotype):
    query = """
        SELECT DISTINCT ?result WHERE {
            ?result rdfs:label ?label ;
            a owl:Thing, dbo:%s .     

            filter strStarts(?label, "%s")  
            filter (lang(?label) = 'en')
        }
        LIMIT 3
    """ % (dbotype, label)

    print(query)

    sparql = SPARQLWrapper('http://dbpedia.org/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()
    resources = []

    for bindings in results['results']['bindings']:
        for result in bindings:
                value = bindings[result]['value']
                resources.append(value)

    return resources

'''
        SELECT ?result1, ?verb1 WHERE {
            ?result1 ?verb1 ?result2.

            ?result1 rdfs:label ?label1 ;
            a owl:Thing, dbo:Person .

            ?result2 rdfs:label ?label2 ;
            a owl:Thing, dbo:Place .

            filter strStarts(?label1, "Donald Trump")
            filter (lang(?label1) = 'en')

            filter strStarts(?label2, "New York")
            filter (lang(?label2) = 'en')
        }
'''

def getRelations(ent1, ent2):
    query = """
        SELECT DISTINCT ?verb1 WHERE {
            {
                <$REF_LEFT$> ?verb1 <$REF_RIGHT$>.
            }
            UNION
            {
                <$REF_LEFT$> ?verb1 ?result.

                ?result rdfs:label ?label ;
                a owl:Thing, dbo:$TYPE_RIGHT$ .

                filter strStarts(?label, "$LABEL_RIGHT$")
                filter (lang(?label) = 'en')
            }
        }
    """.replace('$REF_LEFT$', ent1[2]).replace('$REF_RIGHT$', ent2[2]).replace('$TYPE_RIGHT$', ent2[1]).replace('$LABEL_RIGHT$', ent2[0])

    sparql = SPARQLWrapper('http://dbpedia.org/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()
    return results

def prepare_entities_container(entities, sentence):
    """Method used to prepare entities container
                  Parameters
                  ----------
                  entities : list
                    list of entities
                  sentence : rdflib.term.Literal
                    
                  Returns
                  -------
                  entity_container : dict
                    container of entities
                  """

    entity_container = {}
    offset = 0
    for (entity, dbotype) in entities:
        index = sentence.find(entity)
        sentence = sentence.replace(entity, '', 1)
        indexes_dict = {'beginIndex': index + offset, 'endIndex': index + offset + len(entity)}

        if dbotype == "ORGANIZATION":
            dbotype = "Organisation"

        if entity in entity_container:
            entity_container[entity]['indexes'].append(indexes_dict)
        else:
            entity_container.update({entity: {'indexes': [indexes_dict], 'type': dbotype.title() }})
        offset += len(entity)

    print('Found entities:', entities, '\n', entity_container, '\n')
    return entity_container

def getResourceUrl(entity, dbotype):
    results = execute_query(entity, dbotype)

    if entity.endswith('s') and results['results']['bindings'] == []:
        results = execute_query(entity[:-1], dbotype)

    ifExists = False

    if not results['results']['bindings']:
        m_taIdentRef = 'http://aksw.org/notInWiki/' + "_".join(entity.split(" "))
    else:
        ifExists = True

        for result in results['results']['bindings']:
            if result != {} and result['result']['value']:
                m_taIdentRef = result['result']['value']
                
    return (ifExists, m_taIdentRef)

def clearQueriedRelation(results, dbotype1, dbotype2):
    predicates = []
    url = "http://dbpedia.org/ontology/"

    for bindings in results['results']['bindings']:
        for verb in bindings:
                value = bindings[verb]['value']
                id = value.rsplit('/', 1)[-1]

                if id == "wikiPageWikiLink" or id == "rdf-schema#seeAlso":
                    if dbotype1 == "Person" and dbotype2 == "Person":
                        predicates.append("relation")

                    continue

                predicates.append(id)

                # others
                if id == "keyPerson":
                    predicates.append("ceo")

                if id == "occupation":
                    predicates.append("employer")

    return list(set([ url + t for t in predicates]))

def create_graph(entity_container, m_referenceContext):
    """ Method used to create graph
                      Parameters
                      ----------
                      entity_container : dict
                        dictionary of entities
                      m_referenceContext : rdflib.term.URIRef
                        
                      Returns
                      -------
                      g : Grpah
                        output graph
                      """
    g = Graph()
    namespace_manager = rdflib.namespace.NamespaceManager(g)

    nif = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
    namespace_manager.bind('nif', nif)

    aksw = Namespace("http://aksw.org/notInWiki/")
    namespace_manager.bind('aksw', aksw)

    dbr = Namespace("http://dbpedia.org/resource/")
    namespace_manager.bind('dbr', dbr)

    dbo = Namespace("http://dbpedia.org/ontology/")
    namespace_manager.bind('dbo', dbo)

    oa = Namespace("http://www.w3.org/ns/oa#")
    namespace_manager.bind('oa', oa)

    itsrdf = Namespace("http://www.w3.org/2005/11/its/rdf#")
    namespace_manager.bind('itsrdf', itsrdf)

    nonNegativeInteger = URIRef('http://www.w3.org/2001/XMLSchema#nonNegativeInteger')
    typeUri = URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')

    k = m_referenceContext.rfind("#")
    contextUrlWithoutHash = m_referenceContext[:k]
    
    '''
    cached = {}
    for entity in entity_container:
        cached[entity] = getBytesToRelation(entity, entity_container[entity]['type'])
    '''
    
    dbpediaResources = []

    for entity in entity_container:
        dbpediaResources.append((entity, entity_container[entity]['type'], ""))

    for t in dbpediaResources:
        e = list(dbpediaResources)
        e.remove(t)

        result = (t[0], t[1], resolve_entity(t, e))

        if not result[2] and t[0].endswith('s'):
            result = (t[0], t[1], resolve_entity((t[0][:-1], t[1], t[2]), e))

        dbpediaResources[dbpediaResources.index(t)] = result

    # let's do some rock'n'roll
    for entity in entity_container:
        m_anchor = entity
        resource1 = dbpediaResources[[x[0] for x in dbpediaResources].index(entity)]
        m_taIdentRef = resource1[2]
        ifExists = bool(m_taIdentRef)

        relations = []

        if ifExists:
            for entity2 in entity_container:
                if entity == entity2:
                    continue

                resource2 = dbpediaResources[[x[0] for x in dbpediaResources].index(entity2)]
                m_taIdentRef2 = resource2[2]
                ifExists2 = bool(m_taIdentRef2)
                    
                if ifExists2:
                    #queriedRelation = execute_query_relation(prepare_query_relation(m_taIdentRef, m_taIdentRef2))
                    queriedRelation = getRelations(resource1, resource2)
                    
                    results = clearQueriedRelation(queriedRelation, entity_container[entity]['type'], entity_container[entity2]['type'])

                    if results != []:
                        relations.append((m_taIdentRef2, results))

        else:
            m_taIdentRef = 'http://aksw.org/notInWiki/' + "_".join(entity.split(" "))

        for occur in entity_container[entity]['indexes']:
            m_beginIndex = occur['beginIndex']
            m_endIndex = occur['endIndex']
            m_byte = contextUrlWithoutHash + ("#char=%d,%d" % (m_beginIndex, m_endIndex))

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


        print(relations)

        #realtions
        for (res2Ref, rels) in relations:
            for url in rels:
                relByte = BNode()

                g.add( (relByte, typeUri, RDF.Statement ) )
                g.add( (relByte, typeUri, oa.Annotation ) )

                targetByte = BNode()
                g.add( (relByte, oa.hasTarget, targetByte ) )

                g.add( (targetByte, typeUri, oa.SpecificResource ) )
                g.add( (targetByte, oa.hasSource, URIRef(m_referenceContext) ) )

                g.add( (relByte, RDF.subject, URIRef(m_taIdentRef) ) )
                g.add( (relByte, RDF.object, URIRef(res2Ref) ) )
                g.add( (relByte, RDF.predicate, URIRef(url) ) )
                
    # graph output
    #print(g.serialize(format='turtle').decode('utf-8'))

    return g

def run():
    """ Method used to run processing input file"""

    Btn.config(state="disable")
    outputText.delete('1.0', END)
    g = rdflib.Graph()
    g.parse(data=inputText.get("1.0",END), format='n3')

    context, sentence = get_request_string(g)

    print('\nSent: ' + sentence + '\n')

    (entities, grammarRelations) = get_entities(sentence)

    print("grammar relation: \n", grammarRelations, "\n")

    if entities:
        entity_container = prepare_entities_container(entities, sentence)
        output_graph = create_graph(entity_container, context)
        outputText.insert(END, output_graph.serialize(format='turtle').decode('utf-8'))
    else:
        print('No entities found!')
    Btn.config(state="normal")




def threadButtonRun():
    threading.Thread(target=run).start()


def main():

    '''
    sentence = nltk.word_tokenize("Google CEO Sundar Pichai responded today to the firing of employee James Damore over his controversial memo on workplace diversity.")
    #sentence = nltk.word_tokenize("Pope Francis in Chile at start of Latin America visit.")
    #sentence = nltk.word_tokenize("'First Lady' apple pies in the Kruhek bakery in Melania Trumps hometown of Sevnica in Slovenia are selling like hot cakes.")
    #sentence = nltk.word_tokenize("Shilpa Shetty and Raj Kundra, both 42, have been married for over eight years now. Viaan, 5, is the couple's only child. Shilpa's sister Shamita is also an actress.")
    #sentence = nltk.word_tokenize("Mark works in JPMC in London every day")

    st = StanfordNERTagger(CLASSIFIER_PATH, NER_PATH, encoding='utf-8')
    ne_tagged_sent = st.tag(sentence)
    ne_chunked_sent = stanford_ne_2_tree(ne_tagged_sent)

    reldicts = getRelations(ne_chunked_sent)

    for r in reldicts:
        print("subject: %s, predicate: %s, obj: %s" % (r['subjtext'], r['predicate'], r['objtext']))
    
    '''

    """ Method used to run program"""

    top.title("Knowledge Extraction")
    top.geometry("590x680")
    B = Button(top, text="Load .ttl file", command=filePath, height=2, width=80)
    B.place(x=10, y=570)
    global Btn
    Btn = Button(top, text="Analyze", command=threadButtonRun, height=2, width=80, state="disabled")
    Btn.place(x=10, y=620)

    scrollbar = Scrollbar(top)
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar1 = Scrollbar(top)
    scrollbar1.pack(side=LEFT, fill=Y)
    w = Label(top, text="INPUT")
    w.pack()
    inputText.place(x=10, y=10)
    inputText.pack()

    inputText.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=inputText.yview)

    w = Label(top, text="OUTPUT")
    w.pack()
    outputText.pack()

    outputText.config(yscrollcommand=scrollbar1.set)
    scrollbar1.config(command=outputText.yview)

    top.mainloop()


if __name__ == '__main__':
    main()
