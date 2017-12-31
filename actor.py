"""
@author shattang
"""
from collections import deque
import threading
import logging
import random
import time

class ActorExecutor(object):
    def __init__(self, system, **kwargs):
        self.system = system #type: ActorSystem
        self.max_num_messages_per_run = kwargs.get('max_num_messages_per_run',
                                                   ActorSystem.DEFAULT_MAX_NUM_MESSAGES_PER_RUN)
        self._flag = True
        self._lock = threading.Lock()
        self._actor_queue = deque()
        self._thread = None

    def is_stopping(self):
        return not self._flag

    def start(self):
        if not self._thread:
            self._thread = threading.Thread(target=self._run)
            self._thread.start()

    def stop(self, timeout=None):
        self._flag = False
        self._thread.join(timeout)

    def enqueue_actor(self, actor):
        with self._lock:
            self._actor_queue.append(actor)

    def _run(self):
        logging.info("ActorExecutor(%s): started", self)
        while self._flag:
            actor = None #type: Actor
            with self._lock:
                if self._actor_queue:
                    actor = self._actor_queue.popleft()

            if actor:
                if actor.is_busy() or actor.run(self, self.max_num_messages_per_run):
                    self.system.enqueue_actor(actor)
            else:
                time.sleep(0.25)

class ActorSystem(object):
    DEFAULT_MAX_NUM_MESSAGES_PER_RUN = 8

    def __init__(self, num_executors=1, **kwargs):
        self._random = random.Random()
        self._executors = []
        for i in xrange(num_executors):
            self._executors.append(ActorExecutor(self, **kwargs))

    def start(self):
        for executor in self._executors:
            executor.start()

    def send_message(self, actor, message):
        enqueue_actor = actor.enqueue_message(message)
        if enqueue_actor:
            self.enqueue_actor(actor)

    def enqueue_actor(self, actor):
        i = self._random.randint(0, len(self._executors)-1)
        self._executors[i].enqueue_actor(actor)

    def stop(self, timeout=None):
        for executor in self._executors:
            executor.stop(timeout)

class Actor(object):
    POISON_PILL = object()

    def __init__(self, on_receive):
        self._on_receive = on_receive
        self._lock = threading.Lock()
        self._msg_queue = deque()

    def is_busy(self):
        return self._lock.locked()

    def enqueue_message(self, message):
        with self._lock:
            was_empty = not self._msg_queue
            self._msg_queue.append(message)
        return was_empty

    def run(self, executor, max_num_messages=ActorSystem.DEFAULT_MAX_NUM_MESSAGES_PER_RUN):
        for i in xrange(max_num_messages):
            with self._lock:
                if self._msg_queue:
                    msg = self._msg_queue.popleft()
                else:
                    break

            if executor.is_stopping():
                return False

            if msg == Actor.POISON_PILL:
                return False

            try:
                self._on_receive(msg)
            except:
                logging.exception("ERROR: Actor.run: actor=%s" % self)
                return False

        with self._lock:
            return bool(self._msg_queue) #has more messages


if __name__ == "__main__":
    system = ActorSystem(2)
    system.start()
    def actor1(msg):
        print "%s: A1 %s" % (threading.current_thread(), msg)
    def actor2(msg):
        print "%s: A2 %s" % (threading.current_thread(), msg)

    a1 = Actor(actor1)
    a2 = Actor(actor2)

    for i in xrange(10):
        system.send_message(a1, i)
        system.send_message(a2, i)

    time.sleep(5)
    system.stop(timeout=1)