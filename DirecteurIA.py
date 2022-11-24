from Robot import Robot
class DirecteurIA:

    def __init__(self, robot:Robot, correcteur_direction, detecteur_obstacle, localiseur_radio):
        self.__correcteur_direction = correcteur_direction
        self.__robot
        self.__module_inertiel



    def __avancer_robot(self):
        self.__robot.avancer()

    def __tourner_robot(self, angle_voulu):
        from icm20948 import ICM20948
        from ModuleInertiel import ModuleInertiel

        module_imertiel = ModuleInertiel(ICM20948)