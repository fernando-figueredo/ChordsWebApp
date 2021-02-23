import sys
from neural_network.spliter import Spliter

song_file = sys.argv[1]

spliter = Spliter(song_file)
spliter.save_split()