__author__ = 'mrittha'

import wikipedia
import networkx as nx
import unicodedata




if __name__ == "__main__":
    G = nx.Graph()
    nodes={}
    search_term="java programming language"
    topics = wikipedia.search(search_term)

    main_root=topics[0].encode('ascii', 'xmlcharrefreplace')
    nodes[main_root]=0
    print topics
    for topic in topics[1:]:
        new_topics = wikipedia.search(topic)[:10]
        root=topic.encode('ascii', 'xmlcharrefreplace')
        print root,new_topics
        if root in nodes:
            root_number=nodes[root]
        else:
            root_number=len(nodes.keys())
            nodes[root]=root_number
        G.add_node(nodes[root],label=root)
        G.add_edge(nodes[main_root],nodes[root])
        for node in new_topics[1:]:
            node=node.encode('ascii', 'xmlcharrefreplace')
            if node!=root:
                if node not in nodes:
                     nodes[node]=len(nodes.keys())
                    #print node,node_number
                node_number=nodes[node]
                G.add_node(nodes[node],label=node)
                print root,'->',node
                G.add_edge(nodes[root], nodes[node])
    nx.write_dot(G, search_term.replace(' ','_')+".dot")
