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

    # ------------- DECORATORS -------------

    @property
    def graph(self) -> LinkedDirectedGraph:
        return self._graph
    @property
    def profiles(self) -> Dict[str, UserProfile]:
        return self._profiles
    @property
    def friendships(self) -> Dict[str, Set[UserProfile]]:
        return self._friendships

    # ------------- CRUD: CREATE -------------

    def add_profile(self, name: str, email:str="", phone:str="") -> None:
        """
        Create a new profile (vertex in the graph).
        Precondition: unique profile name
        """

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
        """
        Create a friendship (undirected edge between two profiles).
        Precondition: name1 != name2 and both profiles exist
        """
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
        """
        Print a profile and its friends.
        Preconditin: profile name exists
        """
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
        """
        Print all profiles in the network.
        Precondition: self._profiles not empty
        """
        if not self._profiles:
            print("No profiles in the network.")
            return
        print("All profiles:")
        for name in sorted(self._profiles.keys()):
            print(" -", name)

    def suggest_friends(self, name: str) -> List[UserProfile]:
        """
        Return a sorted list of potential friend profiles (friends-of-friends).
        Precondition: name exists in self._profiles
        """
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
    def update_profile(self, current_name:str, new_name:str=None, new_email:str=None, new_phone:str=None):
        """
        Update profile data and rename vertex if needed.
        Precondition: current_name exists in self._profiles
        Precondition: new_name does not exist in self._profiles
        """
        profile = self.find_profile(current_name)
        if profile is None:
            print("Profile not found.")
            return

        # If we change the name, we must also update dictionaries and the graph.
        if new_name and new_name != current_name:
            if new_name in self._profiles:
                print("Another profile with that new name already exists.")
                return

            # Update profile object
            profile.update(name=new_name)

            # Move in _profiles dict
            self._profiles[new_name] = profile
            del self._profiles[current_name]

            # Move friendships
            self._friendships[new_name] = self._friendships[current_name]
            del self._friendships[current_name]
            # Update every friend's set
            for friend in self._friendships[new_name]:
                if current_name in self._friendships[friend]:
                    self._friendships[friend].remove(current_name)
                    self._friendships[friend].add(new_name)

            # Rebuild graph vertex name: remove + re-add
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

    def remove_profile(self, name:str) -> None:
        """
        Delete a profile (vertex) and all its friendships.
        Precondition: name exists in self._profiles
        """
        if name not in self._profiles:
            print("Profile not found.")
            return

        # Remove this profile from friends' sets
        for friend in list(self._friendships[name]):
            self._friendships[friend].discard(name)

        # Remove from our structures
        del self._profiles[name]
        del self._friendships[name]

        # Remove from graph (removes all incident edges)
        self._graph.removeVertex(name)

        print(f"Profile '{name}' and all its friendships removed.")

    def remove_friendship(self, name1:str, name2:str) ->None :
        """
        Delete the friendship between two profiles.
        Precondition: name1 exists in self._friendships
        Precondition: name2 exists in self._friendships
        """

        if name1 not in self._profiles or name2 not in self._profiles:
            print("Both profiles must exist.")
            return

        if name2 not in self._friendships[name1]:
            print("These two profiles are not friends.")
            return

        self._friendships[name1].remove(name2)
        self._friendships[name2].remove(name1)

        # Remove edges from graph
        self._graph.removeEdge(name1, name2)
        self._graph.removeEdge(name2, name1)

        print(f"Friendship between {name1} and {name2} removed.")
