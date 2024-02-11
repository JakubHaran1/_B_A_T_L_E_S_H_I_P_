import os
import random


class Player:
    row_key = [" A "," B "," C "," D "," E " ," F "," G "," H "," I "," J "]
    column_key = ["1 ","2 ","3 ","4 ","5 ","6 ","7 ","8 ","9 ","10 "]
    banned_symbols = ["<",".",">","?","/",";",":",'""',"[","{","]","}","\\","+","=","-","_",")","(","*","&","^","%","$","#","@","!","`","~","''"]
    
    def __init__(self, name):
        self.name = name
        self.ships = []
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

    def draw_ship(self,ship,board_get):
        arr =""
        for el in ship:
            key = el[:1]
            value = int(el[1:])
            arr = board_get[f" {key} "]
            arr[value-1] = "🚢 "
    



                    
            

class Ai(Player):
    def __init__(self,name):
        super().__init__(name)
    
    def create_ship(self):
        orientations = ["row","column"]
        orientation = random.choice(orientations)
        size = self.type_ship(len(self.ships))
        ship = []
        if orientation == "row":
            while len(ship) != size:
                c = True
                while c == True:
                    row = random.choice(self.row_key)
                    self.ships.append(row)
                


            

    
       
        

            


class Batleship:
    def __init__(self):
        self.players = self.create_player()
        self.pre_game()
        self.start_game()
        
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
            players.append(Player(name))
            players.append(Ai("Ai")) #zamienić kolejnościa z player
            
            
        
        return(players)


    
    # Instrukcja gry 
    def pre_game(self):
        os.system('cls')
        print("---GRA W STATKI---",end='\n\n')
        print("Zasady:")
        print("Masz do wyboru: cztery jednomasztowce, trzy dwumasztowce, dwa trzymasztowce i jeden czteromasztowiec")
        print("Musisz rozmieszczać pojedyncze statki w obrębie jednego wiersza lub kolumny tzn. nie wolno ci postawić np.dwumasztowca na [A1,B2]")
        print("Statki nie mogą się stykać")
        print("Posiadasz dwie plansze:",end='\n\n')
        print("-strzelnicza na której będziesz zaznaczać swoje strzały")
        self.players[0].print_board(self.players[0].board_shot)
        print("-celownicza na której będą zaznaczane strzały i trafienia AI")
        self.players[0].print_board(self.players[0].board_get)
        accept = input("czy akceptujesz zasady gry ? 1 - TAK; 0 - NIE: ")
        os.system("cls") 

    def exception_operator(self,player,num_err, el=0):
        if player != "Ai":
            print()
            match num_err:
                case 1: print("Uwaga! Nie podano pozycji statku!")
                case 2: print("W pozycji znajdują się niedozwolone symbole!!")
                case 3: print("Niepoprawna długość statku!!")
                case 4: print(f"Wartość {el} występuje w deklaracji statku więcej niż jeden raz")
                case 5: print(f"Niepoprawna wartość na pozycji wierszowej - {el[:1]} w {el}! Mają to być litery od A-J")
                case 6: print(f"Niepoprawna wartość na pozycji kolumnowej - {el[1:]} w {el}! Mają to być cyfry od 1-10")
                case 7: print(f"Pozycja {el} jest pozycją chronioną innego statku!")
                case 8: print(f"Na pozycji {el} jest już umiejscowiony statek!")
                case 9: print(f"Statek musi znajdywać się w pozycji poziomej lub pionowej (te same kolumny lub wiersze) !!")
                case 10: print(f"Statek nie jest umiejscowiony poziomo!!")
                case 11: print(f"Elementy składowe statku nie są koło siebie!!")
                case 12: print(f"Statek nie jest umiejscowiony pionowo!!")
                case 13: print(f"Elementy składowe statku nie są koło siebie!")
        



    def start_game(self):
        for player in self.players:
            
            while len(player.ships) != 10:
                orientation = "row"
                size = player.type_ship(len(player.ships))

                if player.name != "Ai":
                    print("To jest twoja tablica ze statkami:")
                    player.print_board(player.board_get)
                    ship = input(f"Podaj umiejscowienie statku o długości {size}: ")
                    ship = ship.upper()
                    os.system('cls')
                else:
                    pass
                
                if ship == "": 
                    self.exception_operator(player,1)
                    continue

                # Sprawdzannie czy znajdują się niedozwolone symbole
                if not any(symbol.strip() in ship for symbol in player.banned_symbols):
                    # Dzielenie statku na poszczególne "frakcje"
                    ship = ship.split(",")
                else:
                    exception_operator(player,2)
                    continue

                # Sprawdzanie długości statku
                if len(ship) != size:
                    exception_operator(player,3)
                    continue

                # Sprawdzanie czy wszystkie klucze są unikalne i nie znajduja się w safety_zone ani ships
                for el in ship:
                    if player.ships.count(el) > 1: 
                        exception_operator(player,4,el)
                        continue

                    el = el.replace(" ","")
                    if f" {el[:1]} " not in player.row_key:
                        exception_operator(player,5,el)
                        continue
                    
                    if f"{el[1:]} " not in player.column_key:
                        exception_operator(player,6,el)
                        continue

                    if el in player.protect_zone:
                        exception_operator(player,7,el)
                        continue
                    
                    for boat in player.ships: 
                        if el in boat:
                            exception_operator(player,8,el)
                            continue
                                


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
                        else: 
                            exception_operator(player,9,el)
                            continue
                        previous_el = ""
                        # Sprawdzanie czy pozycja jest utrzymywana i czy elementy składowe statku znajdują się koło siebie
                        if orientation == "row": 
                            for el in ship:
                                if el[:1] != row:
                                    exception_operator(player,10,el)
                                    continue
                
                                if previous_el == "":
                                    previous_el = ship[0][1:]
                                elif int(el[1:]) == int(previous_el) + 1:
                                    previous_el = el[1:]
                                else:
                                    exception_operator(player,11,el)
                                    continue
                                
                                
                        else:
                            for el in ship:
                                if el[1:] != column: 
                                    exception_operator(player,12,el)
                                    continue
                                
                                if previous_el == "":
                                    previous_el = player.row_key.index(f" {ship[0][:1]} ")
                                elif el[:1] == player.row_key[previous_el + 1].strip():
                                    previous_el = player.row_key.index(f" {el[:1]} ")
                                else:
                                    exception_operator(player,12,el)
                                    continue
                                    
                    
                    player.ships.append(ship)
                        
                    

                

                player.field_protector(orientation,ship)
                player.draw_ship(ship,player.board_get)
            
                    
            
            

    
batleship = Batleship()