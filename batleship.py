import os


class Player:
    column_key = [" A "," B "," C "," D "," E " ," F "," G "," H "," I "," J "]
    row_key = [" 1"," 2"," 3"," 4"," 5"," 6"," 7"," 8"," 9"," 10"]
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
            board[self.column_key[i]] = ["|0|" * 10]
            
        return board

    # Wyświetlanie tablicy
    def print_board(self,board):
        # Wyświetlanie zmiennych kolumnowych
        print("   ",*self.row_key)
        for i in range(10): #liczba kolumn i wierszy
            print(self.column_key[i],*board[self.column_key[i]])
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
        zone = arr.strip() + el
        self.protect_zone.append(zone)

    def field_protector(self,orientation,ship):

        # Wyliczanie zabezpieczonych pól:
        if orientation == "row":
            min_value = ship[0]
            max_value = ship[0]
            index_el = ""

            # Ustalanie wartości
            for el in ship:
                first_zone = ""
                second_zone = ""
                
                #Znalezienie najmniejszej i największej wartości (w zależności od orientacji) 
                if int(min_value[1:]) > int(el[1:]): min_value = el
                else: max_value = el
            
                # Zmienna pomocnicza do wyliczenia górnego i dolnego bezpiecznego pola 
                index_el = self.column_key.index(f" {el[:1]} ")
                
                
                # Wyliczanie górnego pola
                if index_el != 0:
                    self.add_protect_field(first_zone, self.column_key[index_el - 1 ], el[1:])
                    
                # Wyliczanie dolnego pola
                if index_el != len(self.column_key) - 1:
                    self.add_protect_field(second_zone, self.column_key[index_el + 1 ], el[1:])
                    
                    
            # Wyliczanie "dodatkowych" bocznych pól
            # Pole lewe skrajne
            index_el = self.row_key.index(f" {min_value[1:]}")
            if index_el != 0:
                self.add_protect_field(min_value, min_value[:1], self.row_key[index_el - 1].strip())
                
            
            # Pole prawe skrajne
            index_el = self.row_key.index(f" {max_value[1:]}")
            if index_el != len(self.column_key) - 1:
                self.add_protect_field(max_value, max_value[:1], self.row_key[index_el + 1].strip())
                
            

    
       
        

            


class Batleship:
    def __init__(self):
        players = 0
        self.player1 = Player("Player")
        self.player2 = Player("AI")
        self.pre_game()
        self.start_game()
        
    
    # Instrukcja gry 
    def pre_game(self):
        os.system('cls')
        print("GRA W STATKI",end='\n\n')
        print("Zasady:")
        print("Masz do wyboru: cztery jednomasztowce, trzy dwumasztowce, dwa trzymasztowce i jeden czteromasztowiec")
        print("Musisz rozmieszczać pojedyncze statki w obrębie jednego wiersza lub kolumny tzn. nie wolno ci postawić np.dwumasztowca na [A1,B2]")
        print("Statki nie mogą się stykać")
        print("Posiadasz dwie plansze:",end='\n\n')
        print("-strzelnicza na której będziesz zaznaczać swoje strzały")
        self.player1.print_board(self.player1.board_shot)
        print("-celownicza na której będą zaznaczane strzały i trafienia AI")
        self.player1.print_board(self.player1.board_get)
        accept = input("czy akceptujesz zasady gry ? 1 - TAK; 0 - NIE: ")
        os.system("cls") 



    def start_game(self):
        orientation = "row"
        while len(self.player1.ships) != 10:
            size = self.player1.type_ship(len(self.player1.ships))
            print("To jest twoja tablica ze statkami:")
            self.player1.print_board(self.player1.board_get)
            ship = input(f"Podaj umiejscowienie statku o długości {size}: ")
            ship = ship.upper()
            os.system('cls')
            
            try:
                if ship == "": raise Exception("Uwaga! Nie podano pozycji statku!")

                # Sprawdzannie czy znajdują się niedozwolone symbole
                if not any(symbol.strip() in ship for symbol in self.player1.banned_symbols):
                    # Dzielenie statku na poszczególne "frakcje"
                    ship = ship.split(",")
                else:
                    raise Exception("W pozycji znajdują się niedozwolone symbole!!")

                # Sprawdzanie długości statku
                if len(ship) != size: raise Exception("Niepoprawna długość statku!!")

                # Sprawdzanie czy wszystkie klucze są unikalne i nie znajduja się w safety_zone ani ships
                
                for el in ship:
                    el = el.replace(" ","")
                    if f" {el[:1]} " not in self.player1.column_key:
                        raise Exception(f"Niepoprawna wartość na pozycji wierszowej - {el[:1]}! Mają to być litery od A-J")
                    
                    if f" {el[1:]}" not in self.player1.row_key:
                        raise Exception(f"Niepoprawna wartość na pozycji kolumnowej - {el[1:]}! Mają to być cyfry od 1-10")

                    if el in self.player1.protect_zone:
                        raise Exception(f"Pozycja {el} jest pozycją chronioną innego statku!")
                    
                    
                if  any(el in ship for arr in self.player1.ships):
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
                    else:
                        raise Exception("Statek musi znajdywać się w pozycji poziomej lub pionowej (te same kolumny lub wiersze) !!")

                    # Sprawdzanie czy pozycja jest utrzymywana
                    if orientation == "row": 
                        for el in ship:
                            if el[:1] != row: raise Exception("Statek nie jest umiejscowiony poziomo!!")
                    else:
                        for el in ship:
                            if el[1:] != column: raise Exception("Statek nie jest umiejscowiony pionowo!!")
                
                self.player1.ships.append(ship)
                

            except Exception as e:
                print(f"Uwaga! Błąd w deklaracji statku: {e}")
                continue

            

            self.player1.field_protector(orientation,ship)
            print(self.player1.protect_zone)
            print(self.player1.ships)
            
            

    
batleship = Batleship()