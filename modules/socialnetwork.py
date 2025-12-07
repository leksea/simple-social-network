"""
File: testsocialnetwork.py
Author: Alexandra Yakovleva

DESCRIPTION: A simple social networking system implemented using a graph structure.

    Class Variables:
        _graph: LinkedDirectedGraph
            The underlying graph storing profile names as vertices and friendships as edges.

        _profiles: Dict[str, UserProfile]
            Maps each profile name to its corresponding UserProfile object.

        _profile_set: Set[UserProfile]
            A hash-based set containing all UserProfile objects, used for fast
            duplicate detection and equality comparison (__eq__, __hash__).

        _friendships: Dict[str, Set[str]]
            Adjacency structure mapping a profile name to the set of its friend names.

    Features:
        • Add, remove, and update user profiles
        • Create and delete friendships
        • Retrieve profiles and friend lists
        • Suggest new friends using friends-of-friends ranking

    Notes:
        - Friendships are undirected but stored internally as two directed edges.
        - Profile hashing and equality allow efficient membership tests and duplicate checks.

"""


from __future__ import annotations
from typing import Optional, List, Tuple, Set, Dict

from .graph import LinkedDirectedGraph
from .userprofile import UserProfile


class SocialNetwork:
    """Maintains profiles and friendships using a graph."""

    def __init__(self) -> None:
        # Underlying directed graph
        self._graph: LinkedDirectedGraph = LinkedDirectedGraph()
        # Map profile name -> Profile object
        self._profiles: Dict[str, UserProfile] = {}
        # Hash-based set of all profiles
        self._profile_set: Set[UserProfile] = set()
        # Separate adjacency structure to make friend lookups easy
        self._friendships: Dict[str, Set[str]] = {}  # name -> set of friend names

    # ------------- PROPERTIES -------------

    @property
    def graph(self) -> LinkedDirectedGraph:
        return self._graph

    @property
    def profiles(self) -> Dict[str, UserProfile]:
        return self._profiles

    @property
    def friendships(self) -> Dict[str, Set[str]]:
        return self._friendships

    @property
    def profile_set(self) -> Set[UserProfile]:
        return self._profile_set

    # ---------- helpers that use hashing ----------

    def profile_exists(self, target: UserProfile) -> bool:
        """Use hashing (__hash__ and __eq__) to check if profile already exists."""
        return target in self._profile_set

    def find_profile_by_data(self, target: UserProfile) -> Optional[UserProfile]:
        """
        Return an existing profile equal to target (by name/email/phone),
        or None if not found. Uses hashing for fast membership.
        """
        if target not in self._profile_set:
            return None
        # We know an equal object exists, but we want the stored instance.
        for profile in self._profile_set:
            if profile == target:
                return profile
        return None

    # ------------- CRUD: CREATE -------------

    def add_profile(self, name: str, email: str = "", phone: str = "") -> None:
        """
        Create a new profile (vertex in the graph).
        Precondition: there is no profile with the same name/email/phone.
        """
        new_profile = UserProfile(name, email, phone)

        if self.profile_exists(new_profile):
            print("A profile with the same name/email/phone already exists.")
            return

        self._profiles[name] = new_profile
        self._profile_set.add(new_profile)
        self._friendships[name] = set()
        self._graph.addVertex(name)
        print(f"Profile '{name}' created.")

    def add_friendship(self, profile1: UserProfile, profile2: UserProfile) -> None:
        """
        Create a friendship (undirected edge between two profiles).
        Precondition: profile1 != profile2 and both profiles belong to this network.
        """
        if profile1 not in self._profile_set or profile2 not in self._profile_set:
            print("Both profiles must belong to this SocialNetwork.")
            return

        # Prevent self-friendship
        if profile1 == profile2:
            print("A profile cannot be friends with itself.")
            return

        name1 = profile1.name
        name2 = profile2.name

        # Safety: ensure names exist in mapping (should be true if _profile_set is consistent)
        if name1 not in self._profiles or name2 not in self._profiles:
            print("Internal error: profile name not found in _profiles.")
            return

        # Check if already friends
        friends1 = self._friendships.get(name1, set())
        if name2 in friends1:
            print(f"{name1} and {name2} are already friends.")
            return

        # Update friendships
        self._friendships.setdefault(name1, set()).add(name2)
        self._friendships.setdefault(name2, set()).add(name1)

        # Update graph (str names as vertex labels)
        self._graph.addEdge(name1, name2, 1)
        self._graph.addEdge(name2, name1, 1)

        print(f"Friendship created between {name1} and {name2}.")


    # ------------- CRUD: READ -------------

    def find_profile(self, name: str) -> Optional[UserProfile]:
        """Return the UserProfile object or None, by name key."""
        return self._profiles.get(name)

    def get_friends(self, name: str) -> List[UserProfile]:
        """
        Return a sorted list of friend profiles.
        Precondition: name exists in self._profiles.
        """
        if name not in self._profiles:
            return []
        friend_names: Set[str] = self._friendships.get(name, set())
        return [self._profiles[n] for n in sorted(friend_names)]

    def show_profile(self, name: str) -> None:
        """
        Print a profile and its friends.
        Precondition: profile name exists.
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
            for f in friends:
                print(f.name)
        else:
            print("(no friends yet)")

    def show_all_profiles(self) -> None:
        """
        Print all profiles in the network.
        """
        if not self._profiles:
            print("No profiles in the network.")
            return
        print("All profiles:")
        for name in sorted(self._profiles):
            print(" -", name)

    def suggest_friends(self, name: str) -> List[UserProfile]:
        """
        Return a sorted list of potential friend profiles (friends-of-friends).
        Precondition: name exists in self._profiles.
        """
        if name not in self._profiles:
            return []

        direct_friends: Set[str] = self._friendships.get(name, set())
        candidate_scores: Dict[UserProfile, int] = {}

        for friend_name in direct_friends:
            friends_of_friend: Set[str] = self._friendships.get(friend_name, set())
            for fof_name in friends_of_friend:
                if fof_name == name or fof_name in direct_friends:
                    continue
                candidate_profile = self._profiles[fof_name]
                candidate_scores[candidate_profile] = (
                    candidate_scores.get(candidate_profile, 0) + 1
                )

        # Sort by:
        #   - mutual friend count descending
        #   - then by profile.name ascending
        sorted_candidates: List[Tuple[UserProfile, int]] = sorted(
            candidate_scores.items(),
            key=lambda item: (-item[1], item[0].name),
        )

        return [profile for profile, _score in sorted_candidates]

    # ------------- CRUD: UPDATE -------------

    def update_profile(
        self,
        current_name: str,
        new_name: Optional[str] = None,
        new_email: Optional[str] = None,
        new_phone: Optional[str] = None,
    ) -> None:
        """
        Update profile data and rename vertex if name changes.
        Must delete and re-add new hash values BEFORE changing data
        Precondition: current_name exists in self._profiles.
        Precondition: should not match existing profile.
        """
        profile = self.find_profile(current_name)
        if profile is None:
            print("Profile not found.")
            return

        # Remove from hash-based set BEFORE changing hash fields.
        self._profile_set.discard(profile)

        # Handle rename (change dict key and friendships mapping)
        if new_name and new_name != current_name:
            if new_name in self._profiles:
                print("Another profile with that new name already exists.")
                # Put profile back into set unchanged
                self._profile_set.add(profile)
                return

            # Move dict entry
            self._profiles[new_name] = profile
            del self._profiles[current_name]

            # Move friendships
            self._friendships[new_name] = self._friendships[current_name]
            del self._friendships[current_name]

            # Update friends' entries (names only)
            for friend_name in self._friendships[new_name]:
                friends_of_friend = self._friendships[friend_name]
                if current_name in friends_of_friend:
                    friends_of_friend.remove(current_name)
                    friends_of_friend.add(new_name)

            # Update graph: remove old vertex, add new one, re-add edges
            self._graph.removeVertex(current_name)
            self._graph.addVertex(new_name)
            for friend_name in self._friendships[new_name]:
                self._graph.addEdge(new_name, friend_name, 1)
                self._graph.addEdge(friend_name, new_name, 1)

        # Update the profile's own data fields
        profile.update(
            name=new_name if new_name is not None else None,
            email=new_email,
            phone=new_phone,
        )

        # Re-add to hash-based set with updated hash
        self._profile_set.add(profile)

        print("Profile updated.")

    # ------------- CRUD: DELETE -------------

    def remove_profile(self, name: str) -> None:
        """
        Delete a profile (vertex) and all its friendships.
        Must delete from hash set BEFORE deleting the profile.
        Precondition: name exists in self._profiles.
        """
        profile = self.find_profile(name)
        if profile is None:
            print("Profile not found.")
            return

        # Remove from hash set first
        self._profile_set.discard(profile)

        # Remove from friends' lists
        for friend_name in list(self._friendships[name]):
            self._friendships[friend_name].discard(name)

        # Remove from dict and friendships map
        del self._profiles[name]
        del self._friendships[name]

        # Remove from graph
        self._graph.removeVertex(name)

        print(f"Profile '{name}' and all its friendships removed.")

    def remove_friendship(self, profile1: UserProfile, profile2: UserProfile) -> None:
        """
        Delete the friendship between two profiles.
        Precondition: both profiles belong to this network and are friends.
        """
        if profile1 not in self._profile_set or profile2 not in self._profile_set:
            print("Both profiles must belong to this SocialNetwork.")
            return

        name1 = profile1.name
        name2 = profile2.name

        if (
            name1 not in self._profiles
            or name2 not in self._profiles
            or name2 not in self._friendships.get(name1, set())
        ):
            print("These two profiles are not friends (or do not exist).")
            return

        # Update graph
        self._friendships[name1].remove(name2)
        self._friendships[name2].remove(name1)

        self._graph.removeEdge(name1, name2)
        self._graph.removeEdge(name2, name1)

        print(f"Friendship between {name1} and {name2} removed.")