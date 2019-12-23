from collections import defaultdict
import logging

# gal shashua 315878397

logging.basicConfig(filename='LoggerFile.log', level=logging.INFO)

class Node(object):
    def __init__(self, name):
        self.name = str(name)
        self.degree = 0
        self.earliestTime = 0
        self.latestTime = 0
        logging.info("New node: " + repr(self) + " name: " + name)

    def slack_time_for_node(self):
        logging.info("Slack time for node : " + self.name + " slack = " + str(self.latestTime - self.earliestTime))
        return self.latestTime - self.earliestTime

    def __str__(self):
        logging.info("str method for node : " + repr(self))
        return "Node name: " + self.name

    def __repr__(self):
        logging.info("repr method for node : " + self.name)
        return self.name

class Activity(object):
    def __init__(self, name, duration):
        logging.info("New activity! name: " + name + ", duration: " + str(duration))
        self.name = str(name)
        self.duration = duration

    def __str__(self):
        logging.info("str method for activity : " + self.name + "' activity")
        return "Activity name: " + self.name + " , Duration = " + str(self.duration)

    def __repr__(self):
        logging.info("repr method for activity : " + self.name)
        return self.name

class Queue(object):
    def __init__(self):
        self.queue = []
        logging.info("New queue! name : " + str(self.queue))

    def is_empty(self):
        return self.queue == []

    def insert(self, item):
        self.queue.insert(0, item)
        logging.info("Insert new item to queue : " + str(item))

    def delete(self):
        logging.info("Delete item from queue : " + str(self.queue[0]))
        return self.queue.pop()

    def __str__(self):
        logging.info("str method for queue : " + str(list(self.queue)))
        return "Queue list:" + str(list(self.queue))

class Pert(object):

    def __init__(self, graph_dict=None):
        logging.info("New pert! " + repr(self) + " created, graph: " + str(graph_dict))
        if graph_dict is None:
            graph_dict = dict()
        self.__graph_dict = graph_dict
        self.topological_list = []

    def __str__(self):
        logging.info("str method for pert : " + repr(self))
        string = "Adjacency list: \n"
        for vertex in self:
            string += repr(vertex) + repr(list(self[vertex])) + "\n"
        return string

    def __getitem__(self, name):
        logging.info("getitem method for pert : " + repr(self))
        return self.__graph_dict[name]

    # iterator the iterate over the nodes
    def __iter__(self):
        logging.info("iter method for pert : " + repr(self))
        return iter(self.__graph_dict)

    def items(self):
        logging.info("items method for pert : " + repr(self))
        return self.__graph_dict.items()

    def add_activity(self, node_from, act=None, node_to=None):
        logging.info("add_activity method for pert : " + repr(self) + " Node from: " + str(
            node_from) + " activity: " + str(activity) + " Node to: " + str(node_to))
        if not node_to:
            self.__graph_dict[node_from] = []
        else:
            self.__graph_dict[node_from] = [[node_to, act]]

    def get_degree(self):
        logging.info("get_degree method for pert : " + repr(self))
        for node in self:
            for lst in self[node]:
                lst[0].degree = lst[0].degree + 1

    def sorting(self, direction):
        logging.info("sorting method for pert : " + repr(self) + " with direction : " + str(direction))
        queue = Queue()
        self.topological_list.clear()
        self.get_degree()
        for node in self:
            if node.degree == 0:
                queue.insert(node)
                self.topological_list.append(node)
        while not queue.is_empty():
            node = queue.delete()
            for u in self[node]:  # for each node u in the adjacency list of u
                u[0].degree = u[0].degree - 1
                if direction == "FORWARD":
                    u[0].earliestTime = max(u[0].earliestTime, node.earliestTime + u[1].duration)
                else:
                    u[0].latestTime = min(u[0].latestTime, node.latestTime - u[1].duration)
                if u[0].degree == 0:
                    queue.insert(u[0])
                    self.topological_list.append(u[0])
        return self.topological_list

    def reverse_graph(self, append):
        logging.info("reverse_graph method for pert : " + repr(self) + " with append : " + str(append))
        reverse = defaultdict(list)
        node1 = list(self.__graph_dict.keys())[-1]
        for key, value in self.items():
            for node, act in value:
                if append:
                    node.latestTime = node1.earliestTime
                reverse[node].append((key, act))
        for node in graph:
            if node not in reverse:
                reverse[node] = []
        self.__graph_dict = reverse

    def order_slack_time(self):
        logging.info("order_slack_time method called")
        desc_list = dict()
        for node in self:
            desc_list[node] = node.slack_time_for_node()
        desc_list = sorted(desc_list.items(), key=lambda kv: kv[1], reverse=True)
        return desc_list

    def find_isolated(self):
        logging.info("find_isolated method for pert : " + repr(self))
        isolated = []
        self.get_degree()
        for i in self.__graph_dict.keys():
            if i.degree == 0 and not self[i]:
                isolated.append(i)
        return isolated

    # Method for calculating the slack time
    def slack_time(self):
        logging.info("slack_time method for pert : " + repr(self))
        slack_time = 0
        for s in self.__graph_dict.keys():
            slack_time += (s.latestTime - s.earliestTime)
        return slack_time

    def critical_path(self):
        logging.info("critical_path method for pert : " + repr(self))
        self.sorting("FORWARD")
        self.reverse_graph(1)
        self.sorting("BACKWARD")
        self.reverse_graph(0)
        critical_path_lst = []
        for s in reversed(self.topological_list):
            if s.latestTime == s.earliestTime:
                critical_path_lst.append(s)
        return critical_path_lst

    def short_critical_path(self):
        logging.info("short_critical_path method called")
        lst = self.critical_path_activities()
        max_short_list = dict()
        for task in lst:
            task_duration = task.duration
            while True:
                if task.duration == 0:
                    break
                task.duration = task.duration - 1
                temp = self.critical_path_activities()
                if task.duration <= 1:
                    max_short_list[task.name] = 1
                    task.duration = task_duration
                    break
                if task not in temp:
                    max_short_list[task.name] = task_duration - task.duration - 1
                    task.duration = task_duration
                    break
        return max_short_list

    def critical_path_activities(self):
        logging.info("critical_path_activities method called")
        cpm = self.critical_path()
        cpm_copy = cpm[:]
        iterator = iter(cpm_copy)
        next(iterator)
        lst = []
        cpm.pop()
        for node in cpm:
            item = next(iterator).name
            for node2 in self[node]:
                if item == node2[0].name:
                    lst.append(node2[1])
        return lst

if __name__ == "__main__":
    start = Node("start")
    end = Node("end")
    a = Node("A")
    b = Node("B")
    c = Node("C")
    d = Node("D")
    e = Node("E")
    f = Node("F")
    g = Node("G")

    task1 = Activity("Task1", 4)
    task2 = Activity("Task2", 2)
    task3 = Activity("Task3", 2)
    task4 = Activity("Task4", 5)
    task5 = Activity("Task5", 6)
    task6 = Activity("Task6", 4)
    task7 = Activity("Task7", 6)
    task8 = Activity("Task8", 5)
    task9 = Activity("Task9", 5)
    task10 = Activity("Task10", 8)
# this tasks are for the activities priorities
    task11 = Activity("Task11", 0)
    task12 = Activity("Task12", 0)
    task13 = Activity("Task13", 0)
    task14 = Activity("Task14", 0)
    task15 = Activity("Task15", 0)

    graph = {start: [[a, task1], [b, task5], [c, task9]],
             a: [[b, task11]],
             b: [[d, task2]],
             c: [[f, task6]],
             d: [[e, task8], [f, task12], [g, task3], [end, task10], [c, task13]],
             e: [[end, task4], [f, task15]],
             f: [[end, task7]],
             g: [[end, task14]],
             end: []}

# ---------------- 1. Initializes a graph object ----------------
    graph = Pert(graph)
    cpm1 = graph.critical_path()
    print("\n -- Question 1 -- \nThe graph initialization succeeded\n")

# ---------------- 4. method that return slack's time for each activity in descending order ----------------
    print(" -- Question 4 -- \nSlack's time for each activity")
    print(graph.order_slack_time())

# ---------------- 5. method that return the sum of the slacks time ----------------
    print("\n -- Question 5 -- \nSum of the slacks time: " + str(graph.slack_time()))

# ---------------- 7. iterator that iterate over all the nodes ----------------
    print("\n -- Question 7 -- \nIterate over all the nodes:")
    for activity in iter(graph):
        print(activity)

# ---------------- 8. method that find “Critical path” of the project ----------------
    print("\n -- Question 8 -- \nCritical path:")
    for i in cpm1:
        print(str(i.name) + " ", end="")

# ---------------- 9. represent maximum shorting time duration of task ----------------
    print("\n\n -- Question 9 -- \nMaximum shortening times:")
    print(graph.short_critical_path())

# ---------------- 2. Build method that add activity to the project ----------------
    newActivity = Activity("Task11", 6)
    graph.add_activity(Node("H"))
    graph.add_activity(end, newActivity, Node("H"))
    print("\n -- Question 2 -- \nAdd new activity:\n" + str(Node("H")) +"\n" + str(newActivity))

# ---------------- 3. Build method to find isolate activities ----------------
    print("\n -- Question 3 -- \nIsolated nodes are: " + str(graph.find_isolated()) + "\n")