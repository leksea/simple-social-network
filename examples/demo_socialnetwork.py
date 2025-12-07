"""
File: demo_socialnetwork.py
Author: Alexandra Yakovleva

Demonstration script for the SocialNetwork system.
Shows how to create profiles, add friendships, update profiles,
and generate friend suggestions.
"""

from modules.socialnetwork import SocialNetwork
from modules.userprofile import UserProfile


def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main() -> None:
    net = SocialNetwork()

    print_header("1. Creating Profiles")

    alex1 = net.add_profile("Alex", "alex@wvc.edu", "408-111-2222")
    alex2 = net.add_profile("Alex", "alex2@wvc.edu", "650-222-3333")  # duplicate name allowed
    bella = net.add_profile("Bella", "bella@wvc.edu", "415-333-4444")
    carlos = net.add_profile("Carlos", "carlos@wvc.edu", "408-444-5555")
    diana = net.add_profile("Diana", "diana@wvc.edu", "408-555-6666")

    print("Profiles created:")
    for p in net.profiles.values():
        print(f"  id={p.user_id}: {p.name}, {p.email}, {p.phone}")

    print_header("2. Creating Friendships")

    net.add_friendship(alex1, bella)
    net.add_friendship(alex1, carlos)
    net.add_friendship(bella, diana)
    net.add_friendship(carlos, diana)

    # Show friend lists
    print(f"\nFriends of Alex1 (id={alex1.user_id}):")
    for f in net.get_friends(alex1):
        print(f"  -> {f.name} (id={f.user_id})")

    print(f"\nFriends of Bella (id={bella.user_id}):")
    for f in net.get_friends(bella):
        print(f"  -> {f.name} (id={f.user_id})")

    print_header("3. Friend Suggestions")

    suggestions = net.suggest_friends(alex1)
    print(f"Suggested friends for Alex1 (id={alex1.user_id}):")
    if suggestions:
        for s in suggestions:
            print(f"  -> {s.name} (id={s.user_id})")
    else:
        print("  (no suggestions)")

    print_header("4. Updating a Profile")

    print("Updating Alex1’s name to 'Alexander' and email...")
    net.update_profile(alex1.user_id, new_name="Alexander", new_email="alexander@wvc.edu")

    print("New profile details:")
    net.show_profile("Alexander")

    print_header("5. Removing a Profile")

    print(f"Removing Bella (id={bella.user_id})...")
    net.remove_profile(bella.user_id)

    print(f"\nCurrent friends of Alexander (id={alex1.user_id}) after removal:")
    for f in net.get_friends(alex1):
        print(f"  -> {f.name} (id={f.user_id})")

    print_header("6. Final State of All Profiles")
    net.show_all_profiles()

    print("\nDemo complete.\n")


if __name__ == "__main__":
    main()