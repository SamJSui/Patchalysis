''' Health Controller 

This module contains the HealthController class, which is responsible for handling the logic for health checks.

Classes:
    HealthController: A controller class for health checks.

Contributors:
    Sam Sui
'''

class HealthController:
    def __init__(self):
        pass

    def health_check(self):
        return { 'message': 'Healthy' }, 200