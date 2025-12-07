"""
File: TestSocialNetworkScenario.py
Author: Alexandra Yakovleva

A simple social network application based on a graph network.
"""
from typing import Optional, List, Tuple, Set, Dict

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

    def add_profile(self, name: str, email:str="", phone:str="") -> None:
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

    def add_friendship(self, name1:str, name2:str) -> None:
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

    def find_profile(self, name:str) -> Optional[UserProfile]:
        """Return the Profile object or None."""
        return self._profiles.get(name, None)

    def get_friends(self, name:str) -> list[UserProfile]:
        """Return a sorted list of friend names."""
        if name not in self._friendships:
            return []
        return sorted(self._friendships[name])

    def show_profile(self, name:str) -> None:
        """Print a profile and its friends."""
        profile = self.find_profile(name)
        if profile is None:
            print("Profile not found.")
            return
        print("----- Profile -----")
        print(profile)
        print("----- Friends -----")
        friends = self.get_friends(name)
        if friends:
            for friend in friends:
                print(friend)
        else:
            print("(no friends yet)")

    def show_all_profiles(self) -> None:
        """Print all profiles in the network."""
        if not self._profiles:
            print("No profiles in the network.")
            return
        print("All profiles:")
        for name in sorted(self._profiles.keys()):
            print(" -", name)

    def suggest_friends(self, name: str) -> List[UserProfile]:
        """Return a sorted list of potential friend profiles (friends-of-friends)."""
        # If the user doesn't exist, no suggestions
        if name not in self._profiles:
            return []

        # Direct friends of this user
        direct_friends: Set[str] = self._friendships.get(name, set())

        # Count mutual friends for each candidate
        candidate_scores: Dict[str, int] = {}

        for friend in direct_friends:
            friends_of_friend: Set[str] = self._friendships.get(friend, set())
            for fof in friends_of_friend:
                # Skip self and already-friends
                if fof == name or fof in direct_friends:
                    continue
                # Increase mutual-friend count
                candidate_scores[fof] = candidate_scores.get(fof, 0) + 1

        # Sort candidates:
        #   - first by mutual friend count (descending)
        #   - then by name (ascending)
        sorted_candidates: List[Tuple[str, int]] = sorted(
            candidate_scores.items(),
            key=lambda item: (-item[1], item[0])
        )

        # Convert names to UserProfile objects
        suggestions: List[UserProfile] = [
            self._profiles[candidate_name]
            for candidate_name, _ in sorted_candidates
            if candidate_name in self._profiles
        ]

        return suggestions
    # ------------- CRUD: UPDATE -------------
    def update_profile(self, current_name:str, new_name=None, new_email=None, new_phone=None):
        """Update profile data and rename vertex if needed."""
        profile = self.find_profile(current_name)
        if profile is None:
            print("Profile not found.")
            return

        # If we change the name, we must also update dictionaries and the graph.
        if new_name and new_name != current_name:
            if new_name in self._profiles:
                print("Another profile with that new name already exists.")
                return

            # 1) Update profile object
            profile.update(name=new_name)

            # 2) Move in _profiles dict
            self._profiles[new_name] = profile
            del self._profiles[current_name]

            # 3) Move friendships
            self._friendships[new_name] = self._friendships[current_name]
            del self._friendships[current_name]
            # Update every friend's set
            for friend in self._friendships[new_name]:
                if current_name in self._friendships[friend]:
                    self._friendships[friend].remove(current_name)
                    self._friendships[friend].add(new_name)

            # 4) Rebuild graph vertex name (simplest approach: remove + re-add)
            # Remove old vertex (and all its incident edges).
            self._graph.removeVertex(current_name)
            # Add new vertex
            self._graph.addVertex(new_name)
            # Re-add edges from friendships
            for friend in self._friendships[new_name]:
                self._graph.addEdge(new_name, friend, 1)
                self._graph.addEdge(friend, new_name, 1)

        # Update email/phone
        profile.update(email=new_email, phone=new_phone)
        print("Profile updated.")

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