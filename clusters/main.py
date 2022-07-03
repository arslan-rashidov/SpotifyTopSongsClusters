import math


def read_file_and_get_elements(file_name):
    songs = {}
    all_dots = []
    clusters = {}

    with open(file_name) as f:
        for line in f.readlines():

            if '"' in line:
                title = line.split('"')[1]
                line = line.split('"')[-1]
            line = line.split(',')
            title = line[0]

            artist = line[1]
            bpm = line[5]
            pop = line[14]

            if artist != 'artist':
                clusters[(int(bpm), int(pop))] = [[f"{title} - {artist}", (int(bpm), int(pop))]]

    return clusters


def get_min_distance_in_songs(songs):
    min_distance = 0
    min_distance_song_first = 0
    min_distance_song_second = 0

    for song_index_first in range(len(list(songs.keys()))):
        song_first = list(songs.keys())[song_index_first]
        song_first_dot = songs[list(songs.keys())[song_index_first]]
        for song_index_second in range(song_index_first+1, len(list(songs.keys()))):
            song_second = list(songs.keys())[song_index_second]
            song_second_dot = songs[list(songs.keys())[song_index_second]]
            distance = math.dist(song_first_dot, song_second_dot)
            if song_index_first == 0 and song_index_second == 1:
                min_distance = distance
                min_distance_song_first = song_first
                min_distance_song_second = song_second
            else:
                if distance < min_distance:
                    min_distance = distance
                    min_distance_song_first = song_first
                    min_distance_song_second = song_second
    return min_distance, min_distance_song_first, min_distance_song_second


def get_best_clusters_to_merge(clusters):
    min_distance = 0
    first_cluster = 0
    second_cluster = 0

    for cluster_first_index in range(len(list(clusters.values()))):
        first_middle_dot = list(clusters.keys())[cluster_first_index]
        for cluster_second_index in range(cluster_first_index + 1, len(list(clusters.values()))):
            second_middle_dot = list(clusters.keys())[cluster_second_index]
            distance = math.dist(first_middle_dot, second_middle_dot)
            if cluster_first_index == 0 and cluster_second_index == 1:
                min_distance = distance
                first_cluster = list(clusters.values())[cluster_first_index]
                second_cluster = list(clusters.values())[cluster_second_index]
            else:
                if distance < min_distance:
                    min_distance = distance
                    first_cluster = list(clusters.values())[cluster_first_index]
                    second_cluster = list(clusters.values())[cluster_second_index]

    return first_cluster, second_cluster


def count_middle_dot_by_cluster(cluster):
    count_x = 0
    count_y = 0
    for song in cluster:
        dot = song[1]
        count_x += dot[0]
        count_y += dot[1]
    return (count_x/len(cluster), count_y/len(cluster))

if __name__ == '__main__':
    clusters = read_file_and_get_elements('spotifyTop.csv')
    del clusters[(50, 2019)]

    with open('clusters_output.txt', 'w') as f:
        while len(clusters.keys()) != 1:
            first_cluster, second_cluster = get_best_clusters_to_merge(clusters)
            new_cluster = first_cluster + second_cluster

            for key, value in clusters.items():
                if value == first_cluster:
                    del clusters[key]
                    break

            for key, value in clusters.items():
                if value == second_cluster:
                    del clusters[key]
                    break

            clusters[count_middle_dot_by_cluster(new_cluster)] = new_cluster

            f.write(f"clusters{len(clusters)} = {clusters}")
            f.write('\n')

            print(len(clusters))






