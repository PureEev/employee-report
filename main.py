import argparse

class ParseData:
    def __init__(self, data_dict, files: list[str]):
        self.data_dict = data_dict
        for file in files:
            self.parse_data(file)

    def _to_standard(self, possible_values: list[str], standard_value: str, data: list[str]) -> list[str]:
        for i, item in enumerate(data):
            if item in possible_values:
                data[i] = standard_value
        return data

    def parse_data(self, filename: str) -> None:
        with open(filename, 'r') as file:
            parse_data = []
            try:
                while True:

                    line = file.readline()

                    if not line:
                        break

                    line = line.strip()  # Удаляем ведущие и конечные пробелы/переносы строк
                    if not line:  # Пропускаем пустые строки
                        continue

                    parse_line = list(line.split(','))
                    parse_data.append(parse_line)

            except Exception as e:
                print(e)

        if parse_data:
            columns = parse_data[0]

            columns = self._to_standard( ['hourly_rate', 'rate'], 'salary' , columns)
            columns = self._to_standard(['hours_worked'], 'hours', columns)

            seen_columns = set()
            for index, column in enumerate(columns):
                if column not in seen_columns:
                    seen_columns.add(column)
                    self.data_dict[column].extend(row[index] for row in parse_data[1:] if len(row) > index)



class Payout:
    def __init__(self, data: dict, headers: list):
        self.data = data
        self.headers = headers
        self.report = []
        self.clean_data()

    def clean_data(self) -> None:
        payout = [float(numbs[0]) * float(numbs[1]) for numbs in zip(self.data['salary'], self.data['hours'])]
        self.data['payout'] = payout

        self.report = {departament: [] for departament in self.data['department']}

        for i in range(len(self.data['id'])):
            self.report[self.data['department'][i]].append(
                [self.data['name'][i], self.data['hours'][i], self.data['salary'][i], self.data['payout'][i]])

    def _compute_widths(self, rows: list[list[str]]) -> list[int]:
        # ширина = max(длина заголовка, длины всех значений в колонке) + отступ
        widths = [len(h) for h in self.headers]
        widths.insert(0, max(list(map(len, self.report.keys()))))
        for row in rows:
            for i, val in enumerate(row):
                widths[i] = max(widths[i], len(str(val)))
        return [w + 2 for w in widths]  # +2 пробела по бокам

    def print_report(self) -> None:
        rows = [[""] + self.headers]
        for department, persons in self.report.items():
            for person in persons:
                rows.append([department] + person)

        widths = self._compute_widths(rows)
        *non_last_widths, last_width = widths

        non_last_fmt = "  ".join(f"{{:{w}}}" for w in non_last_widths)
        last_fmt = " " + f"{{:>{last_width}}}"

        def fmt_line(cells: list[str]) -> str:
            head = non_last_fmt.format(*cells[:-1])
            tail = last_fmt.format(cells[-1])
            return head + tail

        header_cells = [""] + self.headers
        print(fmt_line(header_cells))

        for department, persons in self.report.items():
            for i, person in enumerate(persons):
                first = department if i == 0 else "-" * widths[0]
                row_cells = [first] + person
                print(fmt_line(row_cells))


def main():

    REPORTS = {
        'payout': [Payout, ['name', 'hours', 'salary', 'payout']],
    }
    parser = argparse.ArgumentParser(description="Reports generator")
    parser.add_argument('files', nargs='+', help="CSV files")
    parser.add_argument('--report', nargs='+',required=True, choices=REPORTS.keys(), help="Type of report")
    args = parser.parse_args()
    columns = ['id',
               'email',
               'name',
               'department',
               'hours',
               'salary']
    data_dict = {column: [] for column in columns}

    data_parse = ParseData(data_dict, args.files)

    for report in args.report:
        report = REPORTS[report][0](data_parse.data_dict, REPORTS[report][1])
        report.print_report()



if __name__ == "__main__":
    main()

