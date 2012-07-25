print("storing data in dictionaries")
with open("../data/kaggle_users.txt", "r") as file:
    users = {}
    index = 0
    for line in file:
        user_id = line.strip()
        index += 1
        users[user_id] = index

with open("../data/kaggle_songs.txt", "r") as file:
    songs = {}
    for line in file:
        song_id, index = line.strip().split(" ")
        songs[song_id] = int(index)

print("creating play_count")
play_count = {}
with open("../data/kaggle_visible_evaluation_triplets.txt", "r") as file:
    for line in file:
        user_id, song_id, count = line.strip().split("\t")
        if users[user_id] in play_count:
            play_count[users[user_id]][songs[song_id]] = int(count)
        else:
            play_count[users[user_id]] = {songs[song_id] : int(count)}

print("creating user_colisten")
user_colisten = {}
with open("../data/user_colisten.txt" , "r") as file:
    for line in file:
        temp_common_songs = []
        common_songs = []
        temp_common_songs = line.strip().split(" ")
    for song in temp_common_songs:
        common_songs.append(int(song))
        user_colisten[common_songs[0]] = common_songs[1:]

print("creating song_colisten")
song_colisten = {}
for user in play_count:
    for song1 in play_count[user]:
        for song2 in play_count[user]:
            if song1 in song_colisten and song2 in song_colisten[song1]:
                song_colisten[song1][song2] += 1
            elif song1 not in song_colisten:
                song_colisten[song1] = {song2 : 1}
            elif song2 not in song_colisten[song1]:
                song_colisten[song1][song2] = 1

print("creating sorted_diagonal")
sorted_diagonal = {}
for song1 in song_colisten:
    for song2 in song_colisten[song1].keys():
        if song1 == song2:
            sorted_diagonal[song1] = -song_colisten[song1][song2]
sorted_diagonal = sorted(sorted_diagonal, key=sorted_diagonal.get)

print("generating output for each user")
with open("../results/solution.txt", "w") as file:
    for user in play_count:
        user_songs = play_count[user]
        songs_ignored = list(user_songs.keys())
        colisten_row = {}
        index = 0
        while index < 500:
            if colisten_row == {}:
                if user_songs == {}:
                    for song in sorted_diagonal:
                        if index == 500:
                            break
                        elif song not in songs_ignored:
                            file.write(str(song) + " ")
                            index += 1
                    break
                recommendation = max(user_songs, key=user_songs.get)
                colisten_row = song_colisten[recommendation]
                del user_songs[recommendation]
                for song in songs_ignored:
                    if song in colisten_row:
                        del colisten_row[song]
                continue
            recommendation = max(colisten_row, key=colisten_row.get)
            songs_ignored.append(recommendation)
            file.write(str(recommendation) + " ")
            del colisten_row[recommendation]
            index += 1
        file.write("\n")

print("finished")