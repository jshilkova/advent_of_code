import argparse
from pathlib import Path


def get_races():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with Path(args.path).open() as f:
        times = f.readline().split(':')[1].strip().split(' ')
        times = [int(x) for x in times if x != '']
        distances = f.readline().split(':')[1].strip().split(' ')
        distances = [int(x) for x in distances if x != '']
    races = list(zip(times, distances))
    return races

def get_distance(start_acceleration_time, race_time):
    speed = 0
    for t in range(0, start_acceleration_time):
        speed += 1
    return speed * (race_time - start_acceleration_time)


def get_number_of_times_to_beat_record(time, race_time, record):
    number = 0
    for t in range(time, -1, -1):
        if get_distance(t, race_time) > record:
            number += 1
        else:
            break
    return number


def main():
    races = get_races()
    final_number = 1
    for race in races:
        time = race[0]
        distance = race[1]
        if time % 2 == 0:
            number = 2 * get_number_of_times_to_beat_record(int((time - 1) / 2), time, distance) + 1
        else:
            number = 2 * get_number_of_times_to_beat_record(int(time / 2), time, distance)
        final_number *= number

    print(final_number)
if __name__ == "__main__":
    main()
