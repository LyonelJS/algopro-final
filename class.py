class WashingMachine:
    consumerElectronic = False
    def __init__(self,brand):
        self.brand = brand
        self.turnedOn = False
    
    def toggle(self):
        if self.turnedOn == True:
            self.turnedOn = False
            print(f'{self.brand} Washing machine is turned off')
        else: 
            print(f'{self.brand} Washing machine is turned on')
            self.turnedOn = True
    
    def setTimer(self, minutes):
        if self.turnedOn == True:
            print(f'Running {self.brand} washing machine for {minutes} minutes.')
        else:
            print(f'Turn on {self.brand} washing machine first')
    
    def __str__(self):
        return f'Brand: {self.brand}'
    def __repr__(self):
        return f'WashingMachine"(brand: {self.brand}, toggle status: {self.turnedOn})"'
    
    def __add__(self, another):
        return f'{self.brand} + {another.brand}'


washMe1 = WashingMachine("Sony")
washMe2 = WashingMachine('LG')

print(washMe2)

washMe1.toggle()
washMe1.setTimer(2)
washMe2.setTimer(4)
