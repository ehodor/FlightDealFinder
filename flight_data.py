class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, fromair, toair, fromcity,tocity,depart,arrive,price):
        self.from_airport = fromair
        self.to_airport = toair
        self.from_city = fromcity
        self.to_city = tocity
        self.depart = depart
        self.arrive = arrive
        self.price = price
