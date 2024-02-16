from player import Player
import random

class Ai(Player):
    def __init__(self,name):
        super().__init__(name)
        self.stategy = False
        self.first_shot = ""
        self.current_shot = ""
        self.direction = "" #bazowa zmienna kierunku
       
        self.correct_direction = "" #poprawny kierunek
        self.sink_ship = False
        self.fired_field = [""]
        self.wrong_directions = [""] #będą tu znajdywać się niewłaściwe kierunki dla danego pierwszego strzału aby wyeliminować sprawdzanie kilku krotne
    
    def create_ship(self, orientation):
        # Dodać sprawdzanie czy nie jest już zajęte pole i czy nie znajduje się w safety field!
        size = self.type_ship(len(self.ships))
        ship = []
        first_el = ""
        c = True
        while c == True:
            # Inicjacja pierwszego elementu statku:
            row = random.choice(self.row_key).strip()
            column = random.choice(self.column_key).strip()
            if int(column) + size <= len(self.column_key):
                first_el = row + column
                c = False
                ship.append(first_el)

        if orientation == "row" and size > 1:
            #Dołączanie kolejnych elementów składowych statku:
            i = 0
            while len(ship) != size:
                i+=1
                el = row + str(int(column) + i)
                ship.append(el)

        elif orientation == "column" and size > 1:
            i = 0
            index_el = self.row_key.index(f" {row} ")

            while len(ship) != size:
                i += 1
                el = self.row_key[index_el + i].strip() + column
                ship.append(el)



        return ship
    
    def reset_strategy(self):
        self.stategy = False
        self.first_shot = ""
        self.current_shot = ""
        self.direction = "" #bazowa zmienna kierunku
        self.correct_direction = "" #poprawny kierunek
        self.sink_ship = False  
        self.wrong_directions = [""]




    def check_direction(self):
        # losuj kierunek do momentu aż nie będzie w wrong direction
        while self.direction in self.wrong_directions:
            if self.first_shot[0][:1] == "A":
                if self.first_shot[0][1:] == "1":
                    self.direction = random.choice(["bottom","right"])
                    
                elif self.first_shot[0][1:] == "10":
                    self.direction = random.choice(["bottom","left"])
                    
                else: self.direction = random.choice(["bottom","left","right"])

            elif self.first_shot[0][:1] == "J":

                    if self.first_shot[0][1:] == "1":
                        self.direction = random.choice(["top","right"])
                        
                    elif self.first_shot[0][1:] == "10":
                        self.direction = random.choice([ "top", "left"])
                        
                    
                    else: self.direction = random.choice(["top","left","right"])
            else:
                    self.direction = random.choice(["bottom","top","left","right"])

    def aiming(self,shot_type,direction):
        
        shot = ""
        if direction == "top":
            row = self.row_key.index(f" {shot_type[0][:1]} ")
            row = self.row_key[row - 1].strip()
            shot = row + shot_type[0][1:]

        elif direction == "bottom":
            row = self.row_key.index(f" {shot_type[0][:1]} ")
            row = self.row_key[row + 1].strip()
            shot = row + shot_type[0][1:]
            
        
        elif direction == "right":
            column = self.column_key.index(f"{shot_type[0][1:]} ")
            column = self.column_key[column + 1].strip()
            shot = shot_type[0][:1] + column


            

        elif direction == "left":
            column = self.column_key.index(f"{shot_type[0][1:]} ")
            column = self.column_key[column - 1].strip()
            shot = shot_type[0][:1] + column
        
        

        return shot
    
    

    def shooting_ai(self):
        shot = ""
        #strzelanie losowe
        if self.stategy == False:
            while shot in self.fired_field:
                shot = random.choice(self.row_key).strip()
                shot = shot + random.choice(self.column_key).strip()
                
                
            
        
        elif self.stategy == "I":
            # Sprawdzanie w którym kierunku strzelać
            self.check_direction()
            shot = self.aiming(self.first_shot, self.direction)
        elif self.stategy == "II":
            
            shot = self.aiming(self.current_shot,self.correct_direction)
        
        elif self.stategy == "III":
            match self.correct_direction:
                case "top":
                    self.correct_direction = "bottom"
                case "left":
                    self.correct_direction = "right"
                case "bottom":
                    self.correct_direction = "top"
                case "right":
                    self.correct_direction = "left"
            
            shot = self.aiming(self.current_shot,self.correct_direction)

        self.fired_field.append(shot)
        return [shot]
        
        

    #strzelanie 
    #losowanie czy column czy row
    # potem losowanie columny lub row 
    # gdy traf 
        # (zapamiętaj traf) 
        #  spróbuj w lewo/prawo/góra dół / gdy traf idziesz w dół...
        # gdy nie traf zacznij od prawo/góra - to co ostatnio nie było traf 
    