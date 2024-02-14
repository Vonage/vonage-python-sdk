from dataclasses import asdict, dataclass

from utils.utils import remove_none_values


@dataclass
class MyDataClass:
    name: str
    age: int
    address: str = None


def test_remove_none_values():
    data = MyDataClass(name='John', age=30)
    result = asdict(data, dict_factory=remove_none_values)
    assert result == {'name': 'John', 'age': 30}
