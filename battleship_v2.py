import os


class Player:
    column_key = [" A "," B "," C "," D "," E " ," F "," G "," H "," I "," J "]
    row_key = [" 1"," 2"," 3"," 4"," 5"," 6"," 7"," 8"," 9"," 10"]
    
    def __init__(self,name):
        self.name = name
        self.board_shot = self.board_maker()
        self.board_get = self.board_maker()

    # Inicjacja tablicy
    def board_maker(self):
        row_value = []
        board = {}
        
        for i in range(10):
            board[self.column_key[i]] = ["|0|" * 10]
            
        return board

    # Wyświetlanie tablicy
    def print_board(self,board):
        # Wyświetlanie zmiennych kolumnowych
        print("   ",*self.row_key)
        for i in range(10):
            print(self.column_key[i],*board[self.column_key[i]])
        print()
            
class Ai(Player):
    pass

class Batleship:
    def __init__(self):
        self.ai = Ai("ai")
        self.ai.print_board(self.ai.board_get)
        print("---- GRA W STATKI ----",end='\n\n')
        players = input("Czy chcesz grać z komputerem? 1 - tak; 0 - nie: ")
        self.player1 = ""
        self.player2 = ""
        if players == 1:
            name1 = input("Podaj imię gracza 1: ")
            name2 = input("Podaj imię gracza 2: ")
            self.player1 = Player(f"{name1}")
            self.player2 = Player(f"{name2}")
        else:
            self.player1 = Player("Player")
            self.player2 = Player("AI")
        
        # self.pre_game()
        
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
        accept = input("czy akceptujesz zasady gry ? 1 - TAK; 0 - NIE")

        if accept == "1":
            accept = 1
            return accept 
        else:
            accept = 0
            return accept
    
    def start_game():
        pass




        
   
        
            
            

        

        
  


batleship = Batleship()