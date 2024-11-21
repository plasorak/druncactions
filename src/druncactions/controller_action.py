import abc
import logging
from druncactions.exceptions import ActionNotImplementedException


class ControllerAction:
    def __init__(self, name:str, configuration):
        self.name = name
        self.actions = {}
        self.mandatory = configuration.mandatory
        self.log = logging.getLogger(f'{name}_controller_action')


    def register_method(self, method, transition, pre_or_post):
        self.actions[f'{pre_or_post}_{transition}'] = method


    def execute(self, transition, pre_or_post, **kwargs):
        if f'{pre_or_post}_{transition}' in self.actions:
            return self.actions[f'{pre_or_post}_{transition}'](**kwargs)
        else:
            if self.mandatory:
                raise ActionNotImplementedException(f'Mandatory action \'{pre_or_post}_{transition}\' not implemented in {self.name}')
            else:
                self.log.warning(f'Optional action \'{pre_or_post}_{transition}\' not implemented, skipping')
                return None


    @abc.abstractmethod
    def provides(self, transition):
        pass