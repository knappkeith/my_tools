import simcity_items
import json

class item(object):
    def __init__(self, item_name):
        self.item_name = item_name
        self.item = dict(simcity_items.items[self.item_name])
        self.time = dict(self.item['time'])
        self.source = self.item['source']
        self.cost = self.item['cost']
        self.name = self.item['name']
        self.required = dict(self.item['required'])
        self.tree = self._grow_tree({
            self.item_name: dict(self.required)})

    @property
    def factory_items(self):
        return self._get_factory_items({self.item_name: 1})

    def get_factory_items(self, quantity=1):
        return self._get_factory_items({self.item_name: quantity})

    def _get_factory_items(self, requires):
        new_requires = {}
        for key, value in requires.iteritems():
            if simcity_items.items[key][
                    'source'] == 'factory' or simcity_items.items[key][
                    'source'] is None:
                new_requires[key] = value
            else:
                org_value = int(value)
                for new_requirement, new_amount in simcity_items.items[
                        key]['required'].iteritems():
                    if new_requirement in new_requires.keys():
                        new_requires[new_requirement] += new_amount * value
                    else:
                        new_requires[new_requirement] = new_amount * value
        all_factory = True
        for key, value in new_requires.iteritems():
            if simcity_items.items[key]['source'] != 'factory':
                all_factory = False
        if all_factory:
            return new_requires
        else:
            return self._get_factory_items(new_requires)

    @property
    def all_time(self):
        return self._get_minimum_time({self.item_name: 1}, self.time)

    @property
    def max_time(self):
        def add_time(a, b):
            new_minutes, new_seconds = divmod(a['seconds'] + b['seconds'], 60)
            new_hours, new_minutes = divmod(
                a['minutes'] + b['minutes'] + new_minutes, 60)
            c = {
                "seconds": new_seconds,
                "minutes": new_minutes,
                "hours": new_hours + a['hours'] + b['hours']
            }
            return c

        total_time = {'hours': 0, 'minutes': 0, 'seconds': 0}
        for time in self.all_time.values():
            total_time = add_time(total_time, time)
        return total_time


    def _get_minimum_time(self, requires, time={}):
        def get_time(a):
            return a['seconds'] + (a['minutes'] * 60) + (a['hours'] * 60 * 60)

        def add_time(a, b):
            new_minutes, new_seconds = divmod(a['seconds'] + b['seconds'], 60)
            new_hours, new_minutes = divmod(
                a['minutes'] + b['minutes'] + new_minutes, 60)
            c = {
                "seconds": new_seconds,
                "minutes": new_minutes,
                "hours": new_hours + a['hours'] + b['hours']
            }
            return c

        new_requires = {}
        for key, value in requires.iteritems():
            if simcity_items.items[key]['source'] == 'factory':
                new_requires[key] = value
                if not time.has_key('factory'):
                    time['factory'] = dict(
                        simcity_items.items[key]['time']['factory'])
                else:
                    if get_time(time['factory']) < get_time(
                            simcity_items.items[key]['time']['factory']):
                        time['factory'] = dict(
                            simcity_items.items[key]['time']['factory'])
            elif simcity_items.items[key]['source'] is not None:
                org_value = int(value)
                for new_requirement, new_amount in simcity_items.items[
                        key]['required'].iteritems():
                    if new_requirement in new_requires.keys():
                        new_requires[new_requirement] += new_amount * value
                    else:
                        new_requires[new_requirement] = new_amount * value
                    manufacturer, new_time = simcity_items.items[
                        new_requirement]['time'].items()[0]
                    if manufacturer == 'factory':
                        if not time.has_key('factory'):
                            time['factory'] = dict(
                                simcity_items.items[
                                    new_requirement]['time']['factory'])
                        else:
                            if get_time(time['factory']) < get_time(
                                    simcity_items.items[
                                        new_requirement]['time']['factory']):
                                time['factory'] = dict(
                                    simcity_items.items[new_requirement][
                                        'time']['factory'])
                    else:
                        if time.has_key(manufacturer):
                            for i in range(0, value):
                                time[manufacturer] = add_time(
                                    new_time, time[manufacturer])
                        else:
                            time[manufacturer] = dict(new_time)
        all_factory = True
        for key, value in new_requires.iteritems():
            if simcity_items.items[key]['source'] != 'factory':
                all_factory = False
        if all_factory:
            return time
        else:
            return self._get_minimum_time(new_requires, time)

    def _grow_tree(self, level):
        if isinstance(level, dict):
            new_level = dict(level)
            for k, v in new_level.iteritems():
                if isinstance(v, int):
                    if simcity_items.items[k]['required'] == {}:
                        new_level[k] = 'factory'
                    else:
                        new_level[k] = dict(self._grow_tree(
                            simcity_items.items[k]['required']))
                elif isinstance(v, dict):
                    new_level[k] = dict(self._grow_tree(v))
        return new_level
