"""
@author shattang
"""
import os
import time

class LocalTopicStorage(object):
    def __init__(self, root_dir):
        self.root_dir = os.path.abspath(os.path.expanduser(root_dir))

    def get_topic_data(self, topic, **kwargs):
        key = kwargs.get('key', None) #type: str
        path = topic.split(".") #type: list
        os_path = os.path.join(self.root_dir, *path)
        ret = {}

        if not os.path.isdir(os_path):
            return ret

        filenames = os.listdir(os_path)
        for filename in filenames:
            if not filename.endswith(".dat"):
                continue
            filekey = filename.split(".")[0]
            if key and key != filekey:
                continue
            filepath = os.path.join(os_path, filename)
            with open(filepath, "rb") as f:
                ret[filekey] = f.read()
        return ret

    def store_topic_data(self, topic, data, **kwargs):
        key = kwargs.get('key', str(int(time.time()*1000*1000)))  # type: str
        path = topic.split(".")  # type: list
        os_path = os.path.join(self.root_dir, *path)

        if os.path.isfile(os_path):
            return False

        if not os.path.exists(os_path):
            os.makedirs(os_path)

        filepath = os.path.join(os_path, ".".join([key, "dat"]))
        with open(filepath, "wb") as f:
            f.write(data)
        return True

if __name__ == "__main__":
    lts = LocalTopicStorage("~/.data")
    lts.store_topic_data("exchange.trades", "sometrade1")
    lts.store_topic_data("exchange.trades", "sometrade2")
    lts.store_topic_data("exchange.quotes", "somequote1")
    print lts.get_topic_data("exchange.trades")
    print lts.get_topic_data("exchange.quotes")

