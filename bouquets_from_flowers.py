class FlowerFileStream(object):

    def __init__(self, file_path):
        try:
            self._file = open(file_path, 'r')
        except IOError:
            print('No file to read stream from in script folder')
            raise

    def next_value(self):
        return self._file.readline().strip()

    def close(self):
        self._file.close()
