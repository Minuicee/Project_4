from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
import sys
import random


character_image_path = {1:"Game/Game_Character_1.png", 2:"Game/Game_Character_2.png", 3:"Game/Game_Character_3.png", 4:"Game/Game_Character_death.png"}
Death_block_image_path = {1: "Game/Death_1.png", 2: "Game/Death_2.png", 3: "Game/Death_3.png", 4: "Game/Death_4.png"}
world_image_path = {1: "Game/world1.jpg", 2: "Game/world2.jpg", 3: "Game/world3.png"}



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

        #! Changeable variables
        self.parameter = 1 # default: 1 - Jump height 
        self.debounce_time = 10 # default: 10 - time between jumps (in milliseconds)
        self.airTime = 15  # default: 15 - time each jump takes = airtime * 50 (milliseconds)
        self.Death_block_moveSpeed = 10 # default: 10 - time between every move (in milliseconds)
        self.Death_block_spawnRate = 1500 # default: 1500 - time between every spawn (in seconds)
        self.Death_block_pxPerMove = 10 # default: 10 - pixels per move
        
        #* initialize variables/timers
        self.jump_steps = 0
        self.jump_debounce = False
        self.Death_blocks = []
        self.game_started = False
        self.deathAnimation_isOn = False
        self.deathAnimation_steps = 0
        self.blocksSpawned = 0
        self.spawn_extraBlocks_timer = QtCore.QTimer(self)
        self.spawn_extraBlocks_timer.timeout.connect(self.spawnDeath_block)
        self.spawn_extraBlocks_extra = False
        self.spawn_extraBlocks_two = False

    def initUI(self):
        self.setWindowTitle("Game")
        self.setFixedSize(1000,700)
        

        #* World label
        self.world_image = QPixmap(world_image_path[1])
        self.world = QtWidgets.QLabel(self)
        self.world.setPixmap(self.world_image)
        self.world.setScaledContents(True)
        self.world.setGeometry(0,0, 1000,700)

        #* Floor label
        self.floor = QtWidgets.QLabel(self)
        self.floor.setGeometry(0,350,1000,200)
        self.floor.setObjectName("floor") 
        
        #* Character label
        self.character_image = QPixmap(character_image_path[1])
        self.character_deathImage = QPixmap(character_image_path[4])
        self.character = QtWidgets.QLabel(self)
        self.character.setPixmap(self.character_image)
        self.character.setScaledContents(True)
        self.character.setGeometry(300,400, 100, 100)

        #* Lose label
        self.lose_label = QLabel("Start Game", self)
        self.lose_label.setGeometry(250,100,500,200)
        self.lose_label.setObjectName("lose")

        #* Score
        self.score_label = QLabel("0", self)
        self.score_label.setGeometry(50,50,375,100)
        self.score_label.setObjectName("score")
        
        
        #* Style
        self.setStyleSheet("""
                           
        QLabel#floor {
        background-color: lightgray;
        }
        QLabel#lose {
        text-align: center;
        font-size: 250px;
        font-family: "Times New Roman";
        color: rgba(250,0,0,0.9);    
        }
        QLabel#score {
        font-size: 125px;
        font-family: "Times New Roman";
        color: gray;
        text-align: center;
        }     
                           
        """)

    def jump(self):
        parameter = self.parameter
        ac_jump =  ((parameter*25)-self.jump_steps*parameter) #*Acceleration jump
        de_jump =  ((self.jump_steps-24)*parameter) #*Deceleration jump

        #* Jump animation
        
        if self.jump_steps < 25 and self.game_started:
             #* Move up
            self.character.setGeometry(self.character.x(), self.character.y()  - ac_jump, self.character.width(), self.character.height())
            self.jump_steps += 1
            
        elif self.jump_steps < 50 and self.game_started:
            #* Move down
            self.character.setGeometry(self.character.x(), self.character.y() + de_jump, self.character.width(), self.character.height()) 
            self.jump_steps += 1
            
        else:
            self.jump_steps = 0 #* Reset
            self.jump_timer.stop()
            self.debounce_timer = QtCore.QTimer(self)
            self.debounce_timer.timeout.connect(self.setDebounce)
            self.debounce_timer.start(self.debounce_time)
    
    def keyPressEvent(self, event):
        key = event.key()  

        #* Listens to spacebar
        if key == QtCore.Qt.Key_Space and not self.deathAnimation_isOn:
            if self.jump_debounce == False and self.game_started == True:
                self.jump_timer = QtCore.QTimer(self)
                self.jump_timer.timeout.connect(self.jump)
                self.jump_timer.start(self.airTime) #* Jumping
                self.jump_debounce = True
            elif self.game_started == False:
                self.game_started = True
                self.start_game()

    def setDebounce(self):
        #* Debounce for jumps
        self.jump_debounce = False
        self.debounce_timer.stop()

    def spawnDeath_blocks(self):

        if self.blocksSpawned < 9:
            self.spawnDeath_block({1: 400})

        elif self.blocksSpawned < 19:
            set = random.randint(1,4)
            if set == 1:
                self.spawnDeath_block({1: 400})
            elif set == 2:
                self.spawnDeath_block({1: 400, 2: 290})
            elif set == 3:
                self.spawnDeath_block({1: 400})
                self.spawn_extraBlocks(1) #* Set 1 spawns 1 extra block
            else:
                self.spawnDeath_block({1: 290, 2: 180})
        else:
            set = random.randint(1,4)
            if set == 1:
                self.spawnDeath_block({1: 400, 2: 290})
            if set == 2:
                self.spawnDeath_block({1: 400, 2: 290})
                self.spawn_extraBlocks(2) #* Set 2 spawns 2 extra blocks (vertically)
            if set == 3:
                self.spawnDeath_block({1: 400, 2: 290})
                self.spawn_extraBlocks(3) #* Set 3 spawns 2 extra blocks (horizontally)
            if set == 4:
                self.spawnDeath_block({1: 290, 2: 70})
            




        self.score_label.setText((str) (self.blocksSpawned))


        if self.blocksSpawned > 19:
            self.new_world_image = QPixmap(world_image_path[3])
            self.world.setPixmap(self.new_world_image)
            self.new_character_image = QPixmap(character_image_path[3])
            self.character.setPixmap(self.new_character_image)
        elif self.blocksSpawned > 9:
            self.new_world_image = QPixmap(world_image_path[2])
            self.world.setPixmap(self.new_world_image)
            self.new_character_image = QPixmap(character_image_path[2])
            self.character.setPixmap(self.new_character_image)
    
    def spawnDeath_block(self, positions={1: 400}):
        if self.blocksSpawned > 29:
            self.changeSpawnRate(10)

        for position in positions:
            x = random.randint(1,4)
            self.Death_block_image = QPixmap(Death_block_image_path[x])
            self.Death_block = QtWidgets.QLabel(self)
            self.Death_block.setPixmap(self.Death_block_image)
            self.Death_block.setScaledContents(True)
            self.Death_block.setGeometry(1000,positions[position],115,100)
            self.Death_block.show()
            self.Death_blocks.append(self.Death_block)
            self.blocksSpawned += 1

        if self.spawn_extraBlocks_timer.isActive():
            self.spawn_extraBlocks_timer.stop()
            if self.spawn_extraBlocks_extra:
                self.spawn_extraBlocks_timer.start(110)
                self.spawn_extraBlocks_extra = False
            if self.spawn_extraBlocks_two:
                self.spawn_extraBlocks_two = False
                self.spawnDeath_block({1: 290})

    def spawn_extraBlocks(self, set):
        if set == 1:
            self.spawn_extraBlocks_timer.start(110)
        if set == 2:
            self.spawn_extraBlocks_timer.start(110)
            self.spawn_extraBlocks_extra = True
        if set == 3:
            self.spawn_extraBlocks_timer.start(110)
            self.spawn_extraBlocks_two = True
            
    def moveDeath_blocks(self):
        for block in self.Death_blocks[:]: 
            if block is not None and block.x() > 0 - block.width():
                block.setGeometry(block.x() - self.Death_block_pxPerMove, block.y(), block.width(), block.height())
            else:
                block.deleteLater()
                self.Death_blocks.remove(block)  
        self.check_collision()

    def check_collision(self):
        X_startOfCharacter = self.character.x()
        X_endOfCharacter = X_startOfCharacter + self.character.width()
        Y_startOfCharacter = self.character.y()
        Y_endOfCharacter = Y_startOfCharacter + self.character.height()

        for block in self.Death_blocks:
            X_startOfBlock = block.x()
            X_endOfBlock = X_startOfBlock + block.width()
            Y_startOfBlock = block.y()
            Y_endOfBlock = Y_startOfBlock + block.height()

            #* Check collision between character and death block
            if (X_startOfCharacter < X_endOfBlock and X_endOfCharacter > X_startOfBlock and
                Y_startOfCharacter < Y_endOfBlock and Y_endOfCharacter > Y_startOfBlock):
                self.lose()

    def lose(self):
        self.game_started = False
        self.lose_label.setText("Lost")

        #* Stop timers
        self.Death_block_spawnTimer.stop()
        self.Death_block_moveTimer.stop()

        #* Delete death blocks
        for block in self.Death_blocks:
            block.deleteLater()
        self.Death_blocks.clear()
        self.lose_label.show()

        #* Death animation
        self.character.setPixmap(self.character_deathImage)
        self.deathAnimation_timer = QtCore.QTimer(self)
        self.deathAnimation_timer.timeout.connect(self.deathAnimation)
        self.deathAnimation_timer.start(10) #* Death animation speed

    def start_game(self):
        #* Death_blocks start moving
        self.Death_block_moveTimer = QtCore.QTimer(self)
        self.Death_block_moveTimer.timeout.connect(self.moveDeath_blocks)
        self.Death_block_moveTimer.start(self.Death_block_moveSpeed) #* Death block move speed
        self.Death_block_spawnTimer = QtCore.QTimer(self)
        self.Death_block_spawnTimer.timeout.connect(self.spawnDeath_blocks)
        self.Death_block_spawnTimer.start(self.Death_block_spawnRate) #* Death block spawn rate
        self.lose_label.hide()
        self.character.setPixmap(self.character_image)
        self.character.setGeometry(300,400, 100, 100)
        self.world.setPixmap(self.world_image)

        self.blocksSpawned = 0
        self.Death_block_spawnRate = 1500
        self.score_label.setText((str) (self.blocksSpawned))

    def deathAnimation(self):
        if self.character.y() < self.height():
            self.deathAnimation_isOn = True
            if self.deathAnimation_steps > 3:
                self.character.setGeometry(self.character.x(), self.character.y() + (int) (self.deathAnimation_steps), self.character.width(), self.character.height())
            self.deathAnimation_steps += 0.5
        else:
            self.deathAnimation_timer.stop()
            self.deathAnimation_isOn = False
            self.deathAnimation_steps = 0

    def changeSpawnRate(self, spawnRate):
        self.Death_block_spawnRate -= spawnRate
        self.Death_block_spawnTimer.stop()
        self.Death_block_spawnTimer.start(self.Death_block_spawnRate)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 