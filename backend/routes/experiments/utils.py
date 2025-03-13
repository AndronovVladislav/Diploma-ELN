from collections import defaultdict
from typing import Any

infinite_defaultdict = lambda: defaultdict(infinite_defaultdict)


def find_or_create_node(children: list[dict[str, Any]], path_part: str) -> dict[str, Any]:
    for child in children:
        if child['path'] == path_part:
            return child
    new_node = {'path': path_part, 'children': []}
    children.append(new_node)
    return new_node


def dict_to_list(d) -> list[dict]:
    result = []
    for k, v in d.items():
        node = {'path': k, **{key: str(value) for key, value in v.items() if key != 'children'}}
        if 'children' in v:
            children = dict_to_list(v['children'])
            if children:
                node['children'] = children
        result.append(node)
    return result


def flat_to_tree(flat: list[dict], desired_keys: list[str]) -> list[dict]:
    root = {}

    for item in flat:
        parts = item['path'].split('/')
        current_level = root

        for i, part in enumerate(parts):
            if part not in current_level:
                current_level[part] = {'path': part, 'children': {}}

            if i == len(parts) - 1:
                current_level[part].update({k: v for k, v in item.items() if k in desired_keys})
                current_level[part].pop("children", None)
            else:
                current_level = current_level[part]['children']

    if '' in root:
        root = root['']['children']

    return dict_to_list(root)
