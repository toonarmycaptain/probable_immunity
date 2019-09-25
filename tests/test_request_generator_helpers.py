import pytest

from tests.request_generator_helpers import flatten_dict


@pytest.mark.parametrize(
    'test_dict, flattened_dict',
    [({'a': 1}, [('a', 1)]),
     ({'a': 1, 'b': 2}, [('a', 1), ('b', 2)]),
     ({'a': 1,
       'b': {'c': 3}
       },
      [('a', 1), ('b-c', 3)]),
     ({'a': 1,
       'b': {'c': 3,
             'd': 4,
             'e': {'f': 6}
             }
       },
      [('a', 1), ('b-c', 3), ('b-d', 4), ('b-e-f', 6)]
      ),
     ({'a': 1,
       'b': {'c': 2,
             'd': 4,
             'e': {'f': 6,
                   'g': {'h': 8,
                         'i': {'j': 10
                               },
                         }
                   },
             },
       },
      [('a', 1), ('b-c', 2), ('b-d', 4), ('b-e-f', 6), ('b-e-g-h', 8), ('b-e-g-i-j', 10)]),
     ])
def test_flatten_dict(test_dict, flattened_dict):
    result = flatten_dict(test_dict)
    print(result)
    assert result == flattened_dict


print(flatten_dict({'a': 1,
                    'b': {'c': 2,
                          'd': 3,
                          'e': {'f': 6}
                          }
                    }))
