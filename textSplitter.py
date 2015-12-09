# coding=utf-8
from keboola import docker
import csv

class App:
    def run(self):
        cfg = docker.Config()
        # validate parameters
        parameters = cfg.getParameters()
        textMax = parameters.get('max')
        textMin = parameters.get('min')
        idColumn = parameters.get('columns').get('id')
        textColumn = parameters.get('columns').get('text')
        if (textMin == None or textMin == None or idColumn == None or textColumn == None):
            raise ValueError("max, min, columns.id and columns.text are required parameters.")
        idPrefix = parameters.get('idPrefix', '')
        incremental = parameters.get('incremental', 0)

        # get input and utput table
        tables = cfg.getInputTables()
        if (len(tables) != 1):
            raise ValueError("Input mapping must contain one table only.")
        inTable = tables[0]
        tables = cfg.getExpectedOutputTables()
        if (len(tables) != 1):
            raise ValueError("Output mapping must contain one table only.")
        outTable = tables[0]
        inFilePath = inTable['full_path']
        outfilePath = outTable['full_path']
        
        with open(inFilePath, 'rt') as inFile:
            lazyLines = map(lambda line: line.replace('\0', ''), inFile)
            csvReader = csv.DictReader(lazyLines, delimiter = ',', quotechar = '"')
            row = next(csvReader)
            print(row)            
            if ((idColumn not in row) or (textColumn not in row)):
                raise ValueError("The source table does not contain columns " + idColumn + ", " + textColumn)

        with open(inFilePath, 'rt') as inFile, open(outfilePath, 'wt') as outFile:
            writer = csv.DictWriter(outFile, fieldnames = ['pk', 'id', 'row', 'text'], lineterminator='\n', delimiter = ',', quotechar = '"')
            writer.writeheader()

            lazyLines = map(lambda line: line.replace('\0', ''), inFile)
            csvReader = csv.DictReader(lazyLines, delimiter = ',', quotechar = '"')
            for row in csvReader:
                fragmentIndex = 0
                stringToSplit = row[textColumn]
                while (len(stringToSplit) > textMax):
                    fragment = stringToSplit[:textMax+1]
                    offset = fragment.rfind(' ')
                    if (offset < textMin):
                        offset = textMin
                    fragment = stringToSplit[:offset]
                    stringToSplit = stringToSplit[offset:]
                    outRow = {
                        'pk': idPrefix + str(row[idColumn]) + '_' + str(fragmentIndex),
                        'id': row[idColumn],
                        'row': fragmentIndex,
                        'text': fragment
                    }
                    fragmentIndex += 1
                    writer.writerow(outRow)
                if len(stringToSplit) > 0:
                    print(stringToSplit)
                    outRow = {
                        'pk': idPrefix + str(row[idColumn]) + '_' + str(fragmentIndex),
                        'id': row[idColumn],
                        'row': fragmentIndex,
                        'text': stringToSplit
                    }
                    writer.writerow(outRow)
        print("Splitting finished.")
