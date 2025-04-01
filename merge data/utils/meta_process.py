import pyreadstat as pr


def remove_elements_by_indices(lst: list, indices: list) -> list:
    """
    根据indices删除lst对应index的元素
    :param lst: 原列表数据
    :param indices: 被删除数据的index
    :return: 删除数据后的lst
    """
    return [element for i, element in enumerate(lst) if i not in indices]


def remove_elements_by_columns(dit: dict, columns: list) -> dict:
    """
    根据列名删除dict的元素
    :param dit: 原字典,{column:value}
    :param columns: 要删除的列名
    :return:
    """
    for column in columns:
        if column in dit:
            del dit[column]
    return dit


def meta_process(meta: pr.metadata_container, columns: list, indices: list):
    """
    原dataframe的column结构改变后，meta数据也需要进行调整
    print(meta.column_labels)  # ['Country code 3-character', 'Country Identifier', 'Intl. School ID']
    print(meta.variable_value_labels) # {'CNT': {'FRA': 'France', 'USA': 'United States'},'CNTRYID': {8.0: 'Albania', 31.0: 'Baku (Azerbaijan)'}}
    print(meta.variable_display_width)  # {'CNT': 3, 'CNTRYID': 8, 'CNTSCHID': 8, 'CNTSTUID': 8, 'CYC': 4}
    print(meta.variable_measure) # {'CNT': 'nominal', 'CNTRYID': 'nominal', 'PV10MPRE': 'scale', 'SENWT': 'scale'}
    print(meta.original_variable_types)  # {'CNT': 'A3', 'CNTRYID': 'F3.0'}
    :param meta: dataframe的meta数据
    :param columns: 被删除的列名
    :param indices: 被删除的列名对应的index
    :return: 处理好的meta
    """
    meta_column_labels = remove_elements_by_indices(meta.column_labels, indices)
    meta_variable_value_labels = remove_elements_by_columns(meta.variable_value_labels, columns)
    meta_variable_display_width = remove_elements_by_columns(meta.variable_display_width, columns)
    meta_variable_measure = remove_elements_by_columns(meta.variable_measure, columns)
    meta_original_variable_types = remove_elements_by_columns(meta.original_variable_types, columns)
    return {
        'column_labels': meta_column_labels,
        'variable_value_labels': meta_variable_value_labels,
        'variable_display_width': meta_variable_display_width,
        'variable_measure': meta_variable_measure,
        'variable_format': meta_original_variable_types
    }


if __name__ == '__main__':
    dit = {'x1': 1, 'x2': 2, 'x3': 3, 'x4': 4, 'x5': 5}
    columns = ['x1', 'x3', 'x5']
    res = remove_elements_by_columns(dit, columns)
    print(res)

    lst = [1, 2, 3, 4, 5]
    indices = [0, 3]
    res = remove_elements_by_indices(lst, indices)
    print(res)
