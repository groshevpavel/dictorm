from dictorm import dictorm
from example_dicts import example1


do = dictorm(example1)
for k, v in do.items(key='mainLevel'):
    print('key:', k, 'value:', v)
# key: mainLevel value {'val1': 'value1', 'parent': {'val2': 'value2', 'parent': {'val3': 'value3', 'parent': {'val4': 'value4', 'deepNestedValue': 'soDeep'}}}}

do = dictorm(example1)
for k, v in do.items(value=1):
    print('key:', k, 'value:', v)
# key: a value: 1

do = dictorm(example1)
for k in do.keys(key='a'):
    print('key:', k)
# key: a

do = dictorm(example1)
for k in do.values(value=1):
    print('value:', v)
# value: 1
