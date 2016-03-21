import csv
from keboola import docker


class App:
    def run(self):
        # initialize KBC configuration
        cfg = docker.Config()
        # validate application parameters
        parameters = cfg.get_parameters()
        text_max = parameters.get('max')
        text_min = parameters.get('min')
        id_dolumn = parameters.get('columns', {}).get('id')
        text_column = parameters.get('columns', {}).get('text')
        if text_min is None or text_min is None or id_dolumn is None or text_column is None:
            raise ValueError("max, min, columns.id and columns.text are required parameters.")
        id_prefix = parameters.get('id_prefix', '')

        # get input and output table and validate them
        tables = cfg.get_input_tables()
        if len(tables) != 1:
            raise ValueError("Input mapping must contain one table only.")
        in_table = tables[0]
        tables = cfg.get_expected_output_tables()
        if len(tables) != 1:
            raise ValueError("Output mapping must contain one table only.")
        out_table = tables[0]
        # physical location of the source file with source data
        in_file_path = in_table['full_path']
        # physical location of the target file with output data
        out_file_path = out_table['full_path']

        # validate columns in the input table
        with open(in_file_path, mode='rt', encoding='utf-8') as in_file:
            # handle null character
            lazy_lines = (line.replace('\0', '') for line in in_file)
            csv_reader = csv.DictReader(lazy_lines, dialect='kbc')
            row = next(csv_reader)
            if id_dolumn not in row or text_column not in row:
                raise ValueError("The source table does not contain columns {}, {}".format(id_dolumn, text_column))

        # read the input table and immediatelly write to the output table
        with open(in_file_path, mode='rt', encoding='utf-8') as in_file, open(out_file_path, mode='wt', encoding='utf-8') as out_file:
            writer = csv.DictWriter(out_file, fieldnames=['pk', 'id', 'row', 'text'], dialect='kbc')
            writer.writeheader()

            lazy_lines = (line.replace('\0', '') for line in in_file)
            csv_reader = csv.DictReader(lazy_lines, dialect='kbc')
            for row in csv_reader:
                # do the text splitting
                fragment_index = 0
                string_to_split = row[text_column]
                while len(string_to_split) > text_max:
                    fragment = string_to_split[:text_max + 1]
                    offset = fragment.rfind(' ')
                    if offset < text_min:
                        offset = text_min
                    fragment = string_to_split[:offset]
                    string_to_split = string_to_split[offset:]
                    # write output row
                    out_row = {
                        'pk': id_prefix + str(row[id_dolumn]) + '_' + str(fragment_index),
                        'id': row[id_dolumn],
                        'row': fragment_index,
                        'text': fragment
                    }
                    writer.writerow(out_row)
                    fragment_index += 1
                if len(string_to_split) > 0:
                    # write output row
                    out_row = {
                        'pk': id_prefix + str(row[id_dolumn]) + '_' + str(fragment_index),
                        'id': row[id_dolumn],
                        'row': fragment_index,
                        'text': string_to_split
                    }
                    writer.writerow(out_row)
        print("Splitting finished.")
