"""
file:main.py
Author: Alexandra Yakovleva
"""
from modules.socialnetwork import SocialNetwork

def main() -> None:
    """Simple text menu to exercise the SocialNetwork class (ID-based)."""
    net = SocialNetwork()

    MENU = """
--- Simple Social Network ---
1. Add profile
2. Show profiles by name
3. Show all profiles
4. Update profile (by ID)
5. Remove profile (by ID)
6. Add friendship (by IDs)
7. Remove friendship (by IDs)
8. Suggest friends (by ID)
0. Quit
"""

    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Goodbye.")
            break

        elif choice == "1":
            # CREATE profile
            name = input("Name: ").strip()
            email = input("Email (optional): ").strip()
            phone = input("Phone (optional): ").strip()
            profile = net.add_profile(name, email, phone)
            if profile is not None:
                print(f"Created profile with id={profile.user_id}.")
            print()

        elif choice == "2":
            # READ profiles by name
            name = input("Enter name to search: ").strip()
            net.show_profile(name)
            print()

        elif choice == "3":
            # READ all profiles
            net.show_all_profiles()
            print()

        elif choice == "4":
            # UPDATE profile by ID
            try:
                user_id = int(input("Enter profile ID to update: ").strip())
            except ValueError:
                print("Invalid ID.")
                continue

            new_name = input("New name (leave blank to keep): ").strip()
            new_email = input("New email (leave blank to keep): ").strip()
            new_phone = input("New phone (leave blank to keep): ").strip()

            net.update_profile(
                user_id=user_id,
                new_name=new_name or None,
                new_email=new_email or None,
                new_phone=new_phone or None,
            )
            print()

        elif choice == "5":
            # DELETE profile by ID
            try:
                user_id = int(input("Enter profile ID to remove: ").strip())
            except ValueError:
                print("Invalid ID.")
                continue

            net.remove_profile(user_id)
            print()

        elif choice == "6":
            # CREATE friendship (by IDs)
            try:
                id1 = int(input("First profile ID: ").strip())
                id2 = int(input("Second profile ID: ").strip())
            except ValueError:
                print("Invalid ID(s).")
                continue

            p1 = net.profiles.get(id1)
            p2 = net.profiles.get(id2)
            if p1 is None or p2 is None:
                print("Both IDs must exist.")
            else:
                net.add_friendship(p1, p2)
            print()

        elif choice == "7":
            # DELETE friendship (by IDs)
            try:
                id1 = int(input("First profile ID: ").strip())
                id2 = int(input("Second profile ID: ").strip())
            except ValueError:
                print("Invalid ID(s).")
                continue

            p1 = net.profiles.get(id1)
            p2 = net.profiles.get(id2)
            if p1 is None or p2 is None:
                print("Both IDs must exist.")
            else:
                net.remove_friendship(p1, p2)
            print()

        elif choice == "8":
            # SUGGEST friends (by ID)
            try:
                user_id = int(input("Profile ID to suggest friends for: ").strip())
            except ValueError:
                print("Invalid ID.")
                continue

            profile = net.profiles.get(user_id)
            if profile is None:
                print("Profile not found.")
                print()
                continue

            suggestions = net.suggest_friends(profile)
            if not suggestions:
                print("No friend suggestions.")
            else:
                print("Suggested friends:")
                for p in suggestions:
                    print(f" - id={p.user_id}, name={p.name}, email={p.email}, phone={p.phone}")
            print()

        else:
            print("Invalid choice, please try again.\n")

if __name__ == "__main__":
    main()
