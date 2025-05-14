# Employee Report Generator

Скрипт для генерации отчетов по заработной плате сотрудников на основе CSV-файлов.

## Особенности

- Чтение данных из нескольких CSV-файлов
- Поддержка отчета `payout` с суммарными выплатами по отделам
- Обработка различных названий колонок для часовой ставки (`hourly_rate`, `rate`, `salary`)
- Расширяемая архитектура для добавления новых типов отчетов

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/PureEev/employee-report.git
cd employee-report
```
## Тестирование
```
pip install pytest
pytest
```
## Пример работы

### Пример запуска скрипта

data1.csv:
```
id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40
3,carol@example.com,Carol Williams,Design,170,60
```

data2.csv:
```
department,id,email,name,hours_worked,rate
HR,101,grace@example.com,Grace Lee,160,45
Marketing,102,henry@example.com,Henry Martin,150,35
HR,103,ivy@example.com,Ivy Clark,158,38

```

data3.csv:
```
email,name,department,hours_worked,salary,id
karen@example.com,Karen White,Sales,165,50,201
liam@example.com,Liam Harris,HR,155,42,202
mia@example.com,Mia Young,Sales,160,37,203
```


```
python main.py data1.csv data2.csv data3.csv --report payout
```

![photo_2025-05-14_14-05-30](https://github.com/user-attachments/assets/d170266c-e943-4ea1-9e4d-cbdab14658c0)


```
python main.py data1.csv --report payout  
```

![photo_2025-05-14_14-05-32](https://github.com/user-attachments/assets/b6913361-b3c9-48c3-aed2-33fd41e8c580)




