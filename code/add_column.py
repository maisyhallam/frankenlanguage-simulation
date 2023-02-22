import csv
import sys

def main(argv):
    for i in range(1000):
        i += 1
        with open('../data/' + argv + '/set' + str(i) + '.csv','r') as csvinput:
            with open('../data/' + argv + '/new/set' + str(i) + '.csv', 'w') as csvoutput:
                writer = csv.writer(csvoutput)

                for row in csv.reader(csvinput):
                    if row:
                        if row[0] == "LANGUAGE":
                            writer.writerow(row+["SET"])
                        else:
                            writer.writerow(row+[str(i)])

if __name__ == '__main__':
    main(sys.argv[1])
