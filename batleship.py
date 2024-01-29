import os

class Batleship:
    def __init__(self):
        os.system("cls")
        print("GRA W STATKI",end='\n\n')
        print("Zasady:")
        print("Masz do wyboru: cztery jednomasztowce, trzy dwumasztowce, dwa trzymasztowce i jeden czteromasztowiec")
        print("Musisz rozmieszczać pojedyncze statki w obrębie jednego wiersza lub kolumny tzn. nie wolno ci postawić np.dwumasztowca na [A1,B2]")
        print("Statki nie mogą się stykać")
        print("Posiadasz dwie plansze:",end='\n\n')
        print("-strzelnicza na której będziesz zaznaczać swoje strzały")
        board_shot = self.board_maker()
        print("-celownicza na której będziesz zaznaczać strzały i trafienia AI")
        board_get = self.board_maker()
        accept = input("czy akceptujesz zasady gry ? 1 - TAK; 0 - NIE")

        
    def board_maker(self):
        column_key = [" A "," B "," C "," D "," E " ," F "," G "," H "," I "," J "]
        row_key = [" 1"," 2"," 3"," 4"," 5"," 6"," 7"," 8"," 9"," 10"]
        row_value = []
        board = {}
        print("   ",*row_key)
        for i in range(10):
            board[column_key[i]] = ["|0|" * 10]
            print(column_key[i],*board[column_key[i]])

        print()
        return board
            
            

        init_board(column_key)

        
  


batleship = Batleship()