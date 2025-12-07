"""
File: socialnetwork.py
Author: Alexandra Yakovleva

DESCRIPTION: A simple social networking system implemented using a graph structure.

Class Variables:
    _graph: LinkedDirectedGraph
        The underlying graph storing user IDs as vertices and
        friendships as directed edges between those IDs.

    _profiles: Dict[int, UserProfile]
        Maps each internal user ID to its corresponding UserProfile object.
        Allows multiple users to share the same name.

    _name_index: Dict[str, Set[int]]
        Maps a name (e.g., "Alex") to a set of user IDs for all profiles
        that share that name.

    _profile_set: Set[UserProfile]
        A hash-based set of all profile objects, used to detect
        exact duplicates (same name, email, and phone).

    _friendships: Dict[int, Set[int]]
        Adjacency structure mapping each user ID to the set of IDs
        representing that user's friends.

    _next_id: int
        An auto-incrementing integer used to assign unique user IDs
        to new profiles.

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
        # Map profile ID -> Profile object
        self._profiles: Dict[int, UserProfile] = {}
        # Map name to set of ids
        self._name_index: Dict[str, Set[int]] = {}
        # Hash-based set of all profiles for duplicate check
        self._profile_set: Set[UserProfile] = set()
        # Separate adjacency structure
        self._friendships: Dict[int, Set[int]] = {}  # ID -> set of friend IDs
        self._next_id: int = 1 # auto-increment next ID when adding a profile

    # ------------- PROPERTIES -------------

    @property
    def graph(self) -> LinkedDirectedGraph:
        return self._graph

    @property
    def profiles(self) -> Dict[int, UserProfile]:
        return self._profiles

    @property
    def friendships(self) -> Dict[int, Set[int]]:
        return self._friendships

    @property
    def profile_set(self) -> Set[UserProfile]:
        return self._profile_set

    # ---------- Helpers ----------

    def profile_exists(self, target: UserProfile) -> bool:
        """Does a profile with same (name, email, phone) already exist?"""
        return target in self._profile_set

    def find_profile_by_data(self, target: UserProfile) -> Optional[UserProfile]:
        """Search matching profile by equality (__eq__)."""
        if target not in self._profile_set:
            return None
        for p in self._profile_set:
            if p == target:
                return p
        return None

    # ------------- CRUD: CREATE -------------

    def add_profile(self, name: str, email: str = "", phone: str = "") -> Optional[UserProfile]:
        """
        Create a new profile (vertex in the graph).
        Precondition: there is no profile with the same name + email + phone.
        """
        new_profile = UserProfile(name, email, phone)

        if self.profile_exists(new_profile):
            print("A profile with the same name/email/phone already exists.")
            return None

        user_id = self._next_id
        self._next_id += 1

        # assign id to profile object
        new_profile.user_id = user_id

        # store in structures
        self._profiles[user_id] = new_profile
        self._profile_set.add(new_profile)
        self._friendships[user_id] = set()
        self._name_index.setdefault(name, set()).add(user_id)

        # graph vertex labeled by ID
        self._graph.addVertex(user_id)

        print(f"Profile created: id={user_id}, name='{name}'")
        return new_profile

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

        id1 = profile1.user_id
        id2 = profile2.user_id

        if profile1.user_id is None or profile2.user_id is None:
            print("Both profiles must have valid IDs.")
            return

        # Check if already friends
        if id2 in self._friendships[id1]:
            print("These profiles are already friends.")
            return

        # Update friendships
        self._friendships[id1].add(id2)
        self._friendships[id2].add(id1)

        # Update graph (IDs as vertex labels)
        self._graph.addEdge(id1, id2, 1)
        self._graph.addEdge(id2, id1, 1)

        print(f"Friendship created between {id1} and {id2}.")

    # ------------- CRUD: READ -------------

    def find_profile(self, name: str) -> List[UserProfile]:
        """
        Return a list of all profiles with the given name.
        Returns an empty list if no matches are found.
        """
        ids = sorted(self._name_index.get(name, set()))
        return [self._profiles[i] for i in ids]

    def get_friends(self, profile:UserProfile) -> List[UserProfile]:
        """
        Return a sorted list of friend profiles.
        Precondition: the profile belongs to this SocialNetwork.
        """
        if profile.user_id is None or profile.user_id not in self._friendships:
            return []
        friend_ids = sorted(self._friendships[profile.user_id])
        return [self._profiles[i] for i in friend_ids]

    def show_profile(self, name: str) -> None:
        """
        Print all profiles with this name and each of their friend lists.
        Supports duplicate names.
        """
        matches = self.find_profile(name)

        if not matches:
            print("No profiles found with name:", name)
            return

        for profile in matches:
            print(f"===== Profile (id={profile.user_id}) =====")
            print(profile)

            print("----- Friends -----")
            friends = self.get_friends(profile)
            if friends:
                for f in friends:
                    print(f"[id={f.user_id}] {f.name}")
            else:
                print("(no friends yet)")

            print()  # spacing between profiles

    def show_all_profiles(self) -> None:
        """ Print all profiles in the network with their IDs."""
        if not self._profiles:
            print("No profiles in the network.")
            return
        print("All profiles:")
        for user_id in sorted(self._profiles):
            p = self._profiles[user_id]
            print(f" - id={user_id}, name={p.name}, email={p.email}, phone={p.phone}")

    def suggest_friends(self, profile: UserProfile) -> List[UserProfile]:
        """
        Return a list of friend profiles for the given profile.
        Precondition: the profile belongs to this SocialNetwork.
        """
        if profile.user_id is None or profile.user_id not in self._friendships:
            return []

        my_id = profile.user_id
        direct_friends: Set[int] = self._friendships.get(my_id, set())
        candidate_scores: Dict[int, int] = {}

        for fid in direct_friends:
            for fof_id in self._friendships.get(fid, set()):
                if fof_id == my_id or fof_id in direct_friends:
                    continue
                candidate_scores[fof_id] = candidate_scores.get(fof_id, 0) + 1

        # sort by mutual friend count desc, then by name
        sorted_candidates: List[Tuple[int, int]] = sorted(
            candidate_scores.items(),
            key=lambda item: (-item[1], self._profiles[item[0]].name),
        )

        return [self._profiles[user_id] for user_id, _ in sorted_candidates]

    # ------------- CRUD: UPDATE -------------

    def update_profile(
            self,
            user_id: int,
            new_name: Optional[str] = None,
            new_email: Optional[str] = None,
            new_phone: Optional[str] = None,
    ) -> None:
        """
        Update profile data (name, email, phone) for the given user ID.

        - Names are not required to be unique.
        - Hash-based structures are updated safely before and after mutation.
        """
        profile = self._profiles.get(user_id)
        if profile is None:
            print("Profile not found.")
            return

        # Remove from hash-based set BEFORE changing hash fields.
        self._profile_set.discard(profile)

        # Update name index if name changes
        old_name = profile.name
        if new_name and new_name != old_name:
            # remove from old name set
            old_ids = self._name_index.get(old_name, set())
            old_ids.discard(user_id)
            if not old_ids:
                self._name_index.pop(old_name, None)

            # add to new name set
            self._name_index.setdefault(new_name, set()).add(user_id)

        # Update the profile's own data fields
        profile.update(
            name=new_name,
            email=new_email,
            phone=new_phone,
        )

        # Re-add to hash-based set with updated hash
        self._profile_set.add(profile)

        print(f"Profile updated: id={user_id}")

    # ------------- CRUD: DELETE -------------

    def remove_profile(self, user_id: int) -> None:
        """
        Delete a profile (vertex) and all its friendships.
        Must delete from hash set BEFORE deleting the profile.
        Precondition: id exists in self._profiles.
        """
        profile = self._profiles.get(user_id)
        if profile is None:
            print("Profile not found.")
            return

        # Remove from hash set first
        self._profile_set.discard(profile)

        # Remove from friends' lists
        for friend_id in list(self._friendships.get(user_id, set())):
            self._friendships[friend_id].discard(user_id)

        # Remove from friendships map
        self._friendships.pop(user_id, None)

        # Remove from profiles dict
        self._profiles.pop(user_id, None)

        # Remove from name index
        name_ids = self._name_index.get(profile.name, set())
        name_ids.discard(user_id)
        if not name_ids:
            self._name_index.pop(profile.name, None)

        # Remove from graph (vertex is labeled by ID)
        self._graph.removeVertex(user_id)

        print(f"Profile id={user_id} and all its friendships removed.")

    def remove_friendship(self, profile1: UserProfile, profile2: UserProfile) -> None:
        """
        Delete the friendship between two profiles.
        Precondition: both profiles belong to this network and are friends.
        """
        if profile1.user_id is None or profile2.user_id is None:
            print("Both profiles must have valid IDs.")
            return

        id1 = profile1.user_id
        id2 = profile2.user_id

        if id1 not in self._profiles or id2 not in self._profiles:
            print("Both profiles must belong to this SocialNetwork.")
            return

        if id2 not in self._friendships.get(id1, set()):
            print("These two profiles are not friends (or do not exist).")
            return

        # Update adjacency structure
        self._friendships[id1].remove(id2)
        self._friendships[id2].remove(id1)

        # Remove edges from the graph (IDs are vertex labels)
        self._graph.removeEdge(id1, id2)
        self._graph.removeEdge(id2, id1)

        print(f"Friendship removed between id={id1} and id={id2}.")