class Row:
    def __init__(self,
                name:str,
                valueType:str,
                pk:bool=False,
                fk:bool=False,
                connectedTable:str|None=None,
                connectedValue:str|None=None):

        self.name = name
        self.valueType = valueType
        self.pk = pk
        self.fk = fk
        self.connectedTable = connectedTable
        self.connectedValue = connectedValue


    def create(self) -> str:
        row = f"{self.name} {self.valueType}"
        if self.pk:
            row += f" PRIMARY KEY"
            return row

        if self.fk and self.connectedTable is not None:
            row += f",\nFOREIGN KEY ({self.name}) REFERENCES {self.connectedTable}({self.connectedValue})"
            return row
        return row

class Table:
    def __init__(self, name:str, *rows:Row):
        self.name = name
        self.rows = rows

    def create(self):
        table = ""
        rows = ""
        c=0
        for row in self.rows:
            rows += row.create()
            c += 1
            if c != len(self.rows):
                rows += ",\n"

        table = (f"""
                CREATE TABLE IF NOT EXISTS {self.name} (
                {rows}
                );
                """)
        return table

if __name__ == "__main__":
    t = Table("table",
              Row("id", "TEXT", pk = True),
              Row("name", "TEXT"),
              Row("value", "INTEGER", fk=True, connectedTable="table2", connectedValue="value"))

    print(t.create())
    print(Row("id", "TEXT", pk = True).create())
    print(Row("value", "INTEGER", fk=True, connectedTable="table2", connectedValue="value").create())










        