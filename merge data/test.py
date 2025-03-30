import pandas as pd

# a = pd.DataFrame(data=[1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3], columns=['x'], dtype='float64')
# a1 = a[a['x'] == 1]
# a2 = a[a['x'] == 2]
# a3 = a[a['x'] == 3]
# print(a1)
# print(a2)
# print(a3.iloc[0])

# def find_common_elements_and_indices(a, b):
#     # 找出共同元素
#     common_elements = set(a).intersection(set(b))
#     # 存储共同元素及其在b中的索引
#     result = {}
#     for element in common_elements:
#         # 获取元素在b中的所有索引位置
#         indices = [i for i, x in enumerate(b) if x == element]
#         result[str(element)] = indices[0]
#     return result
#
# # 示例列表
# a = [1, 2, 3, 4, 5]
# b = [3, 4, 5, 6, 7]
#
# # 调用函数
# common_info = find_common_elements_and_indices(a, b)
# print("共同元素及其在b中的索引位置：", common_info)
#
#
# def remove_elements_by_indices(lst, indices):
#     return [element for i, element in enumerate(lst) if i not in indices]
#
# result = remove_elements_by_indices(common_info, [0,2])
# print("删除指定索引元素后的列表:", result)


a = {'x1':1,'x2':2,}
b = {'y1':1,'y2':2,}
a = {**a,**b}
print(a)