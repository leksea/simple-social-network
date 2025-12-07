"""
file: testsocialnetwork.py
author: Alexandra Yakovleva
Unit test for SocialNetwork
"""
import unittest
from modules.socialnetwork import SocialNetwork
from modules.userprofile import UserProfile

class TestSocialNetworkScenario(unittest.TestCase):
    def test_userprofile_equality_and_hash(self) -> None:
        """Profiles are equal and hash-equal if name/email/phone match."""
        p1 = UserProfile("Alex", "alex@wvc.edu", "408-555-0001")
        p2 = UserProfile("Alex", "alex@wvc.edu", "408-555-0001")
        p3 = UserProfile("Alex", "alex2@wvc.edu", "408-555-0001")

        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)
        self.assertEqual(hash(p1), hash(p2))

        s = {p1}
        self.assertIn(p2, s)
        self.assertNotIn(p3, s)

    def test_add_profile_and_reject_exact_duplicate(self) -> None:
        """Exact duplicate (same name+email+phone) is rejected."""
        net = SocialNetwork()

        p1 = net.add_profile("Alex", "alex@wvc.edu", "408-555-0001")
        p2 = net.add_profile("Alex", "alex@wvc.edu", "408-555-0001")  # duplicate

        self.assertIsInstance(p1, UserProfile)
        self.assertIsNone(p2)

        # Only one profile stored
        self.assertEqual(len(net.profiles), 1)
        self.assertEqual(len(net.profile_set), 1)

    def test_duplicate_names_allowed(self) -> None:
        """Two different profiles with the same name but different data are allowed."""
        net = SocialNetwork()

        p1 = net.add_profile("Alex", "alex_cs@wvc.edu", "408-555-0101")
        p2 = net.add_profile("Alex", "alex_math@wvc.edu", "650-555-0202")

        self.assertIsInstance(p1, UserProfile)
        self.assertIsInstance(p2, UserProfile)
        self.assertNotEqual(p1.email, p2.email)
        self.assertNotEqual(p1.user_id, p2.user_id)

        # Two profiles total, both named Alex
        self.assertEqual(len(net.profiles), 2)

        alex_profiles = net.find_profile("Alex")
        self.assertEqual(len(alex_profiles), 2)
        self.assertEqual({p.email for p in alex_profiles},
                         {"alex_cs@wvc.edu", "alex_math@wvc.edu"})

    def test_add_friendship_and_get_friends(self) -> None:
        """Friendships are mutual and returned correctly via get_friends()."""
        net = SocialNetwork()

        alex = net.add_profile("Alex", "alex@wvc.edu", "408-555-0001")
        bella = net.add_profile("Bella", "bella@wvc.edu", "650-555-0002")
        carlos = net.add_profile("Carlos", "carlos@wvc.edu", "415-555-0003")

        assert isinstance(alex, UserProfile)
        assert isinstance(bella, UserProfile)
        assert isinstance(carlos, UserProfile)

        net.add_friendship(alex, bella)
        net.add_friendship(alex, carlos)

        alex_friends = net.get_friends(alex)
        bella_friends = net.get_friends(bella)
        carlos_friends = net.get_friends(carlos)

        self.assertEqual({p.name for p in alex_friends}, {"Bella", "Carlos"})
        self.assertEqual({p.name for p in bella_friends}, {"Alex"})
        self.assertEqual({p.name for p in carlos_friends}, {"Alex"})

    def test_suggest_friends_friends_of_friends(self) -> None:
        """suggest_friends uses friends-of-friends and counts mutual friends."""
        net = SocialNetwork()

        alex = net.add_profile("Alex", "alex@wvc.edu", "408-555-0001")
        bella = net.add_profile("Bella", "bella@wvc.edu", "650-555-0002")
        carlos = net.add_profile("Carlos", "carlos@wvc.edu", "415-555-0003")
        diana = net.add_profile("Diana", "diana@wvc.edu", "408-555-0004")

        assert isinstance(alex, UserProfile)
        assert isinstance(bella, UserProfile)
        assert isinstance(carlos, UserProfile)
        assert isinstance(diana, UserProfile)

        # Alex is friends with Bella and Carlos
        net.add_friendship(alex, bella)
        net.add_friendship(alex, carlos)

        # Bella and Carlos are both friends with Diana
        net.add_friendship(bella, diana)
        net.add_friendship(carlos, diana)

        # FoF for Alex: Diana (via Bella and Carlos) with count 2
        suggestions = net.suggest_friends(alex)
        self.assertEqual(len(suggestions), 1)
        self.assertEqual(suggestions[0].name, "Diana")

    def test_update_profile_changes_name_and_index_and_hashset(self) -> None:
        """update_profile updates name, name index, and keeps _profile_set consistent."""
        net = SocialNetwork()

        alex = net.add_profile("Alex", "alex@wvc.edu", "408-555-0001")
        assert isinstance(alex, UserProfile)
        user_id = alex.user_id
        assert user_id is not None

        # Initially, Alex is under name "Alex"
        self.assertEqual({p.user_id for p in net.find_profile("Alex")}, {user_id})
        self.assertEqual(net.find_profile("Alexa"), [])

        # Update name and email
        net.update_profile(user_id, new_name="Alexa", new_email="alexa@wvc.edu")

        # Old name should no longer return this profile
        self.assertEqual(net.find_profile("Alex"), [])

        # New name should return this profile
        alexa_profiles = net.find_profile("Alexa")
        self.assertEqual(len(alexa_profiles), 1)
        alexa = alexa_profiles[0]
        self.assertEqual(alexa.name, "Alexa")
        self.assertEqual(alexa.email, "alexa@wvc.edu")
        self.assertEqual(alexa.user_id, user_id)

        # _profile_set should still contain exactly one profile equal to alexa
        self.assertIn(alexa, net.profile_set)
        self.assertEqual(len(net.profile_set), 1)

    def test_remove_profile_cleans_friendships_and_indexes(self) -> None:
        """remove_profile deletes the profile and all references from friendship and name index."""
        net = SocialNetwork()

        alex = net.add_profile("Alex", "alex@wvc.edu", "408-555-0001")
        bella = net.add_profile("Bella", "bella@wvc.edu", "650-555-0002")

        assert isinstance(alex, UserProfile)
        assert isinstance(bella, UserProfile)

        net.add_friendship(alex, bella)

        # Sanity check
        self.assertEqual({p.name for p in net.get_friends(alex)}, {"Bella"})
        self.assertEqual({p.name for p in net.get_friends(bella)}, {"Alex"})

        # Remove Bella
        net.remove_profile(bella.user_id)

        # Bella is gone
        self.assertEqual(len(net.find_profile("Bella")), 0)
        self.assertNotIn(bella, net.profile_set)

        # Alex now has no friends
        self.assertEqual(net.get_friends(alex), [])

    def test_remove_friendship(self) -> None:
        """remove_friendship removes the edge and updates adjacency."""
        net = SocialNetwork()

        alex = net.add_profile("Alex", "alex@wvc.edu", "408-555-0001")
        bella = net.add_profile("Bella", "bella@wvc.edu", "650-555-0002")

        assert isinstance(alex, UserProfile)
        assert isinstance(bella, UserProfile)

        net.add_friendship(alex, bella)

        self.assertEqual({p.name for p in net.get_friends(alex)}, {"Bella"})
        self.assertEqual({p.name for p in net.get_friends(bella)}, {"Alex"})

        net.remove_friendship(alex, bella)

        self.assertEqual(net.get_friends(alex), [])
        self.assertEqual(net.get_friends(bella), [])

if __name__ == "__main__":
    unittest.main()