"""
File: userprofile.py
Author: Alexandra Yakovleva

Defines the UserProfile class for the social network.
"""
from typing import Any, Optional


class UserProfile:
    """Represents a user's profile in the social network."""

    def __init__(self, name:str, email:str="", phone:str="", user_id: Optional[int] = None):
        self.name = name
        self.email = email
        self.phone = phone
        self.user_id = user_id  # assigned by SocialNetwork


    def update(self, name:str=None, email:str=None, phone:str=None) -> None:
        """Update fields that are not None."""
        if name is not None and name != "":
            self.name = name
        if email is not None and email != "":
            self.email = email
        if phone is not None and phone != "":
            self.phone = phone

    def __eq__(self, other: Any) -> bool:
        """Two UserProfiles are equal if all identifying fields are equal."""
        if not isinstance(other, UserProfile):
            return False
        return (
            self.name == other.name and
            self.email == other.email and
            self.phone == other.phone
        )
    def __hash__(self) -> int:
       """Return a hash of the user's profile to be used with dicts and sets"""
       return hash((self.name, self.email, self.phone))

    def __repr__(self) -> str:
        """
        Return a string representation of the user's profile (for debugging purposes).
        """
        return (
            f"UserProfile(id={self.user_id}, "
            f"name={self.name!r}, email={self.email!r}, phone={self.phone!r})"
        )

    def __str__(self) -> str:
        """
        Return a string representation of the user's profile.
        """
        return (
            f"ID:    {self.user_id}\n"
            f"Name:  {self.name}\n"
            f"Email: {self.email}\n"
            f"Phone: {self.phone}"
        )