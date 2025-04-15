import pytest
import sys

from ex03.financial import *

def test_get_response(monkeypatch):
  monkeypatch.setattr(sys, 'argv', ['financial.py', 'MSft'])
  assert get_response().status_code == 200


def test_no_second_arg(monkeypatch):
  monkeypatch.setattr(sys, 'argv', ['financial.py'])
  with pytest.raises(Exception):
    get_response()

def test_defenitly_wrong_arg(monkeypatch):
  monkeypatch.setattr(sys, 'argv', ['financial.py','%C0%AF'])
  with pytest.raises(Exception):
    get_response()

def test_parse_data_normal(monkeypatch):
  monkeypatch.setattr(sys, 'argv', ['financial.py', 'MSft', 'Cost of Revenue'])
  response = get_response()
  table = parse_data(response)
  assert len(table) == 6
  for value in table:
    assert value in response.text

def test_parse_data_wrong(monkeypatch):
  monkeypatch.setattr(sys, 'argv', ['financial.py', 'Maaa', 'Cost of Revenue'])
  response = get_response()
  with pytest.raises(Exception):
    parse_data(response)

def test_parse_data_empty(monkeypatch):
  monkeypatch.setattr(sys, 'argv', ['financial.py', 'MSft', ''])
  response = get_response()
  table = parse_data(response)
  assert len(table) != 6

def test_checks_no_env(monkeypatch):
  monkeypatch.setattr(sys, 'argv', ['financial.py', 'MSft', 'Cost of Revenue'])
  monkeypatch.delenv('VIRTUAL_ENV', raising=False)
  with pytest.raises(Exception):
    checks()

def test_checks_no_args(monkeypatch):
  monkeypatch.setattr(sys, 'argv', ['financial.py','',''])
  with pytest.raises(Exception):
    checks()

def test_checks_too_many_args(monkeypatch):
  monkeypatch.setattr(sys, 'argv', ['financial.py','MSft','Cost of Revenue',''])
  with pytest.raises(Exception):
    checks()

def test_main(monkeypatch):
  monkeypatch.setattr(sys, 'argv', ['financial.py'])
  with pytest.raises(Exception):
    main()

def test_main_normal(monkeypatch):
  monkeypatch.setattr(sys, 'argv', ['financial.py', 'MSft', 'Cost of Revenue'])
  assert main() == 0

def test_main_no_env(monkeypatch):
  monkeypatch.setattr(sys, 'argv', ['financial.py', 'MSft', 'Cost of Revenue'])
  monkeypatch.delenv('VIRTUAL_ENV', raising=False)
  with pytest.raises(Exception):
    main()