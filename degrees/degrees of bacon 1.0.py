import csv
import sys
from heapq import heappop, heappush

# Data structures
people = {}  # Maps person ID to a dictionary with name, birth year, and movies
movies = {}  # Maps movie ID to a dictionary with title, year, and stars
names = {}   # Maps lowercase names to sets of corresponding IDs

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

def load_data(directory):
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            name_key = row["name"].lower()
            if name_key not in names:
                names[name_key] = {row["id"]}
            else:
                names[name_key].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars relationships
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["person_id"]]["movies"].add(row["movie_id"])
            movies[row["movie_id"]]["stars"].add(row["person_id"])
def shortest_path(source, target):
    """Returns the shortest path from source to target using A* search."""
    frontier = []
    heappush(frontier, (0, Node(source, None, None)))  # (cost, node)
    explored = set()
    path_length = 0  # Add this line

    while frontier:
        _, current_node = heappop(frontier)
        current_person = current_node.state

        if current_person == target:
            path = []
            while current_node.parent:
                path.append((current_node.action, current_node.state))
                current_node = current_node.parent
            path.reverse()
            return path

        explored.add(current_person)
        path_length += 1  # Increment path_length here

        for movie_id in people[current_person]["movies"]:
            for neighbor in movies[movie_id]["stars"]:
                if neighbor not in explored:
                    cost = path_length + 1  # Use path_length instead of path
                    heappush(frontier, (cost, Node(neighbor, current_node, movie_id)))

    return None  # Return None if no path is found

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")
if __name__ == "__main__":
    directory = sys.argv[1]
    start_name = sys.argv[2]
    end_name = sys.argv[3]

    load_data(directory)

    start_ids = names.get(start_name.lower())
    end_ids = names.get(end_name.lower())
    if not start_ids or not end_ids:
        print("Actor not found.")
        sys.exit(1)

    # You can add more robust name ID selection mechanism here
    start_id = next(iter(start_ids))
    end_id = next(iter(end_ids))

    path = shortest_path(start_id, end_id)
    if path:
        for movie_id, person_id in path:
            print(f"{people[person_id]['name']} starred in {movies[movie_id]['title']} with {movie_id}")
    else:
        print("No connection found.")
