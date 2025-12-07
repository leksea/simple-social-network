"""
file:main.py
Author: Alexandra Yakovleva
"""
from modules.socialnetwork import SocialNetwork

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
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            network.add_profile(name, email, phone)

        elif choice == "2":
            name = input("Profile name to show: ").strip()
            network.show_profile(name)

        elif choice == "3":
            network.show_all_profiles()

        elif choice == "4":
            current_name = input("Current name: ").strip()
            new_name = input("New name (leave blank to keep): ").strip()
            if new_name == "":
                new_name = None
            new_email = input("New email (leave blank to keep): ").strip()
            if new_email == "":
                new_email = None
            new_phone = input("New phone (leave blank to keep): ").strip()
            if new_phone == "":
                new_phone = None
            network.update_profile(current_name, new_name, new_email, new_phone)

        elif choice == "5":
            name = input("Name of profile to remove: ").strip()
            network.remove_profile(name)

        elif choice == "6":
            name1 = input("First profile: ").strip()
            name2 = input("Second profile: ").strip()
            network.add_friendship(name1, name2)

        elif choice == "7":
            name1 = input("First profile: ").strip()
            name2 = input("Second profile: ").strip()
            network.remove_friendship(name1, name2)

        elif choice == "8":
            # Relies on LinkedDirectedGraph.__str__ implementation
            print("Raw graph representation:\n")
            print(network.graph)

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()