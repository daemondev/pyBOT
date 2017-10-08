
import petl as etl
tbl = etl.fromxlsx("demo.xlsx", read_only=True)
print(tbl)
