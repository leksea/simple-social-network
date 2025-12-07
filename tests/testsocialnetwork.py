"""
file: test_socialnetwork.py
author: Alexandra Yakovleva
Unit test for SocialNetwork
"""
import unittest
from modules.socialnetwork import SocialNetwork

class TestSocialNetworkScenario(unittest.TestCase):
    def test_full_crud_scenario(self):
        """
        OBJECTIVES:

        - testing create profiles
        - testing add friendships
        - testing update profile
        - testing remove friendship
        - testing remove profile
        """
        net = SocialNetwork()

        # --- Create profiles (C) ---
        net.add_profile("Anna", "anna@example.com", "111-1111")
        net.add_profile("Boris", "boris@example.com", "222-2222")
        net.add_profile("Christina", "christina@example.com", "333-3333")

        # Check they exist
        self.assertIn("Anna", net._profiles)
        self.assertIn("Boris", net._profiles)
        self.assertIn("Christina", net._profiles)
        self.assertEqual(len(net._profiles), 3)

        # Initially, no friendships
        self.assertEqual(net.get_friends("Anna"), [])
        self.assertEqual(net.get_friends("Boris"), [])
        self.assertEqual(net.get_friends("Christina"), [])

        # --- Add friendships (C) ---
        net.add_friendship("Anna", "Boris")
        net.add_friendship("Anna", "Christina")

        # Check friend lists
        self.assertCountEqual(net.get_friends("Anna"), ["Boris", "Christina"])
        self.assertEqual(net.get_friends("Boris"), ["Anna"])
        self.assertEqual(net.get_friends("Christina"), ["Anna"])

        # --- Update profile (U): Anna -> Ann ---
        net.update_profile(
            "Anna",
            new_name="Ann",
            new_email="ann@example.com",
            new_phone="999-9999",
        )

        # Old name should be gone
        self.assertNotIn("Anna", net._profiles)
        self.assertIn("Ann", net._profiles)

        # Check updated fields
        ann = net._profiles["Ann"]
        self.assertEqual(ann.name, "Ann")
        self.assertEqual(ann.email, "ann@example.com")
        self.assertEqual(ann.phone, "999-9999")

        # Friendships should now be attached to "Ann"
        self.assertCountEqual(net.get_friends("Ann"), ["Boris", "Christina"])
        # Reverse friendships updated too
        self.assertIn("Ann", net.get_friends("Boris"))
        self.assertIn("Ann", net.get_friends("Christina"))

        # --- Remove friendship (D): Ann - Boris ---
        net.remove_friendship("Ann", "Boris")

        self.assertNotIn("Boris", net.get_friends("Ann"))
        self.assertNotIn("Ann", net.get_friends("Boris"))
        # Ann should still be friends with Christina
        self.assertEqual(net.get_friends("Ann"), ["Christina"])

        # --- Remove profile (D): Christina ---
        net.remove_profile("Christina")

        # Christina should be gone from profiles and friendships
        self.assertNotIn("Christina", net._profiles)
        self.assertNotIn("Christina", net._friendships)

        # Ann should no longer list Christina
        self.assertEqual(net.get_friends("Ann"), [])
        # Boris still exists, but currently no friends
        self.assertEqual(net.get_friends("Boris"), [])

        # Optional: check graph vertex count if __len__ is implemented
        # After removal we should only have Ann and Boris
        try:
            self.assertEqual(len(net._graph), 2)
        except TypeError:
            # If LinkedDirectedGraph doesn't support len(), skip this check
            pass


if __name__ == "__main__":
    unittest.main()