import json


with open('result_Yatsenyuk_AP.json', 'r') as f:
    distros_dict = json.load(f)


print distros_dict['retweets'][0]

final = {
    distros_dict['author_id']: {
        'friends': [],
        'activation': 0
    }
}

for retweet in distros_dict['retweets']:
    final[retweet['author_id']] = {
        'friends': [str(i[0]) for i in retweet['press_from']],
    }


# 1558866932 -> 1559073305
# 20 * 5160
# 100 * 1080
iter_number = 1
iter_time = 1558866932 + 1080

agents = [distros_dict['author_id']]

for retweet in distros_dict['retweets']:
    if retweet['time'] > iter_time:
        # with open('result-'+str(iter_number)+'.json', 'w') as fp:
        #     json.dump(final, fp)
        iter_time += 1080
        iter_number += 1
    final[retweet['author_id']]['activation'] = iter_number
    for friend in retweet["press_from"]:
        if str(retweet['author_id']) not in final[friend[0]]['friends']:
            final[friend[0]]['friends'].append(str(retweet['author_id']))

with open('result-for-reverse-1.json', 'w') as fp:
    json.dump(final, fp)
