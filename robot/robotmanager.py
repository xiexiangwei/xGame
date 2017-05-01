#coding=utf-8

import robot
class RobotManager(object):
    def __init__(self):
        self.robotmap={}

    def start(self,num):
        for i in range(num):
            r= robot.Robot(i)
            r.start()
            self.robotmap[i]=r


instance=RobotManager()


