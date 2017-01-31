"""
Abstract Configuration class
Based on Borg pattern (similar to Singleton)
"""
from abc import ABCMeta


class AbstractConfig:
    __metaclass__ = ABCMeta
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def __str__(self):
        return self.__shared_state
