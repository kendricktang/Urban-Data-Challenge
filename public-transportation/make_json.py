from csv import reader
import os


def convert_to_json(date, route):
    f_csv = file('sf_oct_%d/routes_simplified/%s.csv' % (date, route), 'r')
    f_json = file('sf_oct_%d/json/%s.json' % (date, route), 'w')

    # throw away header
    f_csv.next()

    reader_f = reader(f_csv)

    # Write initial entry!
    f_json.write('route_%s = {\n' % route)
    first_line = reader_f.next()
    curr_trip = first_line[1]
    start_time = first_line[4]
    longitude = first_line[2]
    latitude = first_line[3]
    d_time = first_line[5]
    f_json.write('\t%s: {\n' % curr_trip)
    f_json.write('\t\tstart: %s,\n' % start_time)
    f_json.write('\t\tdata: [\n')
    f_json.write('\t\t\t{\n')
    f_json.write('\t\t\t\troute: %s,\n' % route)
    f_json.write('\t\t\t\ttrip: %s,\n' % curr_trip)
    f_json.write('\t\t\t\ttime: %s,\n' % start_time)
    f_json.write('\t\t\t\tlongitude: %s,\n' % longitude)
    f_json.write('\t\t\t\tlatitude: %s,\n' % latitude)
    f_json.write('\t\t\t\td_time: %s,\n' % d_time)
    f_json.write('\t\t\t},\n')

    for line in reader_f:
        trip = line[1]
        start_time = line[4]
        longitude = line[2]
        latitude = line[3]
        d_time = line[5]

        # End the curr_trip, and begin a new one!
        if trip != curr_trip:
            curr_trip = trip
            f_json.write('\t},\n')
            f_json.write('\t%s: {\n' % curr_trip)
            f_json.write('\t\tstart: %s,\n' % start_time)
            f_json.write('\t\tdata: [\n')

        # Write the trip-stop datum!
        f_json.write('\t\t\t{\n')
        f_json.write('\t\t\t\troute: %s,\n' % route)
        f_json.write('\t\t\t\ttrip: %s,\n' % curr_trip)
        f_json.write('\t\t\t\ttime: %s,\n' % start_time)
        f_json.write('\t\t\t\tlongitude: %s,\n' % longitude)
        f_json.write('\t\t\t\tlatitude: %s,\n' % latitude)
        f_json.write('\t\t\t\td_time: %s,\n' % d_time)
        f_json.write('\t\t\t},\n')

    f_json.write('}')
    f_json.close()


def convert_many_to_json(date):
    for filename in os.listdir(
            os.getcwd() + '/sf_oct_%d/routes_simplified/' % date):
        convert_to_json(date, filename[0:-4])


def convert_all_to_json():
    for date in range(1, 8):
        convert_many_to_json(date)


if __name__ == '__main__':
    convert_all_to_json()
