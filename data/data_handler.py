import csv
import pickle

pickle_file = "data/datap"

# Load data in to memory
with open(pickle_file, 'rb') as file:
    data = pickle.load(file)


def get_log_channel(serverID: int) -> int or None:
    if serverID in data:
        return data[serverID]
    else:
        return None


# initialize guild without knowing channel ID
def init(server_id: int) -> None:
    data[server_id] = 0
    with open(pickle_file, 'wb') as file:
        pickle.dump(data, file)


def set_log_channel(server_id: int, channel_id: int) -> None:
    data[server_id] = channel_id
    with open(pickle_file, 'wb') as file:
        pickle.dump(data, file)
