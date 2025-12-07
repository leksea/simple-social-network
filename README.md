# Simple Social Network (Advanced Python Project)
WVC Advanced Python Project — Spring 2025  

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Project Structure](#project-structure)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [UML Diagrams](#uml-diagrams)  
7. [Design Details](#design-details)  
8. [Examples](#examples)  
9. [Testing](#testing)  
10. [License](#license)

---

## Overview
This project is a **Python implementation of a social network system** built on top of a **graph data structure** (`LinkedDirectedGraph` from Ken Lambert).

It demonstrates:

- Graph-based modeling of user relationships  
- Object-oriented design with hashing, equality, and indexing  
- Managing duplicate names using internal numeric user IDs  
- CRUD operations and friend suggestions based on friends-of-friends  

The project includes a full test suite, UML diagrams, and an interactive console menu.

---

## Features

### Profile Management (CRUD)
- Add new user profiles with auto-assigned unique IDs  
- Support multiple users with the **same name**  
- Update profile info (name, email, phone)  
- Delete profiles and automatically clean related friendships  
- Prevent exact duplicates (same name + email + phone) using hashing

### Friendship Management
- Add and remove friendships  
- Friendships are **mutual** but stored as two directed edges  
- Prevent self-friendship and duplicate edges  

### Friend Recommendation Engine
Suggest new friends based on:

1. Friends-of-friends  
2. Ranked by number of **mutual friends**  
3. Alphabetical tiebreak  

### Graph Integration
- Uses Lambert’s `LinkedDirectedGraph`  
- Each user ID is a graph vertex  
- Friendships represented as edges  

---

## Project Structure
````text
simple-social-network/
│
├── README.md                      # Project overview, usage, diagrams
├── LICENSE                        # License information
├── .gitignore                     # Git ignore rules
│
├── modules/                       # Core implementation
│   ├── __init__.py
│   ├── socialnetwork.py           # Main SocialNetwork class
│   ├── userprofile.py             # UserProfile class with hashing + equality
│   ├── graph.py                   # LinkedDirectedGraph, LinkedVertex, LinkedEdge
│   └── abstractcollection.py      # Base collection class from Lambert
│
├── tests/                         # Unit tests
│   ├── __init__.py
│   └── testsocialnetwork.py       # Test suite for SocialNetwork features
│
├── examples/                      # Example usage scripts (optional)
│   ├── __init__.py
│   └── demo_social_network.py     # Demonstrates friend suggestions, CRUD, etc.
│
└── main.py                        # CLI entry point for interactive mode
````

---
## Installation
1. Clone this repository:  
    ```bash
    git clone https://github.com/leksea/simple-social-network.git
    cd simple-social-network
    ```
2. Set up a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate   # macOS/Linux
    venv\Scripts\activate      # Windows
   ```
3. Optional: Install ```pytest``` test package:
    ```bash
    pip install pytest
    ```
---

## Usage
Run the main program:
```bash
  python main.py
```
Example:
``` text
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
```
---
## UML Diagrams
See the full documentation in [docs/classdiagram.md](docs/classdiagram.md).
Or run:
```bash
  pyreverse modules/socialnetwork.py -o png -p social_network -d docs
```
---
## Design Details

This project follows a modular, object-oriented design centered around graph-based connectivity. The goal is to model a lightweight social network with support for duplicate names, fast profile lookup, and efficient friendship operations.

### Core Architecture

UserProfile Class Represents a single user in the network.
SocialNetwork Class Coordinates all user and friendship operations.

This layered design separates concerns:
-- the graph manages edges,

-- the dictionaries manage lookup and identity,

-- the profile set handles uniqueness, and

-- the adjacency list handles fast friendships.


### Algorithms and Data Flow


---
## Examples
Here is a basic example of creating profiles, adding friendships, and generating friend suggestions:

``` python
from modules.socialnetwork import SocialNetwork

net = SocialNetwork()

# Create profiles
alex1 = net.add_profile("Alex", "alex@wvc.edu", "408-111-2222")
alex2 = net.add_profile("Alex", "alex2@wvc.edu", "650-333-4444")
bella = net.add_profile("Bella", "bella@wvc.edu", "415-555-6666")

# Friendships
net.add_friendship(alex1, bella)
net.add_friendship(bella, alex2)

# Friend suggestions (alex1 gets alex2)
suggestions = net.suggest_friends(alex1)
for s in suggestions:
    print(s)
```
For more, check code in `examples/` directory.

---
## Testing

The unit tests validate every core feature of the social network, including:

UserProfile Behavior
Adding Profiles
Friendships
Friend Suggestion Engine
Updating Profiles
Removing Profiles

``` bash
pytest tests/
```
---
## License

This project is licensed under the MIT License.
See the LICENSE file for full details.
