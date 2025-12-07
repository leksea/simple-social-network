"""
file:main.py
Author: Alexandra Yakovleva
"""
from modules.socialnetwork import SocialNetwork

def main() -> None:
    """Simple text-based driver to exercise the SocialNetwork class."""
    network = SocialNetwork()

    MENU = """
--- Simple Social Network ---
1. Add profile
2. Show profile
3. Show all profiles
4. Update profile
5. Remove profile
6. Add friendship
7. Remove friendship
8. Suggest friends
0. Quit
"""

    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Goodbye.")
            break

        elif choice == "1":
            # CREATE: profile
            name = input("Name: ").strip()
            email = input("Email (optional): ").strip()
            phone = input("Phone (optional): ").strip()
            network.add_profile(name, email, phone)

        elif choice == "2":
            # READ: single profile
            name = input("Profile name to show: ").strip()
            network.show_profile(name)

        elif choice == "3":
            # READ: all profiles
            network.show_all_profiles()

        elif choice == "4":
            # UPDATE: profile data
            current_name = input("Current name: ").strip()
            new_name = input("New name (leave blank to keep): ").strip()
            new_email = input("New email (leave blank to keep): ").strip()
            new_phone = input("New phone (leave blank to keep): ").strip()

            network.update_profile(
                current_name=current_name,
                new_name=new_name or None,
                new_email=new_email or None,
                new_phone=new_phone or None,
            )

        elif choice == "5":
            # DELETE: profile
            name = input("Name of profile to remove: ").strip()
            network.remove_profile(name)

        elif choice == "6":
            # CREATE: friendship (via profiles)
            name1 = input("First profile name: ").strip()
            name2 = input("Second profile name: ").strip()
            p1 = network.find_profile(name1)
            p2 = network.find_profile(name2)
            if p1 is None or p2 is None:
                print("Both profiles must exist.")
            else:
                network.add_friendship(p1, p2)

        elif choice == "7":
            # DELETE: friendship (via profiles)
            name1 = input("First profile name: ").strip()
            name2 = input("Second profile name: ").strip()
            p1 = network.find_profile(name1)
            p2 = network.find_profile(name2)
            if p1 is None or p2 is None:
                print("Both profiles must exist.")
            else:
                network.remove_friendship(p1, p2)

        elif choice == "8":
            # READ: suggestions
            name = input("Profile name to suggest friends for: ").strip()
            suggestions = network.suggest_friends(name)
            if not suggestions:
                print("No friend suggestions.")
            else:
                print("Suggested friends:")
                for prof in suggestions:
                    print(f" - {prof.name} ({prof.email}, {prof.phone})")

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()