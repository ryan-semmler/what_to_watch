import os
import csv
from statistics import mean
import operator
import math


class User:
    def __init__(self, user_id, rtg_by_user_id, movie_names):
        self.user_id = user_id
        self.movies_and_ratings = rtg_by_user_id[self.user_id]
        self.movies_seen = []
        self.movies_not_seen = []
        movie_id_list = [i[0] for i in self.movies_and_ratings]
        for movie in movie_names.keys():
            if movie in movie_id_list:
                self.movies_seen.append(movie)
            else:
                self.movies_not_seen.append(movie)

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
        # print(self.user_id, self.movies_and_ratings)
        ratings_needed = []
        for i in range(len(self.movies_and_ratings)):
            if self.movies_and_ratings[i][0] in shared_movies:
                ratings_needed.append(self.movies_and_ratings[i][1])
        return ratings_needed
        # return [self.movies_and_ratings[1] for movie in shared_movies] # if self.movies_and_ratings[0] == movie]
# =======
#         return [self.movies_and_ratings[1] for movie in shared_movies if self.movies_and_ratings[0] == movie]


class Movie:
    def __init__(self, item_id, movie_title, times_rated, avg_rtg):
        self.item_id = item_id
        self.movie_title = movie_title
        self.times_rated = times_rated
        self.avg_rtg = avg_rtg

    def __repr__(self):
        return "Title: {}, Avg Rating: {}\n ".format(self.movie_title, round(self.avg_rtg, 2))


def clear():
    os.system("clear")


def clear():
    os.system("clear")


def similar(user1, rtg_by_user_id, movie_names):
    similarity_list = []
    for user_id in rtg_by_user_id:
        user2 = User(user_id, rtg_by_user_id, movie_names)
        shared = user1.get_shared_movies(user2)
        # print(shared)
        v = user1.get_shared_ratings(shared)
        w = user2.get_shared_ratings(shared)
        similarity = euclidean_distance(v, w)
        similarity_list.append((user2, similarity))
        similarity_list = sorted(similarity_list, key=lambda x: x[1])
    return similarity_list[::-1]


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
    for movie in sorted_movie_list:
        for tup in rtg_by_user_id[user_id]:
            if tup[0] == movie.item_id:
                seen = True
        if seen is False:
            unseen.append(movie.item_id)

# <<<<<<< HEAD
#     return unseen[0:10]
#
#
# def get_recs(similarity_list):
#     # similarity_list = ((user0, similarity0), (user1, similarity1)...)
# =======
    return unseen[:-11:-1]


def get_recs(similarity_list):
# similarity_list = ((user0, similarity0), (user1, similarity1)...)
# >>>>>>> 477727b88fc76235a26e13869b14756eaea1c542
    rec_list = []
    for tup in similarity_list:
        for movie_tup in tup[0].movies_and_ratings:
            if movie_tup[1] >= 4.5 and movie_tup[0] not in rec_list:
                rec_list.append(movie_tup[0])
    return rec_list


def popular_movie_list(rtg_by_movie_id, movie_names):
    # print(movie_names)
    popular_movie_list = []
    for movie_id in movie_names.keys():
        if len(rtg_by_movie_id[movie_id]) >= 100:
            popular_movie_list.append(Movie(movie_id, movie_names[movie_id], len(rtg_by_movie_id[movie_id]), mean(rtg_by_movie_id[movie_id])))
    popular_movie_list.sort(key=operator.attrgetter('avg_rtg'))
    popular_movie_list = popular_movie_list[-1::-1]
    # print(popular_movie_list[:10])  # prints top 10
    return popular_movie_list[:10]



def main():
    rtg_by_movie_id = {}
    rtg_by_user_id = {}
    movie_names = {}
    get_movie_data(rtg_by_movie_id, rtg_by_user_id, movie_names)
    movie_list = []
    # print(rtg_by_movie_id)
    # print(rtg_by_user_id[user_id])
    # print(movie_names)
    for movie_id in movie_names.keys():
        movie_list.append(Movie(movie_id, movie_names[movie_id], len(rtg_by_movie_id[movie_id]), mean(rtg_by_movie_id[movie_id])))
    movie_list.sort(key=operator.attrgetter('avg_rtg'))
    movie_list = movie_list[-1::-1]
    # print(movie_list)
    # print("\n")
    # print(movie_list[:11])  # top 10

    choice = input("Welcome!\n1. Top-rated movies\n2. Top movies you haven't seen\n3. Movies recommended for you\n")
    if(choice == "2" or choice == "3"):
        user1 = User(input("what's your id: "), rtg_by_user_id, movie_names)
        if choice == "2":
            l = hasnot_seen(movie_list, user1.user_id, rtg_by_user_id)
            for movie_id in l:
                print(movie_names[movie_id])
        else:
            my_recs = get_recs(similar(user1, rtg_by_user_id, movie_names))[:-11:-1]
            for i in range(len(my_recs)):
                print(i + 1, movie_names[my_recs[i]])
            # print([movie_names[x] for x in my_recs[:10]])
    else:
        for item in popular_movie_list(rtg_by_movie_id, movie_names):
            print("{}: {}".format(item.movie_title, item.avg_rtg))


if __name__ == '__main__':
    main()
