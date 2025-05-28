
from etl.management.management_interface import ManagementInterface
from typing import List


class SilaImplement(ManagementInterface, default=True):
    """
    Class to implement the email information service interface.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


    def feed_database(self, data ) -> None:
        pass
    
    
    def validate_input(self, data, **kwargs) -> None:
        pass