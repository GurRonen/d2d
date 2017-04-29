import csv
import json
import flatten_json
import click


@click.command()
@click.argument('input', type=click.File('r'))
@click.argument('output', type=click.File('wb+'))
@click.option('--i', default='json', help='the input format, defaults to json')
@click.option('--o', default='csv', help='the output format, defaults to csv')
def command(input, output, i, o):
    raw_array = input_to_array(i, input)
    array_to_output(o, output, raw_array)


def input_to_array(datatype, data):
    return {
        'json': lambda x: json_input(x),
        'csv': lambda x: csv_input(x)
    }.get(datatype)(data)


def json_input(data_file):
    return map(lambda x: flatten_json.flatten(x), json.loads(data_file.read()))


def csv_input(data_file):
    csv_reader = csv.reader(data_file)
    headers = csv_reader.next()

    data_array = []

    for row in csv_reader:
        dict = {}
        for i in range(0, len(row)):
            dict[headers[i]] = row[i]
        data_array.append(dict)

    return data_array


def array_to_output(datatype, output_file, array):
    return {
        'json': lambda x, file: file.write(json.dumps(array)),
        'csv': lambda x, file: csv_output(x, file)
    }.get(datatype)(array, output_file)


def csv_output(data, file):
    csv_writer = csv.writer(file)
    first_row = data[0]
    csv_writer.writerow(first_row.keys())

    for row in data:
        csv_writer.writerow(row.values())


if __name__ == '__main__':
    command()
