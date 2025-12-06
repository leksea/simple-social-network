"""
File: TestSocialNetworkScenario.py
Author: Alexandra Yakovleva

A simple social network application based on a graph network.
"""

from graph import LinkedDirectedGraph
from userprofile import UserProfile


class SocialNetwork:
    """Maintains profiles and friendships using a graph."""

    def __init__(self):
        # Underlying directed graph
        self._graph = LinkedDirectedGraph()
        # Map profile name -> Profile object
        self._profiles = {}
        # Separate adjacency structure to make friend lookups easy
        self._friendships = {}  # name -> set of friend names

    # ------------- CRUD: CREATE -------------

    def add_profile(self, name, email="", phone="") -> None:
        """Create a new profile (vertex in the graph)."""

        if name in self._profiles:
            print("A profile with that name already exists.")
            return

        profile = UserProfile(name, email, phone)
        self._profiles[name] = profile
        self._friendships[name] = set()
        # Add vertex to the graph
        self._graph.addVertex(name)
        print(f"Profile '{name}' created.")


    def add_friendship(self, name1, name2) -> None:
        """Create a friendship (undirected edge between two profiles)."""
        if name1 not in self._profiles or name2 not in self._profiles:
            print("Both profiles must exist to create a friendship.")
            return
        if name1 == name2:
            print("A profile cannot be friends with itself.")
            return

        if name2 in self._friendships[name1]:
            print(f"{name1} and {name2} are already friends.")
            return

        # Update our adjacency sets
        self._friendships[name1].add(name2)
        self._friendships[name2].add(name1)

        # Add edges in both directions to the directed graph
        self._graph.addEdge(name1, name2, 1)
        self._graph.addEdge(name2, name1, 1)

        print(f"Friendship created between {name1} and {name2}.")

    # ------------- CRUD: READ -------------

    def find_profile(self) -> None:
        """Return the Profile object or None."""
        ...

    def get_friends(self) -> list[UserProfile]:
        """Return a sorted list of friend names."""
        ...

    def show_profile(self) -> None:
        """Print a profile and its friends."""
        ...

    def show_all_profiles(self) -> None:
        """Print all profiles in the network."""
        ...
    # ------------- CRUD: UPDATE -------------
    def update_profile(self) -> None:
        """Update profile data and rename vertex if needed."""
        ...
    # ------------- CRUD: DELETE -------------

    def remove_profile(self) -> None:
        """Delete a profile (vertex) and all its friendships."""
        ...

    def remove_friendship(self) ->None :
        """Delete the friendship between two profiles."""
        ...

# ------------- UI testing -------------

def main():
    network = SocialNetwork()

    MENU = """
--- Simple Social Network Menu ---
1. Add profile (Create)
2. Show profile (Read)
3. Show all profiles (Read)
4. Update profile (Update)
5. Remove profile (Delete)
6. Add friendship (Create)
7. Remove friendship (Delete)
8. Show raw graph (debug)
0. Quit
"""

    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Goodbye.")
            break

        elif choice == "1":
            print("Adding profile.")
            #network.add_profile()

        elif choice == "2":
            print("Displaying profile.")
            #name = input("Profile name to show: ").strip().lower()
            #network.show_profile(name)

        elif choice == "3":
            print("All profiles.")
            #network.show_all_profiles()

        elif choice == "4":
            print("Updating profile.")
            #current_name = input("Current name: ").strip().lower()
            #network.update_profile()

        elif choice == "5":
            print("Removing profile.")
            #name = input("Name of profile to remove: ").strip().lower()
            #network.remove_profile()

        elif choice == "6":
            print("Adding friendship.")
            #name1 = input("First profile: ").strip().lower()
            #name2 = input("Second profile: ").strip().lower()
            #network.add_friendship(name1, name2)

        elif choice == "7":
            print("Removing friendship.")
            #name1 = input("First profile: ").strip().lower()
            #name2 = input("Second profile: ").strip().lower()
            #network.remove_friendship(name1, name2)

        elif choice == "8":
            print("Show raw graph.")
            # Relies on LinkedDirectedGraph.__str__ implementation
            #print("Raw graph representation:\n")
            #print(network._graph)

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()