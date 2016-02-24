from csv import reader
import re
import os


def date_filter_scheduled(date):
    """
    Given a date (between Oct 1st and Oct 7th), scheduled arrival data is
    filtered by date and put into the appropriate folder.
    """
    f_r = file('san-francisco/scheduled-arrivals.csv', 'r')
    f_w = file('sf_oct_%d/scheduled-arrivals.csv' % date, 'w')

    header = f_r.next()
    f_w.write(header)

    date_exists = False

    csv_f_r = reader(f_r)
    for line in csv_f_r:
        if (line[5].startswith('10/%d/2012' % date)):
            date_exists = True
            f_w.write(','.join(line))
            f_w.write('\n')

    f_r.close()
    f_w.close()

    print "Does %d exist? %d" % (date, date_exists)


def date_filter_realtime(date):
    """
    Given a date (between Oct 1st and Oct 7th), realtime arrival data is
    filtered by date and put into the appropriate folder.
    """
    f_r = file('san-francisco/realtime-arrivals.csv', 'r')
    f_w = file('sf_oct_%d/realtime-arrivals.csv' % date, 'w')

    header = f_r.next()
    f_w.write(header)

    date_exists = False

    csv_f_r = reader(f_r)
    for line in csv_f_r:
        if (line[9].startswith('10/%d/2012' % date)):
            date_exists = True
            f_w.write(','.join(line))
            f_w.write('\n')

    f_r.close()
    f_w.close()

    print "Does %d exist? %d" % (date, date_exists)


def date_filter_passenger(date):
    """
    Given a date (between Oct 1st and Oct 7th), passenger data is filtered by
    date and put into the appropriate folder.
    """
    f_r = file('san-francisco/passenger-count.csv', 'r')
    f_w = file('sf_oct_%d/passenger-count.csv' % date, 'w')

    header = f_r.next()
    f_w.write(header)

    date_exists = False

    csv_f_r = reader(f_r)
    for line in csv_f_r:
        if (line[7] == '%d' % date):
            date_exists = True
            f_w.write(','.join(line))
            f_w.write('\n')

    f_r.close()
    f_w.close()

    print "Does %d exist? %d" % (date, date_exists)


def date_filter(date):
    """
    Given a date (between Oct 1st and Oct 7th), the data is partitioned by date
    and split into appropriate folders.
    """
    date_filter_scheduled(date)
    date_filter_realtime(date)
    date_filter_passenger(date)


def all_date_filter():
    """
    Filters (by date) the scheduled and realtime arrival data, and passenger
    data between Oct 1 and Oct 7.

    Does not generate folders for each date, but puts the appropriate files in
    each folder. An error will occur if the folder doesn't exist, and this
    error is not caught!
    """
    for date in range(1, 8):
        date_filter(date)


def sort_scheduled(date):
    """
    Given a date (between Oct 1st and Oct 7th), the scheduled arrival data is
    sorted. Sort priority is: route, trip id, longitude, latitude.
    """
    f_r = file('sf_oct_%d/scheduled-arrivals.csv' % date, 'r')
    f_w = file('sf_oct_%d/scheduled-arrivals-sorted.csv' % date, 'w')

    header = f_r.next()
    f_w.write(header)

    data = []

    csv_f_r = reader(f_r)
    for line in csv_f_r:
        data.append(line)
    f_r.close()

    data.sort(key=lambda x: (x[0], x[1], x[3], x[4]))
    for datum in data:
        f_w.write(','.join(datum))
        f_w.write('\n')
    f_w.close()



def sort_realtime(date):
    """
    Given a date (between Oct 1st and Oct 7th), the realtime arrival data is
    sorted. Sort priority is: route, trip id, longitude, latitude.
    """
    f_r = file('sf_oct_%d/realtime-arrivals.csv' % date, 'r')
    f_w = file('sf_oct_%d/realtime-arrivals-sorted.csv' % date, 'w')

    header = f_r.next()
    f_w.write(header)

    data = []

    csv_f_r = reader(f_r)
    for line in csv_f_r:
        data.append(line)
    f_r.close()

    data.sort(key=lambda x: (x[0], x[2], x[7], x[8]))
    for datum in data:
        f_w.write(','.join(datum))
        f_w.write('\n')
    f_w.close()


def my_sort(date):
    """
    Given a date (between Oct 1st and Oct 7th), the scheduled and realtime
    arrival data is sorted.
    """
    sort_scheduled(date)
    sort_realtime(date)


def all_sort():
    """
    Sorts the scheduled and realtime arrival data between Oct 1 and Oct 7.

    Generates the "sorted" files.
    """
    for date in range(1, 8):
        my_sort(date)


def combine_schedule_realtime_padded(date):
    """
    Given a date (between Oct 1st and Oct 7th), the scheduled and realtime
    arrival data is concatenated into "combined.csv".
    
    Since there are fewer realtime stops than there are scheduled stops,
    the realtime data will be padded so that all stops are contained within
    the generated data set. I don't even use the realtime stop data that isn't
    the realtime arrival... so to indicate padded stops, this value is 'NA'.
    """
    f_real = file('sf_oct_%d/realtime-arrivals-sorted.csv' % date, 'r')
    f_sched = file('sf_oct_%d/scheduled-arrivals-sorted.csv' % date, 'r')
    f_comb = file('sf_oct_%d/combined.csv' % date, 'w')

    csv_real = reader(f_real)
    csv_sched = reader(f_sched)

    header = csv_real.next()
    csv_sched.next()
    f_comb.write(','.join(header))
    f_comb.write(',SCHEDULED_ARRIVAL_TIME\n')

    while 1:
        try:
            # Get next 
            line = csv_real.next()
            route = line[0]
            trip_id = line[2]
            longitude = line[7]
            latitude = line[8]

            written = False

            while not written:
                try:
                    other = csv_sched.next()
                    if (other[0] == route and other[1] == trip_id and
                            other[3] == longitude and other[4] == latitude):
                        f_comb.write(','.join(line))
                        f_comb.write(',%s\n' % other[5])
                        written = True
                    else:
                        # Pad!! The last value of line is the realtime data, so
                        # just ignore that with line[:-1]
                        f_comb.write(','.join(line[:-1]))
                        f_comb.write(',NA')
                        f_comb.write(',%s\n' % other[5])

                except StopIteration:
                    print "Did not write %s" % ','.join(line)
                    break

        except StopIteration:
            break
    f_real.close()
    f_sched.close()
    f_comb.close()


def all_combine_schedule_realtime_padded():
    """
    Combines the scheduled and realtime arrival data between Oct 1 and Oct 7.

    Note: combines "sorted" files (this is really important!!), and generates
    "combined" files.
    """
    for date in range(1,8):
        combine_schedule_realtime_padded(date)


def combine_schedule_realtime(date):
    """
    Given a date (between Oct 1st and Oct 7th), the scheduled and realtime
    arrival data is concatenated into "combined.csv".

    Since I am limited by realtime data, this function matches the scheduled
    data to the real data and simply concatenates the scheduled time into the
    realtime-arrivals data.
    """
    f_real = file('sf_oct_%d/realtime-arrivals-sorted.csv' % date, 'r')
    f_sched = file('sf_oct_%d/scheduled-arrivals-sorted.csv' % date, 'r')
    f_comb = file('sf_oct_%d/combined.csv' % date, 'w')

    csv_real = reader(f_real)
    csv_sched = reader(f_sched)

    header = csv_real.next()
    csv_sched.next()
    f_comb.write(','.join(header))
    f_comb.write(',SCHEDULED_ARRIVAL_TIME\n')

    while 1:
        try:
            line = csv_real.next()
            route = line[0]
            trip_id = line[2]
            longitude = line[7]
            latitude = line[8]

            written = False

            while not written:
                try:
                    other = csv_sched.next()
                    if (other[0] == route and other[1] == trip_id and
                            other[3] == longitude and other[4] == latitude):
                        f_comb.write(','.join(line))
                        f_comb.write(',%s\n' % other[5])
                        written = True
                except StopIteration:
                    print "Did not write %s" % ','.join(line)
                    break

        except StopIteration:
            break
    f_comb.close()
    f_real.close()
    f_comb.close()


def all_combine_schedule_realtime():
    """
    Combines the scheduled and realtime arrival data between Oct 1 and Oct 7.

    Note: combines "sorted" files (this is really important!!), and generates
    "combined" files.
    """
    for date in range(1,8):
        combine_schedule_realtime(date)


def append_time_difference(date):
    """
    Given a date (between Oct 1st and Oct 7th), the value "dTIME" is appended
    to each line. dTIME is in seconds.

    If appending time_difference to a padded stop, just previous value or 0,
    if that doesn't exist.
    """
    f_r = file('sf_oct_%d/combined.csv' % date, 'r')
    f_w = file('sf_oct_%d/appended.csv' % date, 'w')

    csv_r = reader(f_r)
    header = csv_r.next()
    f_w.write(','.join(header))
    f_w.write(',dTIME\n')

    time_pattern = re.compile(
            '10/[0-9]/2012 ([0-9]+:[0-9]{2}:[0-9]{2})\.[0-9]{6} ([PA])M')

    previous_val = 0
    curr_trip = ''
    for line in csv_r:
        # is this a new trip? If yes, reset previous_val to 0
        if line[2] != curr_trip:
            curr_trip = line[2]
            previous_val = 0

        t_sched_raw = time_pattern.match(line[10])
        t_real_raw = time_pattern.match(line[9])

        try:
            if t_real_raw:
                time_sched = convert_time_to_sec(t_sched_raw.groups())
                time_real = convert_time_to_sec(t_real_raw.groups())
                dTIME = time_real - time_sched
                previous_val = dTIME
            else:
                dTIME = previous_val
        except Exception as e:
            print e
            print "Invalid time format!"
            print line

        f_w.write(','.join(line))
        f_w.write(',%d\n' % dTIME)
    f_r.close()


def convert_time_to_sec(time):
    """
    Converts a time into the number of seconds since midnight.

    time must be of the format (XX:XX:XX, Y) where X are in 0-9 and Y is either
    A or P.
    """
    is_night_time = time[1] == 'P'
    time = time[0].split(':')
    hours = int(time[0])
    minutes = int(time[1])
    seconds = int(time[2])
    if is_night_time:
        hours += 12

    return hours*60*60 + minutes*60 + seconds


def all_append_time_difference():
    """
    Appends the difference (in seconds) between the scheduled and realtime
    arrival data between Oct 1 and Oct 7.

    Note: appends to the "combined" files, and generates "appended" files.
    """
    for day in range(1,8):
        append_time_difference(day)


def route_filter(date):
    """
    Given a date (between Oct 1st and Oct 7th), the "appended" file for that
    date is partitioned (by routes) into (route).csv, where route is the name
    of the route.
    """
    f_r = file('sf_oct_%d/appended.csv' % date, 'r')
    header = f_r.next()
    csv_r = reader(f_r)

    route = ''
    f_w = file('temp.tmp', 'w')
    for line in csv_r:
        next_route = line[0]
        if route != next_route:
            f_w.close()
            f_w = file('sf_oct_%d/routes/%s.csv' % (date, next_route), 'w')
            f_w.write(header)
            route = next_route
        f_w.write(','.join(line))
        f_w.write('\n')
    f_w.close()
    f_r.close()

def all_route_filter():
    """
    Assuming that the transit data has already been partitioned by day,
    has been sorted appropriately, has had the scheduled and realtime
    arrival times combined in "combined" files, and has had the time difference
    appended in "appended" files, this data is partitioned by the route!
    """
    for day in range(1, 8):
        route_filter(day)


def simplify_route_data(date):
    time_pattern = re.compile(
            '10/[0-9]/2012 ([0-9]+:[0-9]{2}:[0-9]{2})\.[0-9]{6} ([PA])M')

    for filename in os.listdir(os.getcwd() + '/sf_oct_%d/routes/' % date):
        f_r = file('sf_oct_%d/routes/%s' % (date, filename), 'r')
        f_w = file('sf_oct_%d/routes_simplified/%s' % (date, filename), 'w')

        # throw away header and write my own!
        f_r.next()
        f_w.write('route,trip,longitude,latitude,scheduled_time,d_time\n')

        csv_r = reader(f_r)
        for line in csv_r:
            t_sched_raw = time_pattern.match(line[10])
            try:
                sched_time = convert_time_to_sec(t_sched_raw.groups())
            except:
                print "Invalid time format"

            f_w.write(
                    '%s,%s,%s,%s,%d,%s\n' %
                    (line[0], line[1], line[7], line[8], sched_time, line[11])
            )

        f_r.close()
        f_w.close()


def all_simplify_route_data():
    for date in range(1, 8):
        simplify_route_data(date)


if __name__ == '__main__':
    all_append_time_difference()
    all_route_filter()
    all_simplify_route_data()
