import uuid
import math
import json

current_time = 0

with open('result-for-main-1.json', 'r') as f:
    db = json.load(f)

# db = {
#     'Agent1': {
#         'friends': ['person1', 'person2', 'person3']
#     },
#     'person1': {
#         'friends': {
#             'Agent1': 0.8,
#             'person3': 0.5
#         }
#     },
#     'person2': {
#         'friends': {
#             'Agent1': 0.5
#         }
#     },
#     'person3': {
#         'friends': {
#             'Agent1': 0.2,
#             'person1': 0.5
#         }
#     }
# }


def fun(time):
    # return (1/-math.pow(time + 1, press_coef)) + 1
    return math.pow(time + 1, 0.25) - 1


class InfoClient:
    def __init__(self):
        self.db = db

    def get_friends(self, person_id):
        friends = self.db.get(person_id).get('friends')
        if type(friends) is list:
            return friends
        elif type(friends) is dict:
            return friends.keys()
        else:
            return []

    def get_weight(self, person_id, friend_id):
        friends = self.db.get(person_id).get('friends')
        if type(friends) is dict:
            return friends.get(friend_id)
        else:
            import pdb; pdb.set_trace()


class NodeManager:
    def __init__(self):
        self.activated_nodes = []
        self.potential_nodes = []

    def get_potential_nodes(self):
        return self.potential_nodes

    def save_node(self, node):
        self.potential_nodes.append(node)

    def get_node(self, node_id):
        for node in self.potential_nodes:
            if node.get_id() == node_id:
                return node
        for node in self.activated_nodes:
            if node.get_id() == node_id:
                return "START"

    def activate(self, node):
        self.activated_nodes.append(node)
        try:
            self.potential_nodes.remove(node)
        except ValueError:
            pass


class BaseNode(object):
    def __init__(self, id=None):
        if id is None:
            self._id = str(uuid.uuid4())[:8]
        else:
            self._id = id
        self._atime = None

    def get_id(self):
        return self._id

    def set_action_time(self, time):
        self._atime = int(time)

    def get_action_time(self):
        return self._atime


class AgentNode(BaseNode):
    def __init__(self, id):
        super(AgentNode, self).__init__(id)

    def action(self, nm, ic, time):
        nm.activate(self)
        self.set_action_time(time)
        print "Agent: " + str(self.get_id())
        for friend in self.get_friends(ic):
            print "Press on: " + friend
            node = nm.get_node(friend)
            if node is not None:
                node.add_input_node(self)
            else:
                node = Node(friend, self, nm, ic, time)

    def get_friends(self, infoClient):
        return infoClient.get_friends(self.get_id())


class Node(BaseNode):
    def __init__(self, id, input_node, nm, infoClient, start_pressure):
        super(Node, self).__init__(id)
        self._stime = int(start_pressure)
        # input_nodes should be a list of ids or list of objects
        # input_nodes[0] = (id, weight, start_pressure, power)
        self._input_nodes = set()
        self.infoClient = infoClient
        self._input_nodes.add(input_node)
        input_node_id = input_node.get_id()
        self.weights = {
            input_node_id: self.get_weight(input_node_id)
        }
        self.threshold = 0.5
        nm.save_node(self)

    def get_weight(self, input_id):
        return self.infoClient.get_weight(self.get_id(), input_id)

    def add_input_node(self, node):
        self._input_nodes.add(node)

    def calculate(self):
        sum = 0
        for node in self._input_nodes:
            try:
                sum += self.get_weight(node.get_id()) * \
                fun(current_time - node.get_action_time())
            except:
                import pdb; pdb.set_trace()
        print self.get_id() + " " + str(sum)
        return sum > self.threshold

    def get_friends(self, infoClient):
        return infoClient.get_friends(self.get_id())

    def activate(self, nm, ic, time):
        # TODO: search for friends and init their nodes if they are not inited
        # if node is broker
        nm.activate(self)
        print "Agent: " + str(self.get_id())
        self.set_action_time(time)
        for friend in self.get_friends(ic):
            node = nm.get_node(friend)
            if node == "START":
                print "Cant press on " + friend
                continue
            print "Press on: " + friend
            if node is not None:
                node.add_input_node(self)
            else:
                node = Node(friend, self, nm, ic, time)


if __name__ == "__main__":
    nm = NodeManager()
    ic = InfoClient()
    activation_times = []
    agents = [AgentNode("1896985040")]
    for agent in agents:
        agent.action(nm, ic, current_time)

    while current_time < 110:
        print "Time: " + str(current_time)
        nodes_under_pressure = nm.get_potential_nodes()
        for node in nodes_under_pressure:
                if node.calculate():
                    node.activate(nm, ic, current_time)
                    activation_times.append((node.get_id(), current_time))
        current_time += 1
        if len(activation_times) >= 100:
            break

    print activation_times


    with open('result-for-reverse-1.json', 'r') as f:
        reverse = json.load(f)

    print len(reverse)
    print len(activation_times)

    count = len(activation_times)
    g = 0.0
    for person in activation_times:
        print person[0] + " " + str(person[1]) + " " + str(reverse[person[0]]['activation'])
        g += abs((person[1]/reverse[person[0]]['activation']) - 1)
    print g/count
