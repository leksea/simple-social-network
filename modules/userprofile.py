"""
File: userprofile.py
Author: Alexandra Yakovleva

Defines the UserProfile class for the social network.
"""


class UserProfile:
    """Represents a user's profile in the social network."""

    def __init__(self, name:str, email:str="", phone:str=""):
        self.name = name
        self.email = email
        self.phone = phone

    def update(self, name:str=None, email:str=None, phone:str=None):
        """Update fields that are not None."""
        if name is not None and name != "":
            self.name = name
        if email is not None and email != "":
            self.email = email
        if phone is not None and phone != "":
            self.phone = phone

    def __str__(self):
        return (f"Name:  {self.name}\n"
                f"Email: {self.email}\n"
                f"Phone: {self.phone}")
    def __eq__(self, other) -> bool:
        return (self.name, self.email, self.phone) == (other.name, other.email, other.phone)