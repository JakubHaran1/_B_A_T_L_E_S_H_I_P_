import os
import random
import time


class Player:
    row_key = [" A "," B "," C "," D "," E " ," F "," G "," H "," I "," J "]
    column_key = ["1 ","2 ","3 ","4 ","5 ","6 ","7 ","8 ","9 ","10 "]
    banned_symbols = ["<",".",">","?","/",";",":",'""',"[","{","]","}","\\","+","=","-","_",")","(","*","&","^","%","$","#","@","!","`","~","''"]
    
    def __init__(self, name):
        self.name = name
        self.ships = [['A1',"A2","A3"], ['I10'], ['J9'], ['F9'], ['A8', 'B8'], ['B2', 'B3'], ['C1', 'D1'], ['I7', 'J7', 'J7'], ['I4', 'J4', 'J4'], ['D4', 'D5', 'D6', 'D7']] #wyczyścić 
        self.board_shot = self.board_maker()
        self.board_get = self.board_maker()
        self.protect_zone = []

    # Inicjacja tablicy
    def board_maker(self):
        row_value = []
        board = {}
        
        # Wypełnianie tablicy
        for i in range(10): #liczba kolumn i wierszy
            board[self.row_key[i]] = ["|0|"] * 10
            
        return board

    # Wyświetlanie tablicy
    def print_board(self,board):
        # Wyświetlanie zmiennych kolumnowych
        print("   ",*self.column_key)
        for row in self.row_key: 
            print(row, end="")
            for el in board[row]:
                print(el,end="")
            print()
            
        print()
    
    #funkcja określająca typ statku na podstawie aktualnej długości głównej tablicy statkowej
    def type_ship(self,length_ship):
        category = 0

        if length_ship < 4:
            category = 1
        elif length_ship < 7:
            category = 2
        elif length_ship < 9:
            category = 3
        elif length_ship == 9:
            category = 4
        
        return category

    def add_protect_field(self,zone,arr,el):
        zone = arr.strip() + el.strip()
        self.protect_zone.append(zone)

    def field_protector(self,orientation,ship):
        min_value = ship[0]
        max_value = ship[0]
        index_el = ""
        first_zone = ""
        second_zone = ""

        # Wyliczanie zabezpieczonych pól:
        if orientation == "row":

            # Ustalanie wartości
            for el in ship:
                #Znalezienie najmniejszej i największej wartości (w zależności od orientacji) 
                if int(min_value[1:]) > int(el[1:]): min_value = el
                else: max_value = el
            
                # Zmienna pomocnicza do wyliczenia górnego i dolnego bezpiecznego pola 
                index_el = self.row_key.index(f" {el[:1]} ")
                
                # Wyliczanie górnego pola
                if index_el != 0:
                    self.add_protect_field(first_zone, self.row_key[index_el - 1 ], el[1:])
                    
                # Wyliczanie dolnego pola
                if index_el != len(self.row_key) - 1:
                    self.add_protect_field(second_zone, self.row_key[index_el + 1 ], el[1:])
                    
                    
            # Wyliczanie "dodatkowych" bocznych pól
            # Pole lewe skrajne
            index_el = self.column_key.index(f"{min_value[1:]} ")
            if index_el != 0:
                self.add_protect_field(min_value, min_value[:1], self.column_key[index_el - 1].strip())
                
            
            # Pole prawe skrajne
            index_el = self.column_key.index(f"{max_value[1:]} ")
            if index_el != len(self.column_key) - 1:
                self.add_protect_field(max_value, max_value[:1], self.column_key[index_el + 1].strip())
        else:  
            for el in ship:
                
                #Znalezienie najmniejszej i największej wartości (w zależności od orientacji)
                if min_value[:1] > el[:1]: min_value = el
                else: max_value = el

                # Zmienna pomocnicza do wyliczenia lewego i prawego bezpiecznego pola 
                index_el = self.column_key.index(f"{el[1:]} ")
                
                # wyliczenie lewego zabezpieczonego pola
                if index_el != 0:
                    self.add_protect_field(first_zone ,el[:1], self.column_key[index_el - 1 ] )
                
                # Wyliczanie prawego zabezpieczonego pola
                if index_el != len(self.column_key) - 1:
                    self.add_protect_field(second_zone, el[:1], self.column_key[index_el + 1 ])

            # Wyliczanie "dodatkowego" górnego i dolnego pola
            # Pole górne
            index_el = self.row_key.index(f" {min_value[:1]} ")
            if index_el != 0:
                self.add_protect_field(min_value, self.row_key[index_el - 1].strip(), min_value[1:])

            # Pole dolne 
            index_el = self.row_key.index(f" {max_value[:1]} ")
            if index_el != len(self.row_key) - 1:
                self.add_protect_field(max_value, self.row_key[index_el + 1].strip(), max_value[1:])

    def draw_ship(self,ship,board,shot,miss):
        arr =""
        for el in ship:
            # dodać try aby nie wywalało errora jak w złej kolejności
            key = el[:1]
            value = int(el[1:])
            arr = board[f" {key} "]
            if shot == 0: arr[value-1] = "🚢 "
            elif shot ==1 and miss == 0: arr[value-1] = "🔥 "
            elif shot == 1 and miss == 1: arr[value-1] = "🚩 "
    
    def check_shot(self,shot, ships):
        for ship in ships:
            for el in ship:
                if shot == el:
                    get = el
                    ship.remove(el)
                    ship_remove = ship
                    return [get,ship_remove]
        ship_remove = False
        get = ""
        
        return [get,ship_remove ]



                    
            

