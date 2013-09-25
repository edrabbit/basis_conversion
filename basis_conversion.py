import argparse
import datetime
import glob
import json
import os
import pytz


def write_out(outf, line):
    logline = ('%s' % line['timestamp'])
    for k, v in line.iteritems():
        if k != 'timestamp':
            if not v:
                logline = '%s, %s=""' % (logline, k)
            else:
                logline = '%s, %s="%s"' % (logline, k, v)
    outf.write('%s\n' % logline)


def process_file(infile, outf):
    '''infile is a path, outf is a file object'''

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

def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert Basis json data into timestamped log files')
    parser.add_argument(
        '-d', '--dir', type=str, help='Directory of json files', default='.')
    parser.add_argument(
        '-o', '--output', type=str, help='File to write to',
        default='output.log')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    outf = open(args.output, 'a')
    files = glob.glob(os.path.join(args.dir, '*.json'))
    for f in files:
        print 'Processing %s' % f
        process_file(f, outf)
    outf.close()
