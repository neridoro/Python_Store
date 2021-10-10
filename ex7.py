"""
Name : Neria Doron
ID:315351445
Group:01
Assignment:07

OPTIONS EXAMPLES :
1.Query by category:Dance,^
2.Query by items:Tennis Racket
3.Purchase an item:Tennis Racket
4.Admin panel:123456
"""
from _collections import defaultdict
import sys


"""
* Function Name:read_data()
* Input:None
* Output:dictionary with info
* Function Operation:read file and put data in dictionary return dictionary
"""
def read_data():
    file = open('store.txt')
    store_items = file.readlines()
    dic = {}
    for line in store_items:
        if line != "\n":
            category, data = line.split(":")
            items = data.split(";")
            dic[category.lstrip()] = {}
            for item in items[0:len(items) - 1]:
                name, price = item.split(",")
                dic[category.lstrip()][name.lstrip()] = price.lstrip()
    file.close()
    return dic


"""
* Function Name:print_menu()
* Input:None
* Output:None
* Function Operation:print menu
"""
def print_menu():
    print("Please select an operation:\n"
          "\t0. Exit.\n"
          "\t1. Query by category.\n"
          "\t2. Query by item.\n"
          "\t3. Purchase an item.\n"
          "\t4. Admin panel.")


"""
* Function Name:print_admin_menu()
* Input:None
* Output:None
* Function Operation:print admin menu
"""
def print_admin_menu():
    print("Admin panel:\n"
        "\t0. Return to main menu.\n"
        "\t1. Insert or update an item.\n"
        "\t2. Save.")

"""
* Function Name:in_both_category(data):
* Input:list of dictionaries
* Output:list of sorted data
* Function Operation:find all items that are in more the 1 category
* make them a list and sort and return them
"""
def in_both_category(data):
    needed_list = []
    for item in data:
        for name in item.keys():
            needed_list.append(name)
    new_list = []
    copy_needed_list = needed_list.copy()
    for item in copy_needed_list:
        needed_list.remove(item)
        if item in needed_list:
            new_list.append(item)
    return sorted(list(set(new_list)))


"""
* Function Name:in_either_category(data)
* Input:list of dictionaries
* Output:list of sorted data
* Function Operation:print all items in given categories
"""
def in_either_category(data):
    needed_list = []
    for item in data:
        for name in item.keys():
            needed_list.append(name)
    return sorted(list(set(needed_list)))


"""
* Function Name:in_one_category(data)
* Input:list of dictionaries
* Output:list of sorted data
* Function Operation:find all data that is in exactly one category
* out of given categories
"""
def in_one_category(data):
    needed_list = []
    for item in data:
        for name in item.keys():
            needed_list.append(name)
    both_list=in_both_category(data)
    for item in both_list:
        while item in needed_list:
            needed_list.remove(item)
    return sorted(list(set(needed_list)))


"""
* Function Name:by_category(dic, cache)
* Input:list of dictionaries , dictionary of cache
* Output:None
* Function Operation:print items in store by from given categories
* can have 3 operation ^,&,|
"""
def by_category(dic, cache):
    user_input=input().lstrip()
    for items in cache.keys():
        if user_input in items:
            return print("Cached: {0}".format(cache[user_input]))
    data=user_input.split(",")
    needed_list=[]
    if len(data)<2:
        return print("Error: not enough data.")
    for place in range(0,len(data)-1):
        if place > 1:
            return print("Error: unsupported query operation.")
        elif data[place].lstrip() not in dic.keys():
            return print("Error: one of the categories does not exist.")
        else:
            needed_list.append(dic[data[place].lstrip()])
    if data[len(data)-1].lstrip() == "&":
        needed_list=(in_both_category(needed_list))
        cache[user_input] = needed_list
    elif data[len(data)-1].lstrip() == "|":
        needed_list=(in_either_category(needed_list))
        cache[user_input] = needed_list
    elif data[len(data)-1].lstrip() == "^":
        needed_list=(in_one_category(needed_list))
        cache[user_input]=needed_list
    else:
        return print("Error: unsupported query operation.")
    print(needed_list)

"""
* Function Name:def by_product(data, cache):
* Input:list of dictionaries , dictionary of cache
* Output:None
* Function Operation:print items in store with same category as
* given item
"""
def by_product(data, cache):
    user_input = input().lstrip()
    for items in cache.keys():
        if user_input in items:
            return print("Cached: {0}".format(cache[user_input]))
    needed_list=[]
    for items in data.values():
        if user_input in items:
            for item in items:
                needed_list.append(item)
    if len(needed_list)<1:
        return print("Error: no such item exists.")
    needed_list=(list(set(needed_list)))
    needed_list.remove(user_input)
    cache[user_input]=sorted(needed_list)
    return print(sorted(needed_list))


"""
* Function Name:sell_item(data,cache):
* Input:list of dictionaries , dictionary of cache
* Output:None
* Function Operation:sell item in shop and clean cache
"""
def sell_item(data,cache):
    user_input = input().lstrip()
    needed_item=0
    price=0
    for items in data.values():
        if user_input in items:
            for item in items.keys():
                if item == user_input:
                    needed_item = item
                    price = items[item]
    if (needed_item == 0):
        return print("Error: no such item exists.")
    print('You bought a brand new "{0}" for {1}$.'.format(needed_item, price))
    for items in data.values():
        if needed_item in items:
            del items[needed_item]
    return cache.clear()


"""
* Function Name:update_item(data,cache):
* Input:list of dictionaries , dictionary of cache
* Output:None
* Function Operation:update item in shop and clean cache
"""
def update_item(data,cache):
    user_input = input()
    try:
        add_categories,add_item=user_input.split(":")
        add_item,add_price=add_item.split(",")
        add_categories=add_categories.split(",")
    except:
        return print("Error: not enough data.")
    for category in add_categories:
        if category.lstrip() not in data.keys():
            return print("Error: one of the categories does not exist.")
    try:
        add_price=int(add_price.lstrip())
        if add_price > 0:
            cache.clear()
            for items in data.values():
                if add_item in items:
                    items[add_item.lstrip()] = add_price
            for category in add_categories:
                data[category.lstrip()][add_item.lstrip()] = add_price
            print('Item "{0}" added.'.format(add_item.lstrip()))
    except ValueError:
        return print("Error: price is not a positive integer.")

"""
* Function Name:def save_outpot(data)
* Input:list of dictionaries
* Output:None
* Function Operation:save store data in out.txt file
"""
def save_outpot(data):
    data=dict(sorted(data.items()))
    file= open(sys.argv[3],"w")
    for category in data.keys():
        file.write("{0}:".format(category))
        data[category]=dict(sorted(data[category].items()))
        for item in data[category]:
            file.write(" {0}, {1};".format(item,data[category][item]))
        file.write("\n")
    file.close()
    print('Store saved to "out.txt".')

"""
* Function Name:admin_options(data,cache)
* Input:list of dictionaries, dictionary of cache
* Output:None
* Function Operation:admin input options
"""
def admin_options(data,cache):
    print_admin_menu()
    user_input = input().lstrip()
    if user_input == '0':
        return input_option(data, cache)
    elif user_input == '1':
        update_item(data,cache)
    elif user_input == '2':
        save_outpot(data)
    else:
        print("Error: unrecognized operation.")
    admin_options(data, cache)

"""
* Function Name:admin_panel(data,cache):
* Input:list of dictionaries, dictionary of cache
* Output:None
* Function Operation:validate password and send to admin options
"""
def admin_panel(data,cache):
    print("Password: ",end="")
    user_input = input().lstrip()
    with open('admin.txt') as file:
        if file.readlines()[0]==user_input:
            file.close()
            return admin_options(data,cache)
        else:
            file.close()
            return print("Error: incorrect password, returning to main menu.")
"""
* Function Name:input_option(data, cache)
* Input:list of dictionaries, dictionary of cache
* Output:None
* Function Operation:get user input and send to proper function
"""
def input_option(data, cache):
    print_menu()
    option = input()
    if option == '0':
        exit(1)
    elif option == '1':
        by_category(data, cache)
        return input_option(data, cache)
    elif option == '2':
        by_product(data, cache)
        return input_option(data, cache)
    elif option == '3':
        sell_item(data,cache)
        return input_option(data,cache)
    elif option=='4':
        admin_panel(data,cache)
        return input_option(data,cache)
    else:
        print("Error: unrecognized operation.")
        return input_option(data, cache)


def main():
    data = read_data()
    cache={}
    input_option(data,cache)


main()
