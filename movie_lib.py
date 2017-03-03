import csv
from statistics import mean
import operator
import math


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.movies_and_ratings = rtg_by_user_id[self.user_id]
        self.movies_seen = []
        self.movies_not_seen = []

    def get_shared_movies(self, other):
        shared_movies = []
        if len(self.movies_and_ratings) <= len(other.movies_and_ratings):
            for i in self.movies_and_ratings:
                if i in other.movies_and_ratings:
                    shared_movies.append(i[0])
        else:
            for j in other.movies_and_ratings:
                if j in other.movies_and_ratings:
                    shared_movies.append(j[0])
        return shared_movies

    def get_shared_ratings(self, shared_movies):
        return [self.movies_and_ratings[1] for movie in shared_movies if self.movies_and_ratings[0] == movie]


class Movie:
    def __init__(self, item_id, movie_title, times_rated, avg_rtg):
        self.item_id = item_id
        self.movie_title = movie_title
        self.times_rated = times_rated
        self.avg_rtg = avg_rtg

    def __repr__(self):
        return "Title: {} Avg Rating: {} ".format(self.movie_title, self.avg_rtg)


def get_movie_data(rtg_by_movie_id, rtg_by_user_id, movie_names):
    with open('u.data') as f:  # scrapes general information file
        reader = csv.reader(f)
        for row in reader:
            row = row[0].split('\t')
            row[2] = int(row[2])
            if row[1] in rtg_by_movie_id:
                rtg_by_movie_id[row[1]].append(row[2])
            else:
                rtg_by_movie_id[row[1]] = [row[2]]
            if row[0] in rtg_by_user_id:
                rtg_by_user_id[row[0]].append((row[1], row[2]))
            else:
                rtg_by_user_id[row[0]] = [(row[1], row[2])]

    with open('u.item', encoding='latin_1') as f:  # scrapes Movie name file
        reader = csv.reader(f)
        for row in reader:
            row = row[0].split('|')
            movie_names[row[0]] = row[1]

    return(rtg_by_movie_id, movie_names)


def euclidean_distance(v, w):
    """Given two lists, give the Euclidean distance between them on a scale
    of 0 to 1. 1 means the two lists are identical.
    """

    # Guard against empty lists.
    if len(v) is 0:
        return 0

    # Note that this is the same as vector subtraction.
    differences = [v[idx] - w[idx] for idx in range(len(v))]
    squares = [diff ** 2 for diff in differences]
    sum_of_squares = sum(squares)

    return 1 / (1 + math.sqrt(sum_of_squares))


def hasnot_seen(sorted_movie_list, user_id, rtg_by_user_id):
    unseen = []
    seen = False
    for movie_id in sorted_movie_list:
        for tup in rtg_by_user_id[user_id]:
            if tup[0] == movie_id:
                seen = True
        if seen is False:
            unseen.append(movie_id)

    return unseen[0:11]


def similar(*args):
    similarity_list = []
    for user_id in rtg_by_user_id:
        shared = user1.get_shared_movies(user2)
        v = user1.get_shared_ratings(shared)
        w = user2.get_shared_ratings(shared)
        similarity = euclidean_distance(v, w)
        similarity_list.append((user_id, similarity))
    

def main():
    rtg_by_movie_id = {}
    rtg_by_user_id = {}
    movie_names = {}
    get_movie_data(rtg_by_movie_id, rtg_by_user_id, movie_names)
    movie_list = []
    hasnot_seen(movie_list, user_id, rtg_by_user_id)
    # print(rtg_by_movie_id)
    # print(rtg_by_user_id)
    # print(movie_names)
    for movie_id in movie_names.keys():
        movie_list.append(Movie(movie_id, movie_names[movie_id], len(rtg_by_movie_id[movie_id]), mean(rtg_by_movie_id[movie_id])))

    movie_list.sort(key=operator.attrgetter('avg_rtg'))
    movie_list = movie_list[-1::-1]
    print(movie_list)
    print(movie_list[:11])  # top 10

    similar()


# <<<<<<< HEAD
if __name__ == '__main__':
    main()
# =======
rtg_by_movie_id = {}
rtg_by_user_id = {}
movie_names = {}


def popular():
    popular = [rating for rating in rtg_by_movie_id if len(rtg_by_movie_id[rating][1]) > 5]
    return popular


print(popular())
# >>>>>>> 26991393350e0c9424e5677e98e3f7dd21ba6bc0
