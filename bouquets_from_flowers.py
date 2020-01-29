import argparse
import re
from collections import Counter


class FlowerFileStream(object):
    """
    This class wraps file object. Allows to work with file as a stream.
    """

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
    """
        This class designed to consume stream of designs and flowers
        and generate output of bouquet.
    """

    bouquet_design_pattern = '^([A-Z])([LS])((?:\d+[a-z])+)(\d+)$'
    flowers_pattern = '(\d+)([a-z])'

    def __init__(self, stream):
        self.stream = stream
        self.bouquet_designs = {'L': [], 'S': []}
        self.total_count = {'S': 0, 'L': 0}
        self.flowers = {'S': Counter(), 'L': Counter()}

    def parse_bouquet_design(self, bouquet_design):
        """
        Parses bouquet design string. Saves bouquet data.
        :param bouquet_design: bouquet design string.
        :return: Nothing.
        """

        match = re.match(self.bouquet_design_pattern, bouquet_design)

        if not match:
            print(f'{bouquet_design} is not a valid design')

        bouquet_name, size, flowers_str, total = match.groups()

        flowers = re.findall(self.flowers_pattern, flowers_str)
        flowers_dict = {}

        certain_amount = 0
        for amount, name in flowers:
            amount = int(amount)
            flowers_dict[name] = amount
            certain_amount += amount

        total = int(total)
        any_amount = total - certain_amount

        self.bouquet_designs[size].append({
            'flowers': Counter(flowers_dict),
            'total': total,
            'any': any_amount,
            'name': bouquet_name,
        })

    def get_bouquet_designs(self):
        """
        Gets design strings from stream and processes them
        until reaches empty line.
        :return: Nothing.
        """

        while True:
            design = self.stream.next_value()

            if not design:
                return

            self.parse_bouquet_design(design)

    def get_design(self, flower, size):
        """
        Checks if any boquet is ready to be created using the latest flower.
        :param flower: flower name.
        :param flower: flower size.
        :return: design for boquet that is ready.
        """
        
        for design in self.bouquet_designs[size]:
            if (
                flower in design['flowers'] and
                design['total'] <= self.total_count[size]
            ):
                if design['flowers'] == design['flowers'] & self.flowers[size]:
                    return design

    def create_bouquet(self, design, size):
        """
        Create boquet from give desing. Update internal storage of flowers.
        :param design: design dict with design data.
        :param size: size of flowers we are working with.
        :return: created boquet
        """
        
        bouquet = Counter(design['flowers'])
        flowers = self.flowers[size]
        flowers -= bouquet

        left = design['any']
        if left:
            for flower_name, amount in flowers.items():
                if amount >= left:
                    bouquet[flower_name] += left
                    flowers[flower_name] = amount - left
                    break
                else:
                    bouquet[flower_name] += amount
                    flowers[flower_name] = 0
                    left -= amount

        self.total_count[size] -= design['total']

        bouquet_flowers = ''.join(
            [f'{name}{amount}' for name, amount in bouquet.items()],
        )
        bouquet_str = design['name'] + size + bouquet_flowers

        return bouquet_str

    def stop(self):
        """
        Stop processing. Signal stream that processing stopped
        :return: Nothing
        """
        
        self.stream.close()

    def start(self):
        """
        Processing entry point. Starts and runs consuming flow.
        :return: Nothing
        """
        
        self.get_bouquet_designs()
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
                bouquet = self.create_bouquet(design, size)
                print(bouquet)  # TODO: send to output stream


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
