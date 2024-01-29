import os

class App:
    def __init__(self):
        os.system("cls")
        print("WITAMY W KALKULATORZE SYSTEMÓW LICZBOWYCH",end='\n\n')
        choice_value = self.choice()
    
    def choice(self):
        print("2 - binarny, 8 - ósemkowy, 10 - dziesiętny, 2 - dwójkowy")
        value = input("W jakim systemie będzie zapisana twoja liczba: ")
        if value: return value


app = App()