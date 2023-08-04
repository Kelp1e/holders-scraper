from holders.holders import Holder, Holders

holder = Holder("abc", 500, 1.20)
print(holder)

holders_list_1 = Holders([
    Holder("abc", 200, 2.00),
    Holder("abc", 50, 0.50)
])
print(holders_list_1)

holders_list_2 = Holders([
    Holder("bvd", 200, 2.00),
    Holder("abc", 50, 0.50),
    Holder("zxc", 50, 0.50)
])
print(holders_list_2)

holders_list_1.extend(holders_list_2)
print(holders_list_1)