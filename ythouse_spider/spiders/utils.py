import re


"""
将中层/ 共26层替换成26
"""
def extract_total_floor(item):
    # 判断是否存在 /
    if ("/") in item:
        item_list = item.split(r"/")

        total_floor = item_list[1].replace(" ", "")

        total_floor = re.sub("\D", "", total_floor)

        return total_floor

    return re.sub("\D", "", item)



"""
从“中层/ 共26层”提取“中层”
"""
def extract_floor(item):
    # 判断是否存在 /
    if item.find("/") == -1:
        return None

    item_list = item.split(r"/")

    floor = item_list[0]

    return floor

"""
提取“建筑年代：2020”为2020
"""
def extract_year(item):
    if item == "":
        return None

    year = re.sub("\D", "", item)

    return year

"""
提取均价“14938元/㎡”为14938
"""
def extract_aver_price(item):
    price = re.sub("\D", "", item)
    return price

"""
提取总页码
传入href="/resoldhome/esf/list?page=9"提取9
"""
def extract_total_page(href):
    pattern = re.compile(r'\d+')
    result = int(pattern.findall(href)[0])
    return result

if __name__ == '__main__':
    href = "/resoldhome/esf/list?page=9"
    # total_floor = extract_total_floor(item)
    # floor = extract_floor(item)
    # year = extract_year(item)
    # price = extract_aver_price(item)
    result = extract_total_page(href)
    print(result)



