import logging_manager
import toolkit_config
import toolkit_file

import os
import logging
import aria2p

from tqdm import tqdm

CONFIGFILE = 'config.ini'
TORRENT_DIR = 'torrents'
config = toolkit_config.read_config_general(CONFIGFILE)

host = config['aria client']['host']
port = config['aria client']['port']
secret = config['aria client']['secret']

aria2pClient = aria2p.client.Client(host=host, port=port, secret=secret)
aria2pAPI = aria2p.api.API(client=aria2pClient)


def add_torrent_task(torrent_file_path):
    logging.info('Adding task: ' + torrent_file_path)
    try:
        aria2pAPI.add_torrent(torrent_file_path)
    except Exception as e:
        logging.error('Adding task failed.')
    else:
        logging.info('Added task.')
        os.rename(torrent_file_path, torrent_file_path + '.added')


@logging_manager.logging_to_file
def batch_add_torrent_task():
    torrent_file_list = [file for file in toolkit_file.get_file_list(
        TORRENT_DIR) if file.endswith('.torrent')]
    logging.info('Found torrent: ')
    logging.info([toolkit_file.get_basename(x, withExtension=True)
                  for x in torrent_file_list])
    for torrent_file in tqdm(torrent_file_list, unit='Tasks'):
        add_torrent_task(torrent_file)


if __name__ == '__main__':
    batch_add_torrent_task()
