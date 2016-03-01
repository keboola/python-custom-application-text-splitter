import text_splitter
import os
import csv


class TestTextSplitter:
    def test_text_splitter(self, data_dir):
        data_dir = os.getenv('KBC_DATA_DIR')
        app = text_splitter.App()
        app.run()

        assert(os.path.isfile(data_dir + '/out/tables/result.csv'))
        sample_data = []
        with open(data_dir + '/sample-result.csv', 'rt') as sample:
            csv_reader = csv.DictReader(sample, delimiter=',', quotechar='"')
            for row in csv_reader:
                sample_data.append(row)

        result_data = []
        with open(data_dir + '/out/tables/result.csv', 'rt') as sample:
            csv_reader = csv.DictReader(sample, delimiter=',', quotechar='"')
            for row in csv_reader:
                result_data.append(row)

        assert(sample_data == result_data)
