
import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0] # muutus asukoha suhtes
        self.collisions = {"up": False, "down": False, "right": False, "left": False} # sonastik, mis kontrollib, mis collisionid toimusid 
        #ANIMATSIOONID JUURDE
        self.action = ''
        self.anim_offset = (-3, -3) # animatsioon kui pilt on natuke suurem kui pandud suurus
        self.flip = False # pildi keeramiseks
        self.set_action('idle')
        self.last_movement = [0, 0]
        

    # world colliding RECTANGLE
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()


    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False} # iga frame see reset'itakkse

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        #COLLISION DETECTION for the X-AXIS 
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
                
        #COLLISION DETECTION for the Y-AXIS
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        #kas keerata pilti
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement #imput for the update function


        self.velocity[1] = min(5, self.velocity[1] + 0.1)
    
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset = (0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

# tegelased

class Karu(PhysicsEntity):
    def __init__(self, game, pos, size, alert_flag):
        super().__init__(game, 'karu', pos, size)
        self.alert_flag = alert_flag
        
    def update(self, tilemap, movement=(0, 0)): #TÖÖTAB!
        super().update(tilemap, movement=movement)
        if self.game.happy_karu == True:
                self.set_action('happy')
        elif self.alert(self.game.player.pos) and not self.game.talk_karu:
            self.set_action('wave')
        elif self.game.talk_karu == True:
                self.set_action('talk')   
        else:
            self.set_action('idle')


    def alert(self, player_pos):
        self.player_pos = player_pos
        if 450 < player_pos[0] < 550 and -64 < player_pos[1] < -62:
            self.alert_flag = True
        else:
            self.alert_flag = False
        return self.alert_flag
            

        

class Konn(PhysicsEntity):
    def __init__(self, game, pos, size, alert_flag_konn):
        super().__init__(game, 'konn', pos, size)
        self.alert_flag_konn = alert_flag_konn
        
    def update(self, tilemap, movement=(0, 0)): #TÖÖTAB!
        super().update(tilemap, movement=movement)
        if self.game.happy_konn == True:
                self.set_action('happy')
        elif self.alert(self.game.player.pos) and not self.game.talk_konn:
            self.set_action('wave')
        elif self.game.talk_konn == True:
                self.set_action('talk')   
        else:
            self.set_action('idle')


    def alert(self, player_pos):
        self.player_pos = player_pos
        if -460 < player_pos[0] < -395 and 160 < player_pos[1] < 170:
            self.alert_flag_konn = True
        else:
            self.alert_flag_konn = False
        return self.alert_flag_konn
    
# player
class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0 # kontrollib kaua mängija on õhus olnud
        self.jumps = 2 #mitu hüpet saab teha õhus
        self.wall_slide = False
        self.dig_time = 0
        self.digging = True

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        
        self.dig_time -= 1
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 2 #peale igat põranda puudutust saab 2x hüpata
        
            
        
        self.wall_slide = False #mida varem see seina puudutab, seda kiiremini liigub süsteem järgmise funktsiooni meetodi poole
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.8)
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')

            
        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            elif self.dig_time > 0:
                self.set_action('dig')
            else:
                self.set_action('idle')
        

        if self.velocity[0] > 0: # liigub vasakule
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:                    # liigub paremale
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3 #impulls, pressib sind paremale poole seinast eemale
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1) #et miinimum väärtus oleks null
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3
                self.velocity[1] = -2.5
                self.air_time = 4
                self.jumps = max(0, self.jumps - 1)
                return True    
        elif self.jumps: #see rikub ära võimaluse hüpata rohkem kui lubatud hüpete arv on seadistatud korraga
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
    
    def dig(self):
        self.dig_time = 150


    def talk(self, flag_karu, flag_konn, aare_1, aare_2):
        if flag_karu == True:
            if aare_1 < 1:
                return True
        elif flag_konn == True:
            if aare_2 < 1:
                return True



