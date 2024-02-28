import pandas


df = pandas.read_csv("hotels.csv", dtype={"id": str})
df_card = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_security = pandas.read_csv("card_security.csv", dtype=str)


class User:
    pass


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
        self.city = df.loc[df["id"] == self.hotel_id, "city"].squeeze()

    def book(self):
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        is_free = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if is_free == "yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel_object = hotel_object

    def generate(self):
        content = f"""
        Thank you for reservation!
        This is your booking data:
        
        Name of the customer {self.customer_name}. 
        Hotel: {self.hotel_object.name}
        City: {self.hotel_object.city}
        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration, "holder": holder, "cvc": cvc}

        if card_data in df_card:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_security.loc[df_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False

print(df)

try:
    hotel_id = input("Please enter hotel id: ")
    hotel = Hotel(hotel_id)

    if hotel.available():
        credit_card = SecureCreditCard(number="1234567890123456")
        if credit_card.validate(expiration="12/23", holder="JOHN DOE", cvc="222"):
            user_pass = input("Enter your password (mypass is correct): ")
            if credit_card.authenticate(user_pass):
                hotel.book()
                name = input("Enter your name: ")
                reservation_ticket = ReservationTicket(name, hotel)
                print(reservation_ticket.generate())
            else:
                print("Password is not correct")
        else:
            print("There is problem with your card info")
    else:
        print("Hotel not available")
except ValueError:
    print("Id not exist")


