import datetime
import json
import pytz

INFILE = 'basis-data-2013-08-20.json'
OUTFILE = INFILE.replace('.json', '.log')


def write_out(outf, line):
    logline = ('%s' % line['timestamp'])
    for k, v in line.iteritems():
        if k != 'timestamp':
            logline = '%s, %s="%s"' % (logline, k, v)
    outf.write('%s\n' % logline)


def process_file(infile, outfile):
    outf = open(outfile, 'w')
    dj = json.load(open(infile))
    time_start = dj['timezone_history'][0]['start']
    tz = pytz.timezone(dj['timezone_history'][0]['timezone'])
    interval = dj['interval']
    for x in range(1440):
        line = {}
        timestamp = tz.localize(
            datetime.datetime.fromtimestamp(time_start + (x * interval)))
        line['timestamp'] = timestamp.isoformat()
        for y in ['air_temp', 'calories', 'gsr', 'heartrate',
                  'skin_temp', 'steps']:
            line[y] = dj['metrics'][y]['values'][x]
        write_out(outf, line)

if __name__ == "__main__":
    process_file(INFILE, OUTFILE)
