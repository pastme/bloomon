import argparse
import re
from collections import Counter


class FlowerFileStream(object):

    def __init__(self, file_path):
        try:
            self._file = open(file_path, 'r')
        except FileNotFoundError:
            print(f'Can not find file {file_path}')
            raise ValueError('Not valid filepath')

    def next_value(self):
        return self._file.readline().strip()

    def close(self):
        self._file.close()


class BouquetProcessor(object):
    boquet_design_pattern = '^([A-Z])([LS])((?:\d+[a-z])+)(\d+)$'
    flowers_pattern = '(\d+)([a-z])'

    def __init__(self, stream):
        self.stream = stream
        self.boquet_designs = {'L': [], 'S': []}
        self.total_count = {'S': 0, 'L': 0}
        self.flowers = {'S': Counter(), 'L': Counter()}

    def parse_boquet_design(self, boquet_design):
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

            self.parse_boquet_design(design)

    def get_design(self, flower, size):
        for design in self.boquet_designs[size]:
            if (
                flower in design['flowers'] and
                design['total'] <= self.total_count[size]
            ):
                if design['flowers'] == design['flowers'] & self.flowers[size]:
                    return design

    def create_boquet(self, design, size):
        boquet = Counter(design['flowers'])
        self.flowers[size] -= boquet

        left = design['any']
        if left:
            for flower_name, amount in self.flowers[size].items():
                if amount >= left:
                    boquet[flower_name] += left
                    self.flowers[size][flower_name] = amount - left
                    break
                else:
                    boquet[flower_name] += amount
                    self.flowers[size][flower_name] = 0
                    left -= amount

        self.total_count[size] -= design['total']

        boquet_flowers = ''.join(
            [f'{name}{amount}' for name, amount in boquet.items()],
        )
        boquet_str = design['name'] + size + boquet_flowers

        return boquet_str

    def stop(self):
        self.stream.close()

    def start(self):
        self.get_boquet_designs()
        while True:
            flower_data = self.stream.next_value()
            if not flower_data:
                print('Stream stopped')
                return

            elif len(flower_data) != 2:
                print('Not valid flower input')
                continue

            flower = flower_data[0]
            size = flower_data[1]

            self.total_count[size] += 1
            self.flowers[size][flower] += 1

            design = self.get_design(flower, size)
            if design:
                boquet = self.create_boquet(design, size)
                print(boquet)


def main(path):
    stream = FlowerFileStream(path)
    stream_processor = BouquetProcessor(stream)
    stream_processor.start()
    stream_processor.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Process stream of flowers from specified file',
    )
    parser.add_argument(
        '--path',
        type=str,
        help='filepath for stream file',
        default='stream.txt',
    )
    args = parser.parse_args()
    main(args.path)
