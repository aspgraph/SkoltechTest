import pandas as pd


def process_incidents(*, input_filename, output_filename, dT):
    """
    Обработка файла с "инцидентами"
    Все параметры должны быть проименованы
    Описание алгоритма:
    1) Таблица "инцидентов" загружается в память
    Сложность: O(N)
    2) Таблица сортируется по столбцу с временем
    Сложность: O(N*logN)
    3) Таблица группируется по полям feature1, feature2
    Сложность: O(N)
    3) Внутри каждой группы, в порядке возрастания по времени, каждому "инциденту"
    сопоставляется количество "инцидентов" до него из той же группы
    Отдельно обрабатывается случай, если у двух "инцидентов" из одной группы совпадает время
    Сложность: O(N)
    4) Сортируем итоговый результат и записываем в файл
    Сложность: O(N*logN)
    :arg input_filename: Входной файл с "инцидентами"
    :arg output_filename: Файл для сохранения результатов
    :arg dT: Существенная для алгоритма разница во времени между "инцидентами"
    :type input_filename: str
    :type output_filename: str
    :type dT: int
    """
    if dT < 0.0 or dT > 1.0:
        print('Wrong arguments! dT must be in range [0.0; 1.0]!')
        return

    # Считываем файл в таблицу DataFrame
    try:
        df = pd.read_csv(input_filename, header=0)
    except IOError:
        print('Could not read file:', input_filename)
        return

    res = []
    skip_count = 0
    # Сортируем таблицу с данными по столбцу времени
    df.sort_values(by='time', inplace=True)
    # Группируем записи по столбцам feature1 и feature2
    grp = df.groupby(by=['feature1', 'feature2'], sort=False)
    for grp_index, grp_rows in grp:
        # Итерируемся по получившимся группам
        # cur_i - порядковый номер текущего "инцидента"
        cur_i = 0
        # last_i - порядковый номер первого "инцидента", произошедшего в прошлом не позднее чем dT перед текущим
        last_i = 0
        prev_time = -1.0
        # Внутри каждой группы, итерируемся по "инцидентам" из этой группы
        for cur_index in grp_rows.index:
            cur_time = grp_rows.at[cur_index, 'time']
            # Если разница во времени между текущим и предыдущим "инцидентами"
            # равна нулю, то пропускаем предыдущий и перед ним, произошедшие в то же время
            if cur_time == prev_time:
                skip_count += 1
            else:
                skip_count = 0

            # last_i увеличивается до тех пор, пока last_time не войдёт во временной диапазон [cur_time - dT; cur_time]
            last_time = grp_rows.at[grp_rows.index[last_i], 'time']
            while cur_time - dT > last_time:
                last_i += 1
                last_time = grp_rows.at[grp_rows.index[last_i], 'time']
            # Число "инцидентов" перед текущим - разница в порядковых номерах cur_i и last_i,
            # за исключением одновременных "инцидентов"
            res.append((cur_index, cur_i - last_i - skip_count))
            prev_time = cur_time
            cur_i += 1
    # Расчёты сортируются по id и записывается в итоговую таблицу
    res.sort()
    ndf = pd.DataFrame.from_records(res, columns=['id', 'count'])

    try:
        ndf.to_csv(output_filename, index=False)
    except IOError:
        print('Could not write file:', output_filename)
        return