class Ai(Player):
    directions = ["top","left","right","bottom"]
    def __init__(self,name):
        super().__init__(name)
        self.strategy = False
        self.first_shot = ""
        self.correct_shot = ""
        self.direction = ""
        self.correct_direction = ""
        self.error = 0
        
    
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
                el = self.row_key[index_el + 1].strip() + column
                ship.append(el)



        return ship
    
    def shot_direction(self):

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
                    self.direction = random.choice(["top","left"])
                
                else: self.direction = random.choice(["top","left","right"])
        else:
                self.direction = random.choice(["bottom","top","left","right"])


    def aiming(self, shot_type, direction):
        if direction == "top":
            row = self.row_key.index(f" {shot_type[0][:1]} ")
            row = self.row_key[row - 1].strip()
            shot = row + shot_type[0][1:]

        elif direction == "bottom":
            row = self.row_key.index(f" {shot_type[0][:1]} ")
            row = self.row_key[row + 1].strip()
            shot = row + shot_type[0][1:]
            print(shot)#do wywalenia

        elif direction == "right":
            column = self.column_key.index(f"{shot_type[0][1:]} ")
            column = self.column_key[column + 1].strip()
            shot = shot_type[0][:1] + column
            print(shot) #do wywalenia
        else:
            column = self.column_key.index(f"{shot_type[0][1:]} ")
            column = self.column_key[column - 1].strip()
            shot = shot_type[0][:1] + column
        
        return shot


    def shooting_ai(self):
        if self.strategy == False:
            shot = random.choice(self.row_key).strip()
            shot = shot + random.choice(self.column_key).strip()
            shot = "A2" #USUNĄĆ 
            

        elif self.strategy == "I":
            self.shot_direction()

            shot = self.aiming(self.first_shot,self.direction)
        
        elif self.strategy == "II":
            shot = self.aiming(self.correct_shot,self.correct_direction)
        
        else:
            
            if self.direction == "top":
                shot = self.aiming(self.first_shot,"bottom")
            elif self.direction == "right":
                shot = self.aiming(self.first_shot,"left")
            elif self.direction == "left":
                shot = self.aiming(self.first_shot,"right")
            else:
                 shot = self.aiming(self.first_shot,"top")


        return [shot]   


    
    
                


            

    
       
        

            


class Batleship:
    def __init__(self):
        self.players = self.create_player()
        self.pre_game()
        self.start_game() 
        self.play_game()
        
    # Tworzenie graczy
    def create_player(self):
        print("---GRA W STATKI---")
        players = input("Wybierz typ gry:\n 1 - gra z drugim graczem,\n 0 lub dowolny inny symbol - gra z komputerem \n\nTwój wybór:")
        if players == "1":
            players = []
            for i in range(2):
                name = input(f"Podaj imię gracza nr. {i+1}: ")
                players.append(Player(name))
        else:
            players = []
            name = input(f"Podaj imię gracza nr. 1: ")
            players.append(Ai("Ai")) #zamienić kolejnościa z player
            players.append(Player(name))
            

            
        
        return(players)

    # Zmiana graczy 
    def switch_player(self, current):
        if current == self.players[0]:
            active = self.players[1]
            no_active = self.players[0]
            return [active,no_active]
        else:
            active = self.players[0]
            no_active = self.players[1]
            return [active, no_active]
        
    
    # Instrukcja gry 
    def pre_game(self):
        os.system('cls')
        print("---GRA W STATKI---",end='\n\n')
        print("Zasady:")
        print("Masz do wyboru: cztery jednomasztowce, trzy dwumasztowce, dwa trzymasztowce i jeden czteromasztowiec")
        print("Musisz rozmieszczać pojedyncze statki w obrębie jednego wiersza lub kolumny tzn. nie wolno ci postawić np.dwumasztowca na [A1,B2]")
        print("Statki nie mogą się stykać")
        print("Posiadasz dwie plansze:",end='\n\n')
        print("-strzelnicza na której będziesz zaznaczać swoje strzały") #board_shot
        self.players[0].print_board(self.players[0].board_shot)
        print("-celownicza na której będą zaznaczane twoje statki oraz strzały i trafienia drugiego gracza/Ai") #board_get
        self.players[0].print_board(self.players[0].board_get)
        accept = input("czy akceptujesz zasady gry ? 1 - TAK; 0 - NIE: ")
        os.system("cls") 



    def start_game(self):
        for player in self.players:
            if player.name != "Ai":
                while len(player.ships) != 10:
                    print(f"Uwaga! Uzupełnianie tablicy celowniczej statkami gracza:{player.name}")
                    orientation = "row"
                    size = player.type_ship(len(player.ships))
                    print("To jest twoja tablica ze statkami:")
                    player.print_board(player.board_get)
                    ship = input(f"Podaj umiejscowienie statku o długości {size}: ")
                    ship = ship.upper()
                    os.system('cls')
                    
                    try:
                        if ship == "": raise Exception("Uwaga! Nie podano pozycji statku!")

                        # Sprawdzannie czy znajdują się niedozwolone symbole
                        if not any(symbol.strip() in ship for symbol in player.banned_symbols):
                            # Dzielenie statku na poszczególne "frakcje"
                            ship = ship.split(",")
                        else:
                            raise Exception("W pozycji znajdują się niedozwolone symbole!!")

                        # Sprawdzanie długości statku
                        if len(ship) != size: raise Exception("Niepoprawna długość statku!!")

                        # Sprawdzanie czy wszystkie klucze są unikalne i nie znajduja się w safety_zone ani ships
                        for el in ship:
                            if player.ships.count(el) > 1: raise Exception(f"Wartość {el} występuje w deklaracji statku więcej niż jeden raz")

                            el = el.replace(" ","")
                            if f" {el[:1]} " not in player.row_key:
                                raise Exception(f"Niepoprawna wartość na pozycji wierszowej - {el[:1]} w {el}! Mają to być litery od A-J")
                            
                            if f"{el[1:]} " not in player.column_key:
                                raise Exception(f"Niepoprawna wartość na pozycji kolumnowej - {el[1:]} w {el}! Mają to być cyfry od 1-10")

                            if el in player.protect_zone:
                                raise Exception(f"Pozycja {el} jest pozycją chronioną innego statku!")
                            
                            for boat in player.ships: 
                                if el in boat:
                                    raise Exception(f"Na pozycji {el} jest już umiejscowiony statek!")


                        # Ustalenie pozycji statku
                        if len(ship) > 1:
                            # Przypisywanie wiersza do zmiennej pomocniczej - row
                            row = ship[0][:1] # Litera pierwszej części statku 
                            
                            # Przypisywanie kolumny do zmiennej pomocniczej - column
                            column = ship[0][1:] # Cyfra pierwszej części statku
                            
                            # Sprawdzanie w jakiej orientacji jest statek - na bazie drugiej części statku
                            if ship[1][:1] == row:
                                orientation = "row"
                            elif ship[1][1:] == column:
                                orientation = "column"
                            else: raise Exception("Statek musi znajdywać się w pozycji poziomej lub pionowej (te same kolumny lub wiersze) !!")
                            previous_el = ""
                            # Sprawdzanie czy pozycja jest utrzymywana i czy elementy składowe statku znajdują się koło siebie
                            if orientation == "row": 
                                for el in ship:
                                    if el[:1] != row: raise Exception("Statek nie jest umiejscowiony poziomo!!")
                                    if previous_el == "":
                                        previous_el = ship[0][1:]
                                    elif int(el[1:]) == int(previous_el) + 1:
                                        previous_el = el[1:]
                                    else:
                                        raise Exception("Elementy składowe statku nie są koło siebie!")
                                    
                                    
                            else:
                                for el in ship:
                                    if el[1:] != column: raise Exception("Statek nie jest umiejscowiony pionowo!!")
                                    
                                    if previous_el == "":
                                        previous_el = player.row_key.index(f" {ship[0][:1]} ")
                                    elif el[:1] == player.row_key[previous_el + 1].strip():
                                        previous_el = player.row_key.index(f" {el[:1]} ")
                                    else:
                                        raise Exception("Elementy składowe statku nie są koło siebie!")
                        
                        player.ships.append(ship)
                        
                    except Exception as e:
                        print(f"Uwaga! Błąd w deklaracji statku: {e}")
                        continue

                    player.field_protector(orientation,ship)
                    player.draw_ship(ship,player.board_get,0,0)
            
                    
            else:
                while len(player.ships) != 10:
                    try:
                        orientations = ["row","column"]
                        orientation = random.choice(orientations)
                        ship = player.create_ship(orientation)
                        # Tutaj to sprawdzanie
                        for el in ship:
                            if el in player.protect_zone:
                                raise Exception
                            
                            for boat in player.ships: 
                                if el in boat:
                                    raise Exception

                        player.ships.append(ship)
                        player.field_protector(orientation, ship)
                        
                    except Exception:
                        continue

                print(f" player ships {player.ships}") #do wywalnia
                print(f' protect_ship {player.protect_zone}') #do wywalnia
                
    def play_game(self):
        os.system("cls")
        print("Rozpoczynamy grę! Podawaj koordynaty gdzie twoja załoga ma strzelać (np. A1)",end='\n')
        
        active_player = self.players[0]
        no_active = self.players[1]
        
        while self.players[0].ships != [] or self.players[1].ships != []:
            shot = ""
            print(f"Strzały oddaje {active_player.name}")
            if active_player.name != "Ai":
                active_player.print_board(active_player.board_shot)
                shot = [input("Podaj koordynaty statku przeciwnika: ").upper()]
            else:
                print("AI")
                shot = active_player.shooting_ai()
                print(f"To strzał AI: {shot}!")
                
            
            
            
            
            [get,ship_remove]  = active_player.check_shot(shot[0], no_active.ships) #zmienić na shot[0]
            
                        
            if get != "":
                print(no_active.ships)
                print(f"Gratulację! Gracz {active_player.name} trafił!")
                active_player.draw_ship(shot,active_player.board_shot,1,0)
            
                if len(ship_remove) == 0:
                    no_active.ships.remove([])
                    print("UWAGA STATEK ZATONĄŁ!")
                    if active_player.name == "Ai":
                        active_player.strategy = False
                    
                print("Przysługuje mu kolejny strzał!")

                if active_player.name == "Ai":
                    if active_player.strategy == False: 
                        active_player.first_shot = shot
                        active_player.strategy = "I"

                    elif active_player.strategy == "I":
                        active_player.correct_shot = shot
                        active_player.correct_direction = active_player.direction
                        active_player.strategy = "II"
                        
                    
            else:
                print("Pudło!!",end='\n')
                active_player.draw_ship(shot,active_player.board_get, 1, 1)
                active_player.print_board(active_player.board_get)
                
                print("Następuje zmiana gracza...")
                
                if active_player.name == "Ai":   
                    active_player.error += 1 
                    if active_player.error == 3:
                        active_player.strategy = False
                        active_player.error = 0
                    if  active_player.strategy == "II":
                        active_player.strategy = "III"
                        

                    
                [active_player, no_active] = self.switch_player(active_player)
                    

                
            
            


                
batleship = Batleship()