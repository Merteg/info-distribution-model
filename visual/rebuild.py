import json


with open('result_Yatsenyuk_AP.json', 'r') as f:
    distros_dict = json.load(f)


print distros_dict['retweets'][0]

final = {
    "nodes": [
        {
            "id": distros_dict['author_id'],
            "name": distros_dict['author_name']
        }
    ],
    "links": []
}

# 1558866932 -> 1559073305
# 20 * 10319
iter_number = 0
iter_time = 1558866932 + 10319

agents = [distros_dict['author_id']]

for retweet in distros_dict['retweets']:
    if retweet['time'] > iter_time:
        with open('result-'+str(iter_number)+'.json', 'w') as fp:
            json.dump(final, fp)
        iter_time += 10319
        iter_number += 1
    agents.append(retweet['author_id'])
    final["nodes"].append({
        "id": retweet['author_id'],
        "name": retweet['author_name']
    })
    for link in retweet["press_from"]:
        if link[0] in agents:
            final["links"].append({
                "source": link[0],
                "target": retweet['author_id']
            })

with open('result-last.json', 'w') as fp:
    json.dump(final, fp)
