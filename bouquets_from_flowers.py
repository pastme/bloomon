import re
from collections import Counter

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


class BouquetProcessor(object):
    boquet_design_pattern = '^([A-Z])([LS])((?:\d+[a-z])+)(\d+)$'
    flowers_pattern = '(\d+)([a-z])'

    def __init__(self, file_path='sample.txt'):
        self.stream = FlowerFileStream(file_path)
        self.boquet_designs = {'L': [], 'S': []}
        self.total_count = {'S': 0, 'L': 0}
        self.flowers = {'S': Counter(), 'L': Counter()}

    def match_boquets(self, boquet_design):
        match = re.match(self.boquet_design_pattern, boquet_design)

        if not match:
            print(f'{boquet_design} is not a valid design')

        boquet_name, size, flowers_str, total = match.groups()

        flowers = re.findall(self.flowers_pattern, flowers_str)
        flowers_dict = {}

        certain_amount = 0
        for amount, name in flowers:
            amount = int(amount)
            flowers_dict[name] = amount
            certain_amount += amount

        total = int(total)
        any_amount = total - certain_amount

        self.boquet_designs[size].append({
            'flowers': Counter(flowers_dict),
            'total': total,
            'any': any_amount,
            'name': boquet_name,
        })

    def get_boquet_designs(self):
        while True:
            design = self.stream.next_value()

            if not design:
                return

            self.match_boquets(design)
