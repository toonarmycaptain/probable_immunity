def flatten_subdict(key, subdict: dict) -> list:
    new_items: list = []
    for subdict_key in subdict:
        if isinstance(subdict[subdict_key], dict):
            new_items += flatten_subdict(f'{key}-{subdict_key}', subdict[subdict_key])
        else:
            new_items.append((f'{key}-{subdict_key}', subdict[subdict_key]))

    return new_items


def flatten_dict(orig_dict: dict) -> list:
    flat_dict_list: list = []
    for key in orig_dict:
        if isinstance(orig_dict[key], dict):
            flat_dict_list += flatten_subdict(key, orig_dict[key])
        else:
            flat_dict_list.append((key, orig_dict[key]))
    return flat_dict_list
