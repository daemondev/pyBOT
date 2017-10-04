import petl as etl
data = '''
[{"foo": "a", "bar": 1},
{"foo": "b", "bar": 2},
{"foo": "c", "bar": 2}]
'''
with open('example.json', 'w') as f:
    f.write(data)

table1 = etl.fromjson('example.json', header=['foo', 'bar'])
table1
