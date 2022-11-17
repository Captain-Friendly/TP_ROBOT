# Pascal Arès
# 2022-27-10

# Classe ModuleInertiel: Classe wapper au module ICM20948
# Classe FauxModuleInertiel: Classe permettant d'imiter la classe ModuleInertiel
# pour les tests unitaires.

# from icm20948 import ICM20948

class ModuleInertiel:
    def __init__(self, imu):
        self.__imu = imu
        
    def obtenir_mesure(self):
        return self.__imu.read_accelerometer_gyro_data()


class FauxModuleInertiel:
    def __init__(self):
        self.ax = 0 
        self.ay = 0 
        self.az = 0 
        self.gx = 0 
        self.gy = 0 
        self.gz = 0

    def obtenir_mesure(self):
        return (self.ax, self.ay, self.az, self.gx, self.gy, self.gz)