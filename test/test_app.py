import textSplitter
import os
import csv

class TestTextSplitter:
    def test_textSplitter(self, dataDir):
        dataDir = os.getenv('KBC_DATA_DIR')        
        app = textSplitter.App()
        app.run()
        
        assert(os.path.isfile(dataDir + '/out/tables/result.csv'))
        sampleData = []
        with open(dataDir + '/sample-result.csv', 'rt') as sample:
            csvReader = csv.DictReader(sample, delimiter = ',', quotechar = '"')
            for row in csvReader:
                sampleData.append(row)
                
        resultData = []
        with open(dataDir + '/out/tables/result.csv', 'rt') as sample:
            csvReader = csv.DictReader(sample, delimiter = ',', quotechar = '"')
            for row in csvReader:
                resultData.append(row)

        assert(sampleData == resultData)
