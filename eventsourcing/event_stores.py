import abc
import sys
import json
from .event import IEvent
from .aggregates import AggregateRoot
from .exceptions import ConcurrencyError
import os
from typing import TypedDict

class IEventStore(abc.ABC):
    @abc.abstractmethod
    async def save_events(self, aggregate_id : str, events : list[IEvent], expected_version : int) -> None:...

    @abc.abstractmethod
    async def get_events_for_aggregate(self, aggregate_id : str) -> list[IEvent]:...
    
    async def save_aggregate(self, aggregate : AggregateRoot) -> None:
        await self.save_events(aggregate.to_stream_id(aggregate.id), aggregate.get_uncommitted_changes(), aggregate.version)
        aggregate.mark_changes_as_committed()
    

def get_event_class(class_name) -> type[IEvent]:
    for module in sys.modules.values():
        if hasattr(module, class_name):
            cls = getattr(module, class_name)
            if not issubclass(cls, IEvent):
                raise TypeError(f"{class_name} is not an Event")
            return cls
    raise ValueError(f"Class '{class_name}' not found.")

class EventDescriptor:
    def __init__(self, id : str, event_type: str, event_data : str, version : int) -> None:
        self.event_type = event_type
        self.__event_data = event_data
        self.__version = version
        self.__id = id

    @property
    def event_data(self) -> IEvent:
        return self.__event_data

    @property
    def version(self) -> int:
        return self.__version

    @property
    def id(self) -> str:
        return self.__id
    
    def __repr__(self) -> str:
        return f"(event:{self.event_type} - version:{self.version})"

class EventDescriptorDict(TypedDict):
    id : str
    event_type: str
    event_data : dict
    version : int


class InMemEventStore(IEventStore):

    def __init__(self) -> None:
        self.current : dict[str, list[EventDescriptor]] = {}

    async def save_events(self, aggregate_id: str, events: list[IEvent], expected_version: int) -> None:
        event_descriptors = self.current.get(aggregate_id)
        if not event_descriptors:
            if expected_version != -1:
                raise ConcurrencyError()
            event_descriptors = []
            self.current[aggregate_id] = event_descriptors

        elif event_descriptors[len(event_descriptors)-1].version != expected_version:
            raise ConcurrencyError()

        i = expected_version

        for event in events:
            i += 1
            event_descriptors.append(EventDescriptor(aggregate_id, event.type,json.dumps(event.to_dict()), i))

    async def get_events_for_aggregate(self, aggregate_id: str) -> list[IEvent]:
        event_descriptors = self.current.get(aggregate_id)
        if event_descriptors is None:
            return []
        return [get_event_class(desc.event_type).from_dict(json.loads(desc.event_data)) for desc in event_descriptors]
        

class JSONEventStore(IEventStore):

    def __init__(self, file_name : str) -> None:
        self.file_name = file_name
        data = {}
        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as f:
                data = json.load(f)
                
        self.current : dict[str, list[EventDescriptorDict]] = data

    async def save_events(self, aggregate_id: str, events: list[IEvent], expected_version: int) -> None:
        event_descriptors = self.current.get(aggregate_id)
        if not event_descriptors:
            if expected_version != -1:
                raise ConcurrencyError()
            event_descriptors = []
            self.current[aggregate_id] = event_descriptors

        elif event_descriptors[len(event_descriptors)-1]["version"] != expected_version:
            raise ConcurrencyError()

        i = expected_version

        for event in events:
            i += 1
            event_descriptors.append(EventDescriptorDict(id=aggregate_id, event_type=event.type,event_data=event.to_dict(), version=i))
            
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(self.current, f, ensure_ascii=False)
            
    async def get_events_for_aggregate(self, aggregate_id: str) -> list[IEvent]:
        event_descriptors = self.current.get(aggregate_id)
        if event_descriptors is None:
            return []
        return [get_event_class(desc["event_type"]).from_dict(desc["event_data"]) for desc in event_descriptors]