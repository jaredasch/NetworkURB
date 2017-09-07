import random


class Fluctuation:
    ID = 1

    def __init__(self, category, name):
        self.category = category
        self.name = name
        self.id = self.ID
        self.__class__.ID += 1

    def __repr__(self):
        return '<Fluctuation %d with name %s and category %s' % (self.id, self.name, self.category)


class Mission:
    ID = 1

    def __init__(self, priority, required_workflows):
        self.priority = priority
        self.required_workflows = required_workflows
        self.id = self.ID
        self.__class__.ID += 1

    def __repr__(self):
        return '<Mission %d with Priority %d and Required Workflows [%s]>' % (self.id, self.priority, ', '.join([str(resource.id) for resource in self.required_workflows]))


class Workflow:
    ID = 1

    def __init__(self, priority, required_resources):
        self.priority = priority
        self.required_resources = required_resources
        self.id = self.ID
        self.__class__.ID += 1
        for resource in self.required_resources:
            resource.availability = False

    def __repr__(self):
        return '<Workflow %d with Priority %s and Required Resources [%s]>' % (self.id, str(self.priority), ', '.join([str(resource.id) for resource in self.required_resources]))


class Resource:
    ID = 1

    def __init__(self, category, availability):
        self.category = category
        self.availability = availability
        self.id = self.ID
        self.__class__.ID += 1

    def __repr__(self):
        return '<%s Resource %d with Availability: %s>' % (self.category, self.id, str(self.availability))


RESOURCE_COUNT = 8
WORKFLOW_COUNT = 8
MISSION_COUNT = 3

categories = ['IoT Device', 'Cell phone', 'Drone']  # Just for testing
Resources = [Resource(random.choice(categories), True) for i in range(0, RESOURCE_COUNT)]
Workflows = [Workflow(None, random.sample(set(Resources), 5)) for j in range(0, WORKFLOW_COUNT)]
Missions = [Mission(k + 1, random.sample(set(Workflows), 3)) for k in range(0, MISSION_COUNT)]


def update_priorities(Missions):  # Make function so its easy to readjust after fluctuation
    for Mission in Missions:
        for Workflow in Mission.required_workflows:
            if not Workflow.priority or Workflow.priority > Mission.priority:  # Sets priority of WF to the highest priority Mission its used in
                Workflow.priority = Mission.priority


update_priorities(Missions)
