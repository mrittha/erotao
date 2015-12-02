__author__ = 'mrittha'

import wikipedia
import networkx as nx
import unicodedata

if __name__ == "__main__":
    G = nx.Graph()
    topics = wikipedia.search("chinese pottery")
    for topic in topics:
        new_topics = wikipedia.search(topic)[:10]
        root=new_topics[0].encode('ascii', 'replace')
        print root
        G.add_node(root)
        for node in new_topics[1:]:
            node=node.encode('ascii', 'replace')
            print node
            G.add_node(node)
            G.add_edge(root, node)
        print new_topics
    nx.write_dot(G, "chinese pottery.dot")
