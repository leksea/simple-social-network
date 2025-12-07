"""
file: test_socialnetwork.py
author: Alexandra Yakovleva
Unit test for SocialNetwork
"""
import unittest
from modules.socialnetwork import SocialNetwork
from modules.userprofile import UserProfile

class TestSocialNetworkScenario(unittest.TestCase):
    def test_profile_equality_and_hash(self) -> None:
        """Profiles are equal and hash-equal if name/email/phone match."""
        p1 = UserProfile("Anna", "anna@example.com", "111-1111")
        p2 = UserProfile("Anna", "anna@example.com", "111-1111")
        p3 = UserProfile("Anna", "another@example.com", "111-1111")

        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)
        self.assertEqual(hash(p1), hash(p2))

        # Hash-based membership should work
        s = {p1}
        self.assertIn(p2, s)
        self.assertNotIn(p3, s)

    def test_add_profile_and_find(self) -> None:
        """add_profile registers a profile and find_profile retrieves it."""
        net = SocialNetwork()

        net.add_profile("Anna", "anna@example.com", "111-1111")
        anna = net.find_profile("Anna")

        self.assertIsNotNone(anna)
        self.assertEqual(
            anna,
            UserProfile("Anna", "anna@example.com", "111-1111")
        )

        # Stored in dict and set
        self.assertEqual(len(net.profiles), 1)
        self.assertEqual(len(net.profile_set), 1)

    def test_prevent_duplicate_profiles_by_data(self) -> None:
        """Adding the same profile data twice does not create duplicates."""
        net = SocialNetwork()

        net.add_profile("Anna", "anna@example.com", "111-1111")
        net.add_profile("Anna", "anna@example.com", "111-1111")  # duplicate

        self.assertEqual(len(net.profiles), 1)
        self.assertEqual(len(net.profile_set), 1)

    def test_add_friendship_and_get_friends(self) -> None:
        """Friendships are created between profiles and visible via get_friends."""
        net = SocialNetwork()
        net.add_profile("Anna", "anna@example.com", "111-1111")
        net.add_profile("Boris", "boris@example.com", "222-2222")
        net.add_profile("Christina", "christina@example.com", "333-3333")

        anna = net.find_profile("Anna")
        boris = net.find_profile("Boris")
        christina = net.find_profile("Christina")
        self.assertIsNotNone(anna)
        self.assertIsNotNone(boris)
        self.assertIsNotNone(christina)

        net.add_friendship(anna, boris)
        net.add_friendship(anna, christina)

        anna_friends = net.get_friends("Anna")
        boris_friends = net.get_friends("Boris")
        christina_friends = net.get_friends("Christina")

        self.assertEqual({f.name for f in anna_friends}, {"Boris", "Christina"})
        self.assertEqual({f.name for f in boris_friends}, {"Anna"})
        self.assertEqual({f.name for f in christina_friends}, {"Anna"})

    def test_suggest_friends_friends_of_friends(self) -> None:
        """suggest_friends returns FoF ranked by mutual friend count."""
        net = SocialNetwork()
        net.add_profile("Anna", "anna@example.com", "111-1111")
        net.add_profile("Boris", "boris@example.com", "222-2222")
        net.add_profile("Christina", "christina@example.com", "333-3333")
        net.add_profile("David", "david@example.com", "444-4444")

        anna = net.find_profile("Anna")
        boris = net.find_profile("Boris")
        christina = net.find_profile("Christina")
        david = net.find_profile("David")

        net.add_friendship(anna, boris)
        net.add_friendship(boris, christina)
        net.add_friendship(boris, david)

        suggestions_for_anna = net.suggest_friends("Anna")
        suggestion_names = {p.name for p in suggestions_for_anna}

        # Anna is directly connected only to Boris, so FoF via Boris = {Christina, David}
        self.assertEqual(suggestion_names, {"Christina", "David"})

    def test_update_profile_renames_and_updates_hash_set(self) -> None:
        """update_profile renames user and keeps hash-based sets consistent."""
        net = SocialNetwork()
        net.add_profile("Anna", "anna@example.com", "111-1111")
        net.add_profile("Boris", "boris@example.com", "222-2222")

        anna = net.find_profile("Anna")
        boris = net.find_profile("Boris")
        net.add_friendship(anna, boris)

        net.update_profile("Anna", new_name="Ann", new_email="ann@example.com")

        self.assertIsNone(net.find_profile("Anna"))
        ann = net.find_profile("Ann")
        self.assertIsNotNone(ann)
        self.assertEqual(ann.name, "Ann")
        self.assertEqual(ann.email, "ann@example.com")

        # Friendship should now be between Ann and Boris
        ann_friends = net.get_friends("Ann")
        self.assertEqual({f.name for f in ann_friends}, {"Boris"})

        # Only two profiles total, one renamed
        self.assertEqual(len(net.profiles), 2)
        self.assertEqual(len(net.profile_set), 2)

    def test_remove_friendship_and_profile(self) -> None:
        """Removing friendships and profiles updates all structures."""
        net = SocialNetwork()
        net.add_profile("Anna", "anna@example.com", "111-1111")
        net.add_profile("Boris", "boris@example.com", "222-2222")

        anna = net.find_profile("Anna")
        boris = net.find_profile("Boris")
        net.add_friendship(anna, boris)

        # Remove friendship
        net.remove_friendship(anna, boris)
        self.assertEqual(net.get_friends("Anna"), [])
        self.assertEqual(net.get_friends("Boris"), [])

        # Remove profile
        net.remove_profile("Boris")
        self.assertIsNone(net.find_profile("Boris"))
        self.assertEqual(net.get_friends("Anna"), [])
        self.assertEqual(len(net.profiles), 1)
        self.assertEqual(len(net.profile_set), 1)

if __name__ == "__main__":
    unittest.main()