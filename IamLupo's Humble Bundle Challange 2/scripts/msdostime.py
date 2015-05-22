from datetime import datetime
def dos_time_to_datetime(date, time):
    # little endian to big endian
    date = (date[1] << 8) + date[0]
    time = (time[0] << 0x10) + time[1]
    year = ((date & 0xFE00) >> 9) + 1980
    month = (date & 0x1E0) >> 5
    day = date & 0x1F
    hours = (time & 0xF800) >> 11
    mins = (time & 0x7E0) >> 5
    secs = (time & 0x1F) << 1

    return datetime(year, month, day, hours, mins, secs)

def time_and_date(d):
    t = d.timetuple()
    time = (t.tm_hour << 11) + (t.tm_min << 5) + (t.tm_sec/2)
    date = ((t.tm_year-1980) << 9) + (t.tm_mon << 5) + (t.tm_mday)
    return [ time&0xFF, (time&0xFF00) >> 8, date&0xFF, (date&0xFF00) >> 8]

time = [0x3a, 0x80]
date = [0xEF, 0xF0]
print(dos_time_to_datetime(date, time))

d = datetime.strptime( "2014-09-16 07:20:00", "%Y-%m-%d %H:%M:%S")
print(["{:02x}".format(h) for h in time_and_date(d)[2:]])  # only output date
