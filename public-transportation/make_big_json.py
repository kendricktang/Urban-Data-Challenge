from csv import reader
import os
import json


def convert_to_big_json(date, route):
    f_csv = file('sf_oct_%d/routes_simplified/%s.csv' % (date, route), 'r')
    f_json = file('sf_oct_%d/big_json/%s.json' % (date, route), 'w')

    # throw away header
    f_csv.next()

    reader_f = reader(f_csv)

    curr_trip = ''
    last_time = 0
    data = []

    for line in reader_f:
        next_stop = {
            "trip": line[1],
            "time": int(line[4]),
            "longitude": float(line[2]),
            "latitude": float(line[3]),
            "d_time": int(line[5]),
            "size": 10,
            "route": route
        }

        if ((next_stop["trip"] == curr_trip) and
                (abs(next_stop["time"] - last_time) < 40 * 60)):  # Add this stop to the curr trip!
            data[-1].append(next_stop)
            last_time = next_stop["time"]
        else:  # End the old trip, start new trip, add this stop to new trip.
            # End old trip, if there is an old trip to end
            if data:
                last_stop = data[-1][-1].copy()
                last_stop["size"] = 0
                last_stop["time"] += 10 * 60
                data[-1].append(last_stop)

            # Create new trip
            curr_trip = next_stop["trip"]
            first_stop = next_stop.copy()
            first_stop["size"] = 0
            data.append([first_stop])

            # Add next stop to new trip
            data[-1].append(next_stop)
            last_time = next_stop["time"]

    # END THE LAST TRIP!!!
    last_stop = data[-1][-1].copy()
    last_stop["size"] = 0
    last_stop["time"] += 10 * 60
    data[-1].append(last_stop)

    f_json.write(json.dumps(data))

    f_csv.close()
    f_json.close()


def convert_many_to_big_json(date):
    for filename in os.listdir(
            os.getcwd() + '/sf_oct_%d/routes_simplified/' % date):
        convert_to_big_json(date, filename[0:-4])


def convert_all_to_big_json():
    for date in range(1, 8):
            convert_many_to_big_json(date)


if __name__ == "__main__":
    # convert_to_big_json(1, '01')
    # convert_many_to_big_json(1)
    convert_all_to_big_json()
