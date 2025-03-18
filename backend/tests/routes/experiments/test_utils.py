import pytest

from backend.routes.experiments.utils import flat_to_tree, dict_to_list


@pytest.mark.parametrize("flat_input, desired_keys, expected_output", [
    (
            [{"path": "a/b/c", "value": 1}, {"path": "a/b/d", "value": 2}],
            ["value"],
            [{"path": "a", "children": [{"path": "b", "children": [
                {"path": "c", "value": '1'},
                {"path": "d", "value": '2'}
            ]}]}]
    )
])
def test_flat_to_tree(flat_input, desired_keys, expected_output):
    """Тест преобразования списка в дерево"""
    assert flat_to_tree(flat_input, desired_keys) == expected_output


@pytest.mark.parametrize("dict_input, expected_output", [
    (
            {"a": {"path": "a", "children": {"b": {"path": "b", "value": 1}}}},
            [{"path": "a", "children": [{"path": "b", "value": '1'}]}]
    )
])
def test_dict_to_list(dict_input, expected_output):
    """Тест преобразования словаря в список"""
    assert dict_to_list(dict_input) == expected_output
