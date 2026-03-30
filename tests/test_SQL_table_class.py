import pytest
from app.SQL_table_class import Table, Row
import _helpers as h


def test_creating_row_primary_key():
    r = Row("id", "TEXT", pk = True).create()
    expected = "id TEXT PRIMARY KEY"
    r = h.normalize_whitespace(r)
    expected = h.normalize_whitespace(expected)

    assert r == expected, "Expected row does not match the result"

def test_creating_row_foreign_key():
    r = Row("value", "INTEGER", fk=True, connectedTable="table2", connectedValue="value").create()
    expected = "value INTEGER,FOREIGN KEY (value) REFERENCES table2(value)"
    r = h.normalize_whitespace(r)
    expected = h.normalize_whitespace(expected)

    assert r == expected, "Expected row does not match the result"

def test_creating_table():
    t = Table("table",
              Row("id", "TEXT", pk = True),
              Row("name", "TEXT"),
              Row("value", "INTEGER", fk=True, connectedTable="table2", connectedValue="value"))

    result = t.create()

    expected = """
    CREATE TABLE IF NOT EXISTS table (
        id TEXT PRIMARY KEY,
        name TEXT,
        value INTEGER,
        FOREIGN KEY (value) REFERENCES table2(value)
    );
    """
    result = h.normalize_whitespace(result)
    expected = h.normalize_whitespace(expected)
    assert expected == result, "Created table does not match expected."


