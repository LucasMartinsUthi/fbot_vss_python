import socket
import sys
import threading
import time

sys.path.append("..")

# from protos.packet import Environment, Packet
# from protos.command import Commands, Command

class Communication:
    
    LOCALHOST = "127.0.0.1"
    HOST = "224.0.0.1"
    VISION_ADDR = 10002
    # SIM_ADDR = 10001
    COMMAND_ADDR = 20011
    
    __environment = None
    __thread = None
    __stop = False

    def __init__(self):
        self.__stop = False
        
        self.__thread = threading.Thread(target=self.__parse_environment, args=())
        self.__thread.start()
        
    def __parse_environment(self):
        count = 0
        
        while not self.__stop:
            # socket = self.__create_socket(self.VISION_ADDR)
            
            # environment = Environment()
                   
            # data, _ = socket.recvfrom(2048)
            # environment.ParseFromString(data)
                        
            self.__environment = count
            
            count += 1
            
            time.sleep(0.1)
            
    def __create_socket(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # sock.bind((self.LOCALHOST, port))
        sock.bind((self.HOST, port))
        
        return sock
        
    def stop(self):
        self.__stop = True
        self.__thread.join()
        
    def environment(self):
        return self.__environment
    
    def frame(self):
        return self.__environment.frame
    
    def ball(self):
        frame = self.frame()
        return frame.ball
    
    def blue_team(self):
        frame = self.frame()
        return frame.robots_blue

    def yellow_team(self):
        frame = self.frame()
        return frame.robots_yellow
    
    def blue_robot(self, id):
        return self.blue_team()[id]
    
    def yellow_robot(self, id):
        return self.yellow_team()[id]


# Todo 
# - send command

# def move(id, ToF, VE,VD):
#     pacote = Packet()
#     cmd = Command()
#     cmd.id = id
#     cmd.yellowteam = ToF
#     cmd.wheel_left = VE
#     cmd.wheel_right = VD
#     pacote.cmd.robot_commands.append(cmd) #esta adiconando ao packet as informações do command ## appen() adiciona um item no final de lista 
#     pacote_byte = pacote.SerializeToString()# .SerializeToString() serealiza dos dados
#     socket_envia.sendto(pacote_byte,(localhost, porta_envia))
