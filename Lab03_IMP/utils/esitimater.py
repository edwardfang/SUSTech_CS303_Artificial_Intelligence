#!/usr/bin/env python2
'''
ISE
'''
from __future__ import division
import random
import logging


class Estimater(object):
    '''
    Class to solve the problem 01
    '''

    def __init__(self, graph, seeds, model, solution_receiver, processid, ter_type, random_s=None):
        model_map = {'IC': self.ic_simulate, 'LT': self.lt_simulate}
        if random_s:
            random.seed(random_s)
        self.graph = graph
        self.seeds = seeds
        self.nodes = self.graph.vertices()
        self.model = model_map[model]
        self.solution_receiver = solution_receiver
        self.processid = processid
        self.ter_type = ter_type
        self.cur_avg = 0
        self.cur_round = 0

    def get_result(self):
        '''
        get the influenece valuence
        '''
        # logging.debug("get result")
        sim_round = 100
        sum_activated = 0
        for _ in range(sim_round):
            estimated_set = self.model()
            sum_activated += len(estimated_set)
        self.cur_avg = (self.cur_round * self.cur_avg +
                        sum_activated / sim_round) / (self.cur_round + 1)
        self.cur_round += 1
        logging.debug("id %d, avg %f", self.processid, self.cur_avg)
        self.solution_receiver.put([self.processid, self.cur_avg])

    def estimate(self):
        '''
        see the termination type to decide
        '''
        if self.ter_type == 0:
            # logging.debug('a')
            for _ in range(100):
                self.get_result()
        else:
            # logging.debug('b')
            while True:
                self.get_result()

    def ic_simulate(self):
        '''
        use the independent Cascade model
        '''
        activated = set()
        next_layer = self.seeds
        while next_layer:
            new_layer = set()
            for node in next_layer:
                for linked_node, value in self.graph[node].iteritems():
                    rnd = random.random()
                    if linked_node not in activated and rnd < value['weight']:
                        new_layer.add(linked_node)
            activated = set.union(activated, next_layer)
            # print(activated)
            next_layer = new_layer
        return activated

    def lt_simulate(self):
        '''
        use the independent Cascade model
        '''
        activated = self.seeds
        threshold = dict()
        for node in self.nodes:
            threshold[node] = random.random()
        changed = True
        while changed:
            changed = False
            inactive = set.difference(set(self.nodes), activated)
            for node in inactive:
                indicator = 0
                for linked_node, value in self.graph.inverse[node].iteritems():
                    if linked_node in activated:
                        indicator += value['weight']
                if indicator > threshold[node]:
                    activated.add(node)
                    changed = True
        return activated
