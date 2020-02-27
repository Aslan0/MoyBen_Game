import pygame

# You can have several User Events, so make a separate Id for each one
EVENT_SOUNDEND_MEOW = pygame.USEREVENT + 0

class EventListener:

    def notify(self, event):
        raise NotImplementedError("Listeners need to be notifiyable")


class EventManager(EventListener):
    def __init__(self):
        self.listener_dict = dict()

    def register(self, event_type, listener):
        if not event_type in self.listener_dict:
            self.listener_dict[event_type] = set()
        self.listener_dict[event_type].add(listener)

    def unregister(self, event_type, listener):
        if event_type in self.listener_dict:
            self.listener_dict[event_type].remove(listener)

    def notify(self, event):
        if self.listener_dict and event.type in self.listener_dict:
            for listener in self.listener_dict[event.type]:
                listener.notify(event)


global_eventmanager = EventManager()