import os


class Player:
    column_key = [" A "," B "," C "," D "," E " ," F "," G "," H "," I "," J "]
    row_key = [" 1"," 2"," 3"," 4"," 5"," 6"," 7"," 8"," 9"," 10"]
    banned_symbols = ["<",".",">","?","/",";",":",'""',"[","{","]","}","\\","+","=","-","_",")","(","*","&","^","%","$","#","@","!","`","~"]
    
    def __init__(self, name):
        self.name = name
        self.ships = []
        self.board_shot = self.board_maker()
        self.board_get = self.board_maker()
        self.safe_zone = []

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
    
    def full_board(self,board_shot,board_get):
        player = self.name
        
        


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

        def check_value(self,size,ship):
            ship = ship.upper()
            orientation = "row"
            

            try:
                
                # Sprawdzannie czy znajdują się niedozwolone symbole
                if not any(symbol.strip() in ship for symbol in self.banned_symbols):
                    # Dzielenie statku na poszczególne "frakcje"
                    ship = ship.split(",")
                    
                else:
                    raise Exception("W pozycji znajdują się niedozwolone symbole!!")

                # Sprawdzanie czy wszystkie klucze są unikalne i nie znajduja się w safety_zone ani ships


                # Sprawdzanie długości statku
                if len(ship) != size:raise Exception("Niepoprawna długość statku!!")
                
                
                if len(ship) > 1:
                    # Przypisywanie wiersza do zmiennej pomocniczej - row
                    row = ship[0][:1] # Litera pierwszej części statku 
                    
                    # Przypisywanie kolumny do zmiennej pomocniczej - column
                    column = ship[0][1] # Cyfra pierwszej części statku
                    
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
                
               

                    
                self.ships.append(ship)
                
                
            
                

                

               
                
            #co trzeba sprawdzić ?
            # 1. czy dana pozycja nie jest już zajęta - ships arr i czy nie znajduje sie w safety_ area - wartośći obliczane w punkcie 3 
            # 2. Czy został spełniony warunek 1 kolumny i 1 wierszego // to mam
            #       2.1 W pętli sprawdzić czy wszystkie pierwsze wartości są takie same czy drugie // to mam
            #       2.2 Określić kiernek ułożenia statku  // to mam
            # 3. Obliczamy zabezpieczone wartości dla statku 
                #  jeśli jest to wartość początkowa statku - wartość z najmniejszą zmienną bazowa to musi być wolna   
          
                    
               
            

            except Exception as e:
                print(f"Uwaga! Błąd w deklaracji statku: {e}")
                return False
            
            

            # Wyliczanie zabezpieczonych pól:
            
            if orientation == "row":
                min_value = ship[0]
                max_value = ship[0]
                index_el = ""

                def add_safe_field(zone,arr,el):
                    
                    zone = arr.strip() + el
                    self.safe_zone.append(zone)
                
                # Ustalanie wartości
                for el in ship:
                    first_zone = ""
                    second_zone = ""
                    
                    #Znalezienie najmniejszej i największej wartości (w zależności od orientacji) 
                    if int(min_value[1:]) > int(el[1:]): min_value = el
                    else: max_value = el
                
                    # Zmienna pomocnicza do wyliczenia górnego i dolnego bezpiecznego pola 
                    index_el = self.column_key.index(f" {el[0]} ")
                    
                    
                    # Wyliczanie górnego pola
                    if index_el != 0:
                        add_safe_field(first_zone, self.column_key[index_el - 1 ], el[1])
                        
                    # Wyliczanie dolnego pola
                    if index_el != len(self.column_key) - 1:
                        add_safe_field(second_zone, self.column_key[index_el + 1 ], el[1])
                        
                        
                # Wyliczanie "dodatkowych" bocznych pól
                # Pole lewe skrajne
                index_el = self.row_key.index(f" {min_value[1]}")
                if index_el != 0:
                    add_safe_field(min_value, min_value[0], self.row_key[index_el - 1].strip())
                    
                
                # Pole prawe skrajne
                index_el = self.row_key.index(f" {max_value[1]}")
                if index_el != len(self.column_key) - 1:
                    add_safe_field(max_value, max_value[0], self.row_key[index_el + 1].strip())
                   
                print(self.safe_zone)

                
                



                
                
                    
                
            

        if player == "Player":
            os.system("cls")#nie rozumiem czemu musze jeszcze czyścić tu skoro daje to tu -> odnośnik do [2]
            while len(self.ships) != 10:
                
                size = type_ship(self,len(self.ships))
                
                print("To jest twoja tablica ze statkami:")
                self.print_board(self.board_get)
                ship = input(f"Podaj umiejscowienie statku o długości {size}: ")
                os.system('cls')
                if ship: ship = check_value(self,size,ship)
                else: print("Uwaga! Nie podano pozycji statku!")

                
                


        #20 pól w sumie zajętych 4x1, 3x2,2x3,1x4
        
        # 1. while az ships != 10 i w zaleznosci od aktualnej długosci pętli taki typ statku rozmieszczamy:
        #         2. while az ships != aktualny typ statku 
        #             2.1 Pytamy o umiejscowienie, przypominamy o zasadach - te same wiersze lub kolumny albo nie moga się stykać
        #             2.2 Wyswietlamy tablice get 
        #             2.2 sprawdzamy czy okej 
        #     3. Dodajemy do ships
        

            


class Batleship:
    def __init__(self):
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
        os.system("cls") # -> [2] gdy daje tylko tu to czasem pokazuje się print ,,Musisz rozmieszczać pojedyncze..." więc bez sensu bo nawet nie jest to ostatni print tylko w środku
        if accept == "1":
            
            accept = 1
            return accept 
        else:
            return 

    def start_game(self):
        self.player1.full_board(self.player1.board_shot,self.player1.board_get)

    
batleship = Batleship()