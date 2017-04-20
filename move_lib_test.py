from movie_lib import *


def test_euclidean_distance():
    assert movie_lib.euclidean_distance([1, 2, 3, 4, 5], [3, 4, 5, 6, 7]) == 5 ** 0.5 / 10
    assert movie_lib.euclidean_distance([], [1, 2, 3]) == 0


def test_hasnot_seen():
    assert movie_lib.hasnot_seen(sorted_movie_list, '123', rtg_by_user_id) ==
