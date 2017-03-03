import csv
from statistics import mean
import operator


class User:
    def __init__(self, user_id, rtg_by_user_id):
        self.user_id = user_id
        self.rtg_by_user_id = {}


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


def hasnot_seen(sorted_movie_list, user_id, rtg_by_user_id):
    unseen = []
    seen = False
    for movie_id in sorted_movie_list:
        for tup in rtg_by_user_id[user_id]:
            if tup[0] == movie_id:
                seen = True
        if seen == False:
            unseen.append(movie_id)
    return unseen[0:11]

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


if __name__ == '__main__':
    main()
