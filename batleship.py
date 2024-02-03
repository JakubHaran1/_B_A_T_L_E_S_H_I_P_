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
            orientation = ""
            row = ship[0][:1]
            column = ship[0][1:]
            orientation_error = "Statek musi znajdywać się w pozycji poziomej lub pionowej (te same kolumny lub wiersze) !!"
            try:
                
                if not any(symbol in ship for symbol in self.banned_symbols):
                    ship = ship.split(",")
                    
                else:
                    raise Exception("W pozycji znajdują się niedozwolone symbole!!")

                if len(ship) != size:raise Exception("Niepoprawna długość statku!!")
                
                if len(ship) > 1:
                    if ship[0][:1] == row:
                        orientation = "row"
                    elif ship[0][1:] == column:
                        orientation = "column"
                    else:
                        raise Exception(orientation_error)

                    if orientation == "row": 
                        for el in ship:
                            if el[:1] != row: raise Exception(orientation_error)
                    else:
                        for el in ship:
                            if el[1:] != column: raise Exception(orientation_error)
                        
                

                print()

                # for el in ship:
                #     let = el[:1] 
                #     num = el[1:]
                #     print(let,num,el)
                
            #co trzeba sprawdzić ?
            # 1. czy dana pozycja nie jest już zajęta - ships arr i czy nie znajduje sie w safety_ area - wartośći obliczane w punkcie 3 
            # 2. Czy został spełniony warunek 1 kolumny i 1 wierszego // to mam
            #       2.1 W pętli sprawdzić czy wszystkie pierwsze wartości są takie same czy drugie // to mam
            #       2.2 Określić kiernek ułożenia statku  // to mam
            # 3. Sprawdzić czy określone wartości są wolne i dodajemy je do zmiennej safety_area - są tam dodawane 
                #  jeśli jest to wartość początkowa statku - wartość z najmniejszą zmienną bazowa to musi być wolna   
          
                    
               
            

            except Exception as e:
                print(f"Uwaga! Błąd w deklaracji statku: {e}")
                return False
            
            

        if player == "Player":
            while len(self.ships) != 10:
                size = type_ship(self,len(self.ships))
                ship = input(f"Podaj umiejscowienie statku o długości {size}: ")
                
                ship = check_value(self,size,ship)

                


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
        os.system("cls")
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

        if accept == "1":
            accept = 1
            return accept 
        else:
            return 

    def start_game(self):
        self.player1.full_board(self.player1.board_shot,self.player1.board_get)

    


        
   
        
            
            

        

        
  


batleship = Batleship()