import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import main

@pytest.fixture
def make_csv(tmp_path):
    def _make_csv(name, content):
        file_path = tmp_path / name
        file_path.write_text(content.strip())
        return str(file_path)
    return _make_csv

def test_parse_data_standardize_headers(make_csv):
    content = """
    id,rate,name,department,hours_worked
    1,100.0,Alice,Dev,10
    """
    file1 = make_csv("file1.csv", content)
    data_dict = {col: [] for col in ['id', 'email', 'name', 'department', 'hours', 'salary']}
    parser = main.ParseData(data_dict, [file1])

    assert data_dict['name'] == ['Alice']
    assert data_dict['department'] == ['Dev']
    assert data_dict['hours'] == ['10']
    assert data_dict['salary'] == ['100.0']

def test_parse_data_multiple_files(make_csv):
    content1 = """
    id,hourly_rate,name,department,hours_worked
    2,50.0,Bob,Marketing,8
    """
    content2 = """
    id,rate,name,department,hours,hourly_rate
    3,60.0,Carol,Sales,12,ignored
    """
    f1 = make_csv("f1.csv", content1)
    f2 = make_csv("f2.csv", content2)
    data_dict = {col: [] for col in ['id', 'email', 'name', 'department', 'hours', 'salary']}
    parser = main.ParseData(data_dict, [f1, f2])

    assert data_dict['department'] == ['Marketing', 'Sales']
    assert data_dict['hours'] == ['8', '12']
    assert data_dict['salary'] == ['50.0', '60.0']

def test_payout_clean_data():
    data = {
        'id': ['1', '2'],
        'email': ['a@e.com', 'b@e.com'],
        'name': ['Alice', 'Bob'],
        'department': ['Dev', 'Dev'],
        'hours': ['10', '5'],
        'salary': ['100.0', '200.0'],
    }
    payout = main.Payout(data, ['name', 'hours', 'salary', 'payout'])
    # payout: 100.0*10=1000.0, 200.0*5=1000.0
    assert payout.data['payout'] == [1000.0, 1000.0]
    assert 'Dev' in payout.report
    assert len(payout.report['Dev']) == 2

def test_print_report_output(capsys):
    data = {
        'id': ['1', '2'],
        'email': ['a@e.com', 'b@e.com'],
        'name': ['Alice', 'Bob'],
        'department': ['HR', 'IT'],
        'hours': ['2', '3'],
        'salary': ['10', '20'],
    }
    payout = main.Payout(data, ['name', 'hours', 'salary', 'payout'])
    payout.print_report()
    captured = capsys.readouterr().out.strip().splitlines()

    header = captured[0]
    assert 'name' in header and 'hours' in header and 'salary' in header and 'payout' in header
    assert any('HR' in line for line in captured[1:])
    assert any('IT' in line for line in captured[1:])

def test_main_help(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['main.py'])
    with pytest.raises(SystemExit):
        main.main()

def test_payout_calculation():
    data = {
        'id': ['1', '2'],
        'name': ['Alice', 'Bob'],
        'department': ['Dev', 'Dev'],
        'hours': ['10', '5'],
        'salary': ['100.0', '200.0'],
    }
    payout = main.Payout(data, ['name', 'hours', 'salary', 'payout'])
    assert payout.data['payout'] == [1000.0, 1000.0]

def test_department_grouping():
    data = {
        'id': ['1', '2', '3'],
        'name': ['Alice', 'Bob', 'Charlie'],
        'department': ['HR', 'IT', 'HR'],
        'hours': ['10', '5', '8'],
        'salary': ['100.0', '200.0', '150.0'],
    }
    payout = main.Payout(data, ['name', 'hours', 'salary', 'payout'])
    assert 'HR' in payout.report
    assert 'IT' in payout.report
    assert len(payout.report['HR']) == 2
    assert len(payout.report['IT']) == 1


def test_print_report(capsys):
    data = {
        'id': ['1'],  # Dummy ID
        'name': ['Alice'],
        'department': ['HR'],
        'hours': ['10'],
        'salary': ['100.0'],
    }
    payout = main.Payout(data, ['name', 'hours', 'salary', 'payout'])
    payout.print_report()
    captured = capsys.readouterr()
    assert 'HR' in captured.out
    assert 'Alice' in captured.out
    assert '1000.0' in captured.out