if  any(el in ship for arr in self.player1.ships):
                    raise Exception(f"Na pozycji {el} jest już umiejscowiony statek!")

                if el in self.player1.protect_zone:
                    raise Exception(f"Pozycja {el} jest pozycją chronioną innego statku!")