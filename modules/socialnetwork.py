"""
File: socialnetwork.py
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

    # ------------- CRUD: CREATE -------------

    def add_profile(self):
        """Create a new profile (vertex in the graph)."""
        ...

    def add_friendship(self):
        """Create a friendship (undirected edge between two profiles)."""
        ...

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