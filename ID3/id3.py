import math

def entropy(classes, objects):
    if len(objects) == 0:
        return 0.0
    mp = divide_objects(objects, 1, classes)

    p = []
    for i in range(len(classes)):
        p.append(len(mp[i]) / len(objects))
    
    e = 0
    for i in range(len(classes)):
        if p[i] == 0.0:
            continue
        e -= p[i] * math.log(p[i], 2)

    return e

def information_gain(count_values, e_all, count_subset_obj, entropy_subset, objects):
    ig = e_all
    for i in range(count_values):
        ig -= count_subset_obj[i] / len(objects) * entropy_subset[i]
    return ig

def attribute2index(attrib):
    if attrib == "velikost":
        return 2
    elif attrib == "srst":
        return 3
    elif attrib == "barva":
        return 4
    elif attrib == "spolecensky":
        return 5

def all_ig(attributes, classes, objects):
    e_all = entropy(classes, objects)
    ig = []
    for attribute in attributes:
        values = attributes.get(attribute)
        mp = divide_objects(objects, attribute2index(attribute), values)

        entropy_subset = []
        count_subset_obj = []
        for subset in mp:
            count_subset_obj.append(len(subset))
            e = entropy(classes, subset)
            entropy_subset.append(e)

        ig_attrib = round(information_gain(len(values), e_all, count_subset_obj, entropy_subset, objects), 4)
        ig.append(ig_attrib)
    return ig

def divide_objects(objects, index, values):
    mp = []
    for value in values:
        mp.append([])
        
    for obj in objects:
        for i, category in enumerate(values):
            if category == obj[index]:
                mp[i].append(obj)
    return mp

def print_node(attributes_list, ig, best_attrib, index):
    print(best_attrib + str(index) +" ", end="")
    print('[label="' + best_attrib + '|{', end="")
    for i, attrib_ig in enumerate(ig):
        if i == len(ig) - 1:
            print(attributes_list[i] + "=" + str(format(attrib_ig, ".4f")).format() + '}"]')
        else:
            print(attributes_list[i] + "=" + str(format(attrib_ig, ".4f")) + "|", end="")

def print_edge(objects, attribute, best_attrib, index, output):
    print(output, end="")
    print(best_attrib + str(index) +" ", end="")
    print('[label="' + attribute + " {", end="")
    for i, object in enumerate(objects):
        if i == len(objects) - 1:
            print(str(object[0]) + '}"]')
        else:
            print(str(object[0]) + ',', end="")

def all_from_same_category(objects):
    cls = objects[0][1]
    for obj in objects:
        if obj[1] != cls:
            return False
    return True

def id3(attributes, classes, objects, attribute, output):
    global uid
    counter = uid
    uid += 1
    if len(objects) == 0:
        uid -= 1
        return
    if all_from_same_category(objects):
        print_edge(objects, attribute, objects[0][1], counter, output)
        print(objects[0][1] + str(counter) + '  [label="' + objects[0][1] + '"]')
        return

    attributes_list = list(attributes)
    ig = all_ig(attributes, classes, objects)
    max_index = ig.index(max(ig))
    best_attrib = attributes_list[max_index]
    values = attributes.get(best_attrib)
    if counter > 1:
        print_edge(objects, attribute, best_attrib, counter, output)
    
    del attributes[best_attrib]

    print_node(attributes_list, ig, best_attrib, counter)
    mp = divide_objects(objects, attribute2index(best_attrib), values)
    for i in range(len(values)):
        output = best_attrib + str(counter) +" -> "
        id3(attributes, classes, mp[i], values[i], output)
    attributes[best_attrib] = values
    return
    
    
if __name__ == "__main__":
    global uid
    uid = 1
    attributes = {
        "velikost": ["maly", "stredni", "velky"],
        "srst": ["kratka", "dlouha", "bez"],
        "barva": ["cerny", "bily", "hnedy"],
        "spolecensky": ["ano", "ne"]
    }
    classes = ["V", "N", "Q"]
    objects = [
        (1, "N", "velky", "kratka", "bily", "ano"),
        (2, "N", "stredni", "bez", "cerny", "ne"),
        (3, "V", "maly", "dlouha", "cerny", "ne"),
        (4, "Q", "maly", "bez", "hnedy", "ne"),
        (5, "V", "velky", "bez", "bily", "ano"),
        (6, "Q", "stredni", "dlouha", "hnedy", "ano"),
        (7, "V", "velky", "dlouha", "bily", "ano"),
        (8, "V", "maly", "dlouha", "hnedy", "ano"),
        (9, "Q", "stredni", "dlouha", "hnedy", "ne"),
        (10, "Q", "stredni", "kratka", "bily", "ne"),
        (11, "V", "velky", "bez", "cerny", "ne"),
        (12, "N", "stredni", "bez", "bily", "ne"),
        (13, "V", "velky", "bez", "cerny", "ano"),
        (14, "V", "maly", "kratka", "bily", "ne"),
        (15, "V", "velky", "kratka", "hnedy", "ano")
    ]

    id3(attributes, classes, objects, None, None)