import time
import generator
import processor


if __name__ == '__main__':
    M = 2
    N = 10
    dT = 0.3
    start = time.time()
    generator.create_incidents(M, N, 'csv/incidents.csv')
    #generator.create_incidents2(M, N, 'csv/incidents.csv')
    end = time.time()
    print('Generation finished, elapsed:', end - start)

    start = time.time()
    processor.process_incidents(input_filename='csv/incidents.csv', output_filename='csv/incidents_count.csv', dT=dT)
    end = time.time()
    print('Processing finished, elapsed:', end - start)
