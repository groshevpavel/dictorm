from dictorm import dictorm
from example_dicts import example1

dictorm_from_args = dictorm('Key1', 'Key2', 3, 4)  # {'Key1': None, 'Key2': None, 3: None, 4: None}

dictorm_from_args = dictorm({'a': 1, 'b': 2})  # one dict at args
dictorm_from_args = dictorm({'a': 1}, {'b': 2})  # two(or more) dicts at args
dictorm_from_args = dictorm(('a', 1,), ('b', 2,))  # tuples with (key, value,)
dictorm_from_args = dictorm(('a', 1,), {'b': 2}, ('c', 3,), {'d': 4})  # combine of course

dictorm_from_kwargs = dictorm(keyOne='valueOne', keyTwo='valueTwo')  # {'keyOne': 'valueOne', 'keyTwo': 'valueTwo'}
dictorm_combine = dictorm({'a': 1}, ('b', 2,), keyName='valueName')

value = dictorm(example1).mainLevel.parent.parent.parent.deepNestedValue
print(value)  # 'soDeep'
print(repr(value))  # nest level: 5; type: <class 'str'>

print(dictorm(example1).path('mainLevel.parent.parent.parent'))  # {'val4': 'value4', 'deepNestedValue': 'soDeep'}
print(dictorm(example1).path('mainLevel.parent.parent.parent.val4'))  # value4
print(dictorm(example1).mainLevel.path('parent.parent').parent.path('deepNestedValue'))  # 'soDeep'

print(dictorm(example1) + dict(newKey='newValue'))  # example1 updated with 'newKey': 'newValue'
do = dictorm(example1) + dict(newKey='newValue')  # example1 updated with 'newKey': 'newValue'
do1 = do.mainLevel.path('parent.parent')
print('current_path:', do1.current_path)  # mainLevel.parent.parent
do1.current_path = None  # drop current path to root level
print('current path:', do1.current_path)

# @ROOT.mainLevel
# @ROOT.mainLevel.parent
# @ROOT.mainLevel.parent.parent
# @ROOT.mainLevel.parent.parent.parent
# @ROOT.mainLevel.parent.parent.parent.deepNestedValue
for element in dictorm(example1).ipath('mainLevel.parent.parent.parent.deepNestedValue'):
    print(element.current_path)

# @ROOT.mainLevel.parent
# @ROOT.mainLevel.parent.parent
# @ROOT.mainLevel.parent.parent.parent
for element in dictorm(example1).mainLevel.yuke('parent'):
    print(element.current_path)
