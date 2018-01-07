# -*- coding: utf-8 -*-
from cassandra.cluster import Cluster

class CassandraTopicStore:
    def __init__(self, **kwargs):
        contact_points = kwargs.get('contact_points', '127.0.0.1')
        
        

