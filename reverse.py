import math
import json

# db = {
#     'Agent1': {
#         'friends': ['person1', 'person2', 'person3'],
#         'activation': 0
#     },
#     'person1': {
#         'friends': ['Agent1', 'person3'],
#         'activation': 6
#     },
#     'person2': {
#         'friends': ['Agent1'],
#         'activation': 16
#     },
#     'person3': {
#         'friends': ['Agent1', 'person1'],
#         'activation': 13
#     }
# }

with open('result-for-reverse-1.json', 'r') as f:
    db = json.load(f)


def fun(time):
    # return (1/-math.pow(time + 1, press_coef)) + 1
    return math.pow(time + 1, 0.25) - 1

def get_max_time():
    maximum = 0
    for person in db.keys():
        if person['activation'] > maximum:
            maximum = person['activation']
    return maximum

def is_press(current, name):
    if db[name]['activation'] is not None:
        return db[name]['activation'] < db[current]['activation']

def get_pressure_time(person, friend):
    return db[person]['activation'] - db[friend]['activation']

def calculate(input_nodes):
    sum = 0
    for node in input_nodes:
        sum += node[2] * node[1]
    return sum

if __name__ == "__main__":
    result = {}
    for person in db.keys():
        if person == "1896985040":
            result[person] = {'friends': db[person]['friends']}
        else:
            result[person] = {'friends': {}}
            for friend in db[person]['friends']:
                result[person]['friends'][friend] = 0

    for person in db.keys():
        friends = [f for f in db[person]['friends'] if is_press(person, f)]

        func_arr = []
        for friend in friends:
            func_arr.append([friend, fun(get_pressure_time(person, friend)), 0.5])

        
        alpha = 0.005
        delta = 1
        max_loop = 500
        loop = 0
        index = 0
        func_arr.sort(key=lambda x: x[1], reverse=True)
        delta = calculate(func_arr) - 0.5
        while index < len(func_arr):
            previous = func_arr[index][2]
            if delta > alpha:
                if func_arr[index][2] < 0.1:
                    index += 1
                    continue
                func_arr[index][2] -= 0.1
            elif delta < 0:
                if func_arr[index][2] > 0.9:
                    index += 1
                    continue
                func_arr[index][2] += 0.1
            else:
                break
            if abs(calculate(func_arr) - 0.5) > abs(delta):
                func_arr[index][2] = previous
                index += 1
            else:
                delta = calculate(func_arr) - 0.5
        
        if person != "1896985040":
            for a in func_arr:
                result[person]['friends'][a[0]] = a[2]

        print person + ", " + str(db[person]['activation']) + ": " + str(func_arr)

    with open('result-for-main-1.json', 'w') as fp:
        json.dump(result, fp)



