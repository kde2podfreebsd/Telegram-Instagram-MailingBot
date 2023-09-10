from abc import ABCMeta
from abc import abstractmethod


class UserAgentInterface(metaclass=ABCMeta):

    @abstractmethod
    def joinChat(self, chat: str):
        '''
        Implement join chat func
        :param chat:
        :return:
        '''