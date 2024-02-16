

class Player:
    row_key = [" A "," B "," C "," D "," E " ," F "," G "," H "," I "," J "]
    column_key = ["1 ","2 ","3 ","4 ","5 ","6 ","7 ","8 ","9 ","10 "]
    banned_symbols = ["<",".",">","?","/",";",":",'""',"[","{","]","}","\\","+","=","-","_",")","(","*","&","^","%","$","#","@","!","`","~","''"]
    
    def __init__(self, name):
        self.name = name
       
        self.ships = [] #wyczyścić 
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
            index_el = self.column_key.index(f"{min_value[1:].strip()} ")
            if index_el != 0:
                self.add_protect_field(min_value, min_value[:1], self.column_key[index_el - 1].strip())
                
            
            # Pole prawe skrajne
            index_el = self.column_key.index(f"{max_value[1:].strip()} ")
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
        try:
            arr =""
            for el in ship:
                # dodać try aby nie wywalało errora jak w złej kolejności
                key = el[:1]
                value = int(el[1:])
                arr = board[f" {key} "]
                if shot == 0: arr[value-1] = "🚢 "
                elif shot ==1 and miss == 0: arr[value-1] = "🔥 "
                elif shot == 1 and miss == 1: arr[value-1] = "🚩 "
        except:
            print("Nie właściwy strzał - nie można nanieść strzału na plansze...")
    
    def check_shot(self,shot):
        for ship in self.ships:
            for el in ship:
                if shot == el:
                    get = shot
                    ship_remove = ship
                    return [get,ship_remove]
               
        get = ""
        ship_remove = "False"
        return [get, ship_remove ]

