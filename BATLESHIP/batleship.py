import os
import random
from player import Player
from ai import Ai

                    
            


class Batleship:
    def __init__(self):
        self.players = self.create_player()
        accept = self.pre_game()
        if accept == "1":
            self.start_game() 
            self.play_game()
        else:
            print("Jeśli nie akceptujesz warunków gry musimy się pożegnać!")
    
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
            players.append(Ai("Ai")) 
            players.append(Player(name))
            

            
        
        return(players)
    # Tworzenie graczy
    
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
        return accept



    def start_game(self):
        for player in self.players:
            if player.name != "Ai":
                while len(player.ships) != 10:
                    print(f"Uwaga! \n Uzupełnianie tablicy celowniczej statkami gracza: {player.name}")
                    orientation = "row"
                    size = player.type_ship(len(player.ships))
                    print("To jest twoja tablica ze statkami:")
                    player.print_board(player.board_get)
                    ship = input(f"Podaj umiejscowienie statku o długości {size}: ")
                    ship = ship.upper().replace(" ","")
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

                
                
    def play_game(self):
        os.system("cls")
        print("Rozpoczynamy grę! Podawaj koordynaty gdzie twoja załoga ma strzelać (np. A1)",end='\n')
        
        active_player = self.players[0]
        no_active = self.players[1]
        while self.players[0].ships != [] and self.players[1].ships != []:
            print(f"Strzały oddaje {active_player.name}")
            active_player.print_board(active_player.board_shot)
            
            get = ""
            shot = ""
            if active_player.name != "Ai":
                shot = [input("Podaj koordynaty statku przeciwnika: ").upper()]
                
            else:
                print("AI")
                # TWORZENIE STRZAŁÓW W ZALEŻNOŚCI OD ZMIENNYCH
                # 1.Losowy strzał
                # 2. Sprawdzanie kierunku 
                shot = active_player.shooting_ai()
                print(f"to jest strzał AI: {shot}")
                

            for ship in no_active.ships:
                if get != "":
                    break #aby po znalezieniu juz nie sprawdzało
                for el in ship:
                    if shot[0] == el:
                        ship.remove(el)
                        get = shot
                        ship_remove = ship
                        break
                    
                
            if get != "":
                print(f"Gratulację! Gracz {active_player.name} trafił!")
                active_player.draw_ship(shot,active_player.board_shot,1,0)
                active_player.print_board(active_player.board_shot)
                
                
                if len(ship_remove) == 0:
                    no_active.ships.remove([])
                    print("UWAGA STATEK ZATONĄŁ!")
                    # Resetowanie strategii gdy statek zatonął
                    if active_player.name == "Ai":
                        active_player.sink_ship = True
                    
                print("Przysługuje mu kolejny strzał!")
                next_step = input("Enter aby przejść dalej...")
                # Zmiana zmiennych w zależności czy traf 
                
                if active_player.name == "Ai":
                    # Dla losowych strzałów:
                    if active_player.stategy == False:
                        active_player.stategy = "I" #przechodzenie do sprawdzania kierunku
                        active_player.first_shot = shot

                        if active_player.sink_ship == True:
                            active_player.reset_strategy()
                        
                        
                        # Dla sprawdzania kierunku
                    elif active_player.stategy == "I":
                        active_player.stategy = "II" #Przechodzenie do zatapiania statku
                        #Zapisywanie właściwego kierunku
                        active_player.correct_direction = active_player.direction 
                        # Zapisywanie current shot - potrzebne do funkcji zatapiającej
                        active_player.current_shot = shot
                        print(active_player.current_shot)

                        if active_player.sink_ship == True:
                            active_player.reset_strategy()
                        # Dla zatapiania statku i poprawania zatapiania
                    elif active_player.stategy == "II":
                        active_player.current_shot = shot

                        if active_player.sink_ship == True:
                            active_player.reset_strategy()

                    elif  active_player.stategy == "III":
                        active_player.stategy = "II"
                        active_player.current_shot = shot
                        if active_player.sink_ship == True:
                            active_player.reset_strategy()

            else:
                print("Pudło!!",end='\n')
                active_player.draw_ship(shot,active_player.board_shot, 1, 1)
                active_player.print_board(active_player.board_shot)
                next_step = input("Enter aby przejść dalej...")
                print("Następuje zmiana gracza...")
                # Zmiana zmiennych w zależności  czy nie TRAF
                # Dla losowych strzałów: brak 
                # Dla sprawdzania kierunku
                if active_player.name == "Ai":
                    if active_player.stategy == "I":
                        active_player.wrong_directions.append(active_player.direction)
                    # Dla zatapiania statku
                    elif active_player.stategy == "II":
                        active_player.current_shot = active_player.first_shot
                        active_player.stategy = "III"

                [active_player, no_active] = self.switch_player(active_player)
                os.system("cls")

            
        if self.players[1].ships == []:
            os.system("cls")
            print("--------------------------- ")
            print(f"GRĘ W STATKI ZWYCIĘŻA: {self.players[0].name} ")
            print("--------------------------- ")
        else:
            os.system("cls")
            print("--------------------------- ")
            print(f"GRĘ W STATKI ZWYCIĘŻA: {self.players[1].name} ")
            print("--------------------------- ")

        
        


                
batleship = Batleship()