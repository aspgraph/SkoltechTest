import time
import generator
import processor


# Входная точка программы
if __name__ == '__main__':
    M = 100
    N = 1000000
    dT = 0.3
    # генерируем файл инцидентов с заданными параметрами
    start = time.time()
    generator.create_incidents(M, N, 'csv/incidents.csv')
    end = time.time()
    print('Generation finished, elapsed:', end - start)

    # Обрабатываем файл с инцидентами и записываем результаты в указанный файл
    start = time.time()
    processor.process_incidents(input_filename='csv/incidents.csv', output_filename='csv/incidents_count.csv', dT=dT)
    end = time.time()
    print('Processing finished, elapsed:', end - start)
