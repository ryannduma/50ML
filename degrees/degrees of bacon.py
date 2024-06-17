import csv
import sys
from heapq import heappop, heappush
from util import Node, StackFrontier, QueueFrontier
class Movie:
    def __init__(self, title):
        self.title = title
        self.actors = []

class Actor:
    def __init__(self, name):
        self.name = name
        self.movies = []

def load_data(filename):
    """ Load data from CSV, a row contains an actor and a movie."""
    actors = {}
    movies = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            actor_name, movie_title = row
            if actor_name not in actors:
                actors[actor_name] = Actor(actor_name)
            if movie_title not in movies:
                movies[movie_title] = Movie(movie_title)
            actors[actor_name].movies.append(movies[movie_title])
            movies[movie_title].actors.append(actors[actor_name])
    return actors, movies

def heuristic(actor1, actor2):
    """ Simple heuristic that could be the difference in the number of movies they starred in. """
    return abs(len(actor1.movies) - len(actor2.movies))

def a_star_search(actors, start, goal):
    """ Perform the A* search between two actors. """
    open_set = []
    heappush(open_set, (0, start, [start]))  # (cost, actor, path)
    visited = set()

    while open_set:
        _, current, path = heappop(open_set)

        if current == goal:
            return path

        visited.add(current)

        for movie in current.movies:
            for neighbor in movie.actors:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    cost = len(new_path) - 1
                    heappush(open_set, (cost + heuristic(neighbor, goal), neighbor, new_path))

    return []

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: degrees.py [start_actor] [end_actor]")
        sys.exit(1)

    actors, _ = load_data("imdb_data.csv")
    start_actor = actors.get(sys.argv[1])
    end_actor = actors.get(sys.argv[2])

    if not start_actor or not end_actor:
        print("Actor not found.")
        sys.exit(1)

    path = a_star_search(actors, start_actor, end_actor)
    if path:
        for i in range(len(path) - 1):
            print(f"{i+1}: {path[i].name} and {path[i+1].name} starred in {', '.join(set(movie.title for movie in path[i].movies if movie in path[i+1].movies))}")
    else:
        print("No connection found.")
