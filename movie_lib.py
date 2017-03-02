import csv
from statistics import mean

rtg_by_movie_id = {}
rtg_by_user_id = {}
movie_names = {}

with open('u.data') as f:
    reader = csv.reader(f)
    for row in reader:
        row = row[0].split('\t')
        row[2] = int(row[2])
        if row[1] in rtg_by_movie_id:
            rtg_by_movie_id[row[1]].append(row[2])
        else:
            rtg_by_movie_id[row[1]] = [row[2]]
        if row[0] in rtg_by_user_id:
            rtg_by_user_id[row[0]].append(row[2])
        else:
            rtg_by_user_id[row[0]] = [row[2]]

with open('u.item', encoding='latin_1') as f:
    reader = csv.reader(f)
    for row in reader:
        row = row[0].split('|')
        movie_names[row[0]] = row[1]

def avg_rtg(id):
    return mean(rtg_by_movie_id[id])


print(movie_names)
