"""
File: socialnetwork.py
Author: Alexandra Yakovleva

Create a graph representing a social network.
Add some people (vertices) to the network
then create friendships (edges) among some of them.
"""

from graph import LinkedDirectedGraph

def main() -> None:
    # Create a directed graph using an adjacency list
    myNetworkGraph = LinkedDirectedGraph()

    # Add friends (vertices) to the graph and print it
    myNetworkGraph.addVertex("Anna")
    myNetworkGraph.addVertex("Boris")
    myNetworkGraph.addVertex("Christina")
    myNetworkGraph.addVertex("Asaf")
    myNetworkGraph.addVertex("Helen")
    myNetworkGraph.addVertex("Glenn")
    myNetworkGraph.addVertex("Marco")

    print("Graph after adding friends:")
    print(myNetworkGraph)
    print()

    # Create friendships (edges) among some of them.
    myNetworkGraph.addEdge("Boris", "Glenn", 1)
    myNetworkGraph.addEdge("Glenn", "Boris", 1)
    myNetworkGraph.addEdge("Christina", "Asaf", 1)
    myNetworkGraph.addEdge("Asaf", "Christina", 1)
    myNetworkGraph.addEdge("Marco", "Asaf", 1)
    myNetworkGraph.addEdge("Marco", "Christina", 1)
    myNetworkGraph.addEdge("Marco", "Boris", 1)
    myNetworkGraph.addEdge("Boris", "Marco", 1)
    myNetworkGraph.addEdge("Marco", "Glenn", 1)
    myNetworkGraph.addEdge("Helen", "Anna", 1)

    print("Graph after adding friendships:")
    print(myNetworkGraph)
    print()

    # Marco's friends and friendships
    print("Incident edges of Marco:", list(map(str, myNetworkGraph.incidentEdges("Marco"))))

if __name__ == "__main__":
    main()
    """
    OUTPUT:
    Graph after adding friends:
    7 Vertices:  Anna Boris Christina Asaf Helen Glenn Marco
    0 Edges: 

    Graph after adding friendships:
    7 Vertices:  Anna Boris Christina Asaf Helen Glenn Marco
    10 Edges:  Boris>Glenn:1 Boris>Marco:1 Christina>Asaf:1 Asaf>Christina:1 Helen>Anna:1 Glenn>Boris:1 Marco>Asaf:1 Marco>Christina:1 Marco>Boris:1 Marco>Glenn:1

    Incident edges of Marco: ['Marco>Asaf:1', 'Marco>Christina:1', 'Marco>Boris:1', 'Marco>Glenn:1']
    """
