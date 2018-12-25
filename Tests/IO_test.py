score = 251

def save_best():  # saves the best score
    temp_score = score
    with open("data_test.txt", "r+") as data_file:
        prev_best_score = int(data_file.read()[:3])
        nr_char = len(str(temp_score))

        if nr_char == 1:
            seek = 2
        elif nr_char == 2:
            seek = 1
        else:
            seek = 0

        if temp_score > prev_best_score:
            data_file.seek(seek)
            data_file.write(str(temp_score))
            return temp_score
        else:
            return prev_best_score

def statistics():  # saves how many times the user has played
    with open("data_test.txt", "r+") as data_file:
        prev_times_played = int(data_file.read()[4:])
        prev_times_played += 1
        data_file.seek(4)
        data_file.write(str(prev_times_played))
        return prev_times_played

save_best()
statistics()