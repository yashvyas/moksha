# -*- coding: utf-8 -*-
import psycopg2, time

class PGTopicStore:

    def __init__(self, **kwargs):
        dbname = kwargs.get('dbname', 'trades')
        user = kwards.get('user', 'postgress')
        password = kwargs.get('password', 'password')
        host = kwargs.get('host', '127.0.0.1')
        port = kwargs.get('port', 5432)
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    def store_topic_data(self, topic, data, **kwargs):
        key = kwargs.get('key', int(time.time()*1000*1000))
        curr = self.conn.cursor()
        curr.execute("INSERT INTO {} (key, data) values (%s, %s)".format(key), (key, data))
        conn.commit()
        curr.close()

    def get_topic_data(self, topic, **kwargs)
        key = kwargs.get('key', None)
        statement = ""

        if key is None:
            statement = "Select * from {}".format(topic)
        else:
            statemement = "Select * from {} where key = {}".format(topic, key)

        curr = self.conn.curr()
        curr.execute(statement)
        data = curr.fetchall()
        curr.close()
        return data

    def close(self):
        self.conn.close()



