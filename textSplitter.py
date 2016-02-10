from keboola import docker
import csv

class App:
    def run(self):
        # initialize KBC configuration 
        cfg = docker.Config()
        # validate application parameters
        parameters = cfg.getParameters()
        textMax = parameters.get('max')
        textMin = parameters.get('min')
        idColumn = parameters.get('columns').get('id')
        textColumn = parameters.get('columns').get('text')
        if (textMin == None or textMin == None or idColumn == None or textColumn == None):
            raise ValueError("max, min, columns.id and columns.text are required parameters.")
        idPrefix = parameters.get('idPrefix', '')
        incremental = parameters.get('incremental', 0)

        # get input and output table and validate them
        tables = cfg.getInputTables()
        if (len(tables) != 1):
            raise ValueError("Input mapping must contain one table only.")
        inTable = tables[0]
        tables = cfg.getExpectedOutputTables()
        if (len(tables) != 1):
            raise ValueError("Output mapping must contain one table only.")
        outTable = tables[0]
        # physical location of the source file with source data
        inFilePath = inTable['full_path']
        # physical location of the target file with output data
        outfilePath = outTable['full_path']

        # validate columns in the input table        
        with open(inFilePath, mode='rt', encoding='utf-8') as inFile:
            # handle null character
            lazyLines = map(lambda line: line.replace('\0', ''), inFile)
            csvReader = csv.DictReader(lazyLines, dialect='kbc')
            row = next(csvReader)
            if ((idColumn not in row) or (textColumn not in row)):
                raise ValueError("The source table does not contain columns " + idColumn + ", " + textColumn)

        # read the input table and immediatelly write to the output table
        with open(inFilePath, mode='rt', encoding='utf-8') as inFile, open(outfilePath, mode='wt', encoding='utf-8') as outFile:
            writer = csv.DictWriter(outFile, fieldnames = ['pk', 'id', 'row', 'text'], dialect='kbc')
            writer.writeheader()

            lazyLines = map(lambda line: line.replace('\0', ''), inFile)
            csvReader = csv.DictReader(lazyLines, dialect='kbc')
            for row in csvReader:
                # do the text splitting
                fragmentIndex = 0
                stringToSplit = row[textColumn]
                while (len(stringToSplit) > textMax):
                    fragment = stringToSplit[:textMax+1]
                    offset = fragment.rfind(' ')
                    if (offset < textMin):
                        offset = textMin
                    fragment = stringToSplit[:offset]
                    stringToSplit = stringToSplit[offset:]
                    # write output row
                    outRow = {
                        'pk': idPrefix + str(row[idColumn]) + '_' + str(fragmentIndex),
                        'id': row[idColumn],
                        'row': fragmentIndex,
                        'text': fragment
                    }
                    writer.writerow(outRow)
                    fragmentIndex += 1
                if len(stringToSplit) > 0:
                    # write output row
                    outRow = {
                        'pk': idPrefix + str(row[idColumn]) + '_' + str(fragmentIndex),
                        'id': row[idColumn],
                        'row': fragmentIndex,
                        'text': stringToSplit
                    }
                    writer.writerow(outRow)
        print("Splitting finished.")
