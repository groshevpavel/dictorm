"""Dict ORM
plans:
    value = dictorm(d).get('mainLevel.parent.parent.parent.deepNestedValue')  # 'soDeep'
    value = dictorm(d).mainLevel.parent.parent.parent.deepNestedValue  # 'soDeep'
    value_iterator = dictorm(d).mainLevel.iter_until_exists('parent')  # yield all values of 'parent' until it exists
    count nesting and print in __repr__ calls
    print(repr(dictorm(d).mainLevel.parent.parent))  # nest level: 3, type: dict
    :TODO for finded_key, finded_value in dictorm(d).items(key='keyNameToFind', value='valueNameToFind')
    :TODO for finded_key in dictorm(d).keys(key='keyNameToFind')
    :TODO for finded_value in dictorm(d).values(value='valueNameToFind')
"""
import functools
from pprint import pformat

ROOT_PATH_NAME = '@ROOT'


class dictorm:

    def __init__(self, *args, **kwargs):
        self._dictionary = {}
        self._nest_path = []
        self._current_element = None
        self._types = (dict, type(self),)

        self.operate_args(args)
        self.operate_kwargs(kwargs)

    def operate_args(self, args):
        """If agrs contains 1 dict it will apply as main,
        otherwise all dicts will merged(updated) into one resulted"""
        dicts = [arg for arg in args if isinstance(arg, self._types)]
        dicts.extend([{arg: None} for arg in args if isinstance(arg, (str, int,))])  # str, int as keys with None value
        tuples = [arg for arg in args if isinstance(arg, tuple) and len(arg) == 2]  # list of (key, value,) tuples

        if dicts:
            if len(dicts) == 1:
                self._dictionary = dicts[0]
            else:
                initial = self._dictionary if self._dictionary is not None else dict()
                for d in dicts:
                    initial.update(d)
                self._dictionary = initial

        if tuples:
            self._dictionary.update(dict(tuples))

    def operate_kwargs(self, kwargs):
        if kwargs:
            self._dictionary.update(kwargs)

    def __getattr__(self, item):
        if not isinstance(self._dictionary, (dict, dictorm,)):
            raise KeyError(f'You try to get "{item}" key from non-dict object, which type is {type(self._dictionary)}')

        value = self._current_element[item] if self._current_element is not None else self._dictionary[item]
        self._nest_path.append(item)
        self._current_element = value
        return self

    def __str__(self):
        return pformat(self.current_element)

    def __repr__(self):
        return f'nest level: {len(self._nest_path)}; type: {type(self._current_element)}'

    def __add__(self, other):
        types = (dict, type(self),)
        if isinstance(other, types) and isinstance(self.current_element, types):
            self.current_element.update(other)
            return self

    @property
    def current_element(self):
        return self._current_element if self._current_element is not None else self._dictionary

    @current_element.setter
    def current_element(self, value):
        self._current_element = value

    @property
    def current_path(self):
        if self._nest_path:
            return f'{ROOT_PATH_NAME}.' + '.'.join(self._nest_path)
        return ROOT_PATH_NAME

    @current_path.setter
    def current_path(self, new_path):
        if new_path is None:
            self.current_element = None
            self._nest_path = []

    def path(self, path: str, delimiter: str = '.'):
        path_split = path.split(delimiter)
        result = functools.reduce(lambda a, b: a[b], path_split, self.current_element)
        self._nest_path.extend(path_split)
        self.current_element = result
        return self

    def ipath(self, fullpath: str, delimiter: str = '.'):
        path_split = fullpath.split(delimiter)
        for path_step in path_split:
            yield self.path(path_step)

    def yuke(self, keyname: str):
        """yield until key exsists"""
        while True:
            try:
                yield getattr(self, keyname)
            except KeyError:
                break

    def items(self, key: object = None, value: object = None):
        if not isinstance(self.current_element, self._types):
            raise TypeError(f'Can not iterate items on current element of type {type(self.current_element)}')

        for k, v in self.current_element.items():
            if not key and not value:
                yield k, v
            if key and k == key and not value:
                yield k, v
            if value and v == value and not key:
                yield k, v
            if value and key and k == key and v == value:
                yield k, v

    def keys(self, key: object = None):
        for k, v in self.items(key=key):
            yield k

    def values(self, value: object = None):
        for k, v in self.items(value=value):
            yield v


if __name__ == '__main__':
    pass
