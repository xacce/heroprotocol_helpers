from heroprotocol.mpyq import mpyq
from heroprotocol import protocol29406
import importlib
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--dest')
parser.add_argument('--player')
parser.add_argument('--hero')
parser.add_argument('--map')
args = parser.parse_args()

print 'Search player %s - %s on %s: ' % (args.player, args.hero, args.map)
for p, dirs, files in os.walk(args.dest):
    for f in files:
        if not f.split('.')[-1] == 'StormReplay':
            continue

        fp = os.path.join(p, f)
        archive = mpyq.MPQArchive(fp)

        contents = archive.header['user_data_header']['content']
        header = protocol29406.decode_replay_header(contents)
        baseBuild = header['m_version']['m_baseBuild']

        protocol = importlib.import_module('heroprotocol.protocol%s' % baseBuild)
        contents = archive.read_file('replay.details')
        details = protocol.decode_replay_details(contents)
        if details['m_title'] == args.map:
            for player_data in details['m_playerList']:
                if player_data['m_hero'] == args.hero and player_data['m_name'] == args.player:
                    print '\t', fp
