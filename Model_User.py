# Student Name: Carol song
# Student ID: 1154836

from Model_Cinema import *
import re

class Guest():
    def __init__(self):
        self.__isRegistered = False

    @property
    def isRegistered(self):
        return self.__isRegistered
    
    @isRegistered.setter
    def isRegistered(self, value):
        self.__isRegistered = value
    
    def register(self):
        self.isRegistered = True

class Person(ABC):
    def __init__(self, name: str, address: str, email: str, phone: str):
        self._name = name
        self._address = address
        self._email = email
        self._phone = phone
        super().__init__()

    @property
    def pName(self) -> str:
        return self._name

    @property
    def pAddress(self) -> str:
        return self._address

    @property
    def pEmail(self) -> str:
        return self._email
    
    @property
    def pPhone(self) -> str:
        return self._phone
    

class User(Person, ABC):
    def __init__(self, username: str, password: str, name: str, address: str, email: str, phone: str):
        self._username = username
        self._password = password
        self._login_status = False
        super().__init__(name, address, email, phone)
    
    @property
    def role(self) -> str:
        return 'user'
    
    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, new_username: str):
        self._username = new_username

    @property
    def password(self) -> str:
        return self._password
    
    @password.setter
    def password(self, new_password: str):
        self._password = new_password
    
    @property
    def login_status(self) -> bool:
        return self._login_status

    def login(self, password_attempt: str) -> bool:
        if self._password == password_attempt:
            self._login_status = True
            return True
        return False
        
    def logout(self) -> bool:
        if self._login_status:
            self._login_status = False
            return True
        return False

    def resetPassword(self, new_password: str) -> bool:
        if self._login_status:
            self._password = new_password
            return True
        return False

class Admin(User):
    def __init__(self, username: str, password: str, name: str, address: str, email: str, phone: str):
        super().__init__(username, password, name, address, email, phone)
    
    @property
    def role(self) -> str:
        return 'admin'
    
    def addMovie(self, cinema, movie: Movie) -> bool:
        try:
            cinema.add_newmovie(movie)
            return True
        except Exception as e:
            print(f"Error adding movie: {e}")
            return False

    def addScreening(self, screening: Screening) -> bool:
        try:
            movie = screening.movie
            movie.add_screening(screening)
            hall = screening.hall
            hall.addScreening(screening)
            return True
        except Exception as e:
            print(f"Error adding screening: {e}")
            return False

    def cancelMovie(self, cinema, movie: Movie) -> bool:
        try:
            cinema.cancel_movie(movie)
            return True
        except Exception as e:
            print(f"Error canceling movie: {e}")
            return False

    def cancelScreening(self, screening: Screening) -> bool:
        try:
            movie = screening.movie
            movie.cancel_screening(screening)
            hall = screening.hall
            hall.cancelScreening(screening)
            return True
        except Exception as e:
            print(f"Error canceling screening: {e}")
            return False

class FrontDeskStaff(User):
    def __init__(self, username: str, password: str, name: str, address: str, email: str, phone: str):
        super().__init__(username, password, name, address, email, phone)
    
    @property
    def role(self) -> str:
        return 'staff'
    
    def makeBooking(self, cinema, customer, screening, seats, amount, payment):
        created_time = datetime.now()
        status = 1
        booking = Booking(customer, created_time, screening, seats, amount, payment, status)
        try:
            customer.makeBooking(booking)
            cinema.add_booking(booking)
            content = f"You have made a booking for Movie {screening.movie.title} on {screening.screeningDate} from {screening.startTime} to {screening.endTime} with the following seats: {seats}"
            notification = Notification(created_time, content)
            customer.notificationList.append(notification)

            # Change seat status
            seats_list = seats.split(",")
            seat_numbers = [int(''.join(filter(str.isdigit, seat))) for seat in seats_list]
            for seat_num in seat_numbers:
                for seat in screening.hall.listOfSeats:
                    if seat.seatNumber == seat_num:
                        seat.isReserved = True
                        break
            return True
        except Exception as e:
            print(f"Error making booking: {e}")
            return False

    def cancelBooking(self, cinema, customer, booking):
        try:
            cinema.cancel_booking(booking)
            customer.cancelBooking(booking)
            return True
        except Exception as e:
            print(f"Error canceling booking: {e}")
            return False

class Customer(User):
    def __init__(self, username: str, password: str, name: str, address: str, email: str, phone: str):
        self.__bookingList: List[Booking] = []
        self.__notificationList: List[Notification] = []
        super().__init__(username, password, name, address, email, phone)
    
    @property
    def role(self) -> str:
        return 'customer'
    
    def makeBooking(self, booking: 'Booking') -> bool:
        if booking not in self.__bookingList:
            self.__bookingList.append(booking)
            return True
        return False

    def findBooking(self, booking_id):
        for booking in self.bookingList:
            if booking.bookingID == booking_id:
                return booking
            
    def cancelBooking(self, booking: 'Booking') -> bool:
        if booking in self.__bookingList:
            self.__bookingList.remove(booking)
            return True
        return False
    
    @property
    def bookingList(self) -> List['Booking']:
        return self.__bookingList
    
    @property
    def notificationList(self) -> List['Notification']:
        return self.__notificationList
    
    @bookingList.setter
    def bookingList(self, booking: 'Booking'):
        if booking not in self.__bookingList:
            self.__bookingList.append(booking)
    
    @notificationList.setter
    def notificationList(self, notification: 'Notification'):
        if notification not in self.__notificationList:
            self.__notificationList.append(notification)

class Booking:
    nextID = 10000
    def __init__(self, customer: Customer, createdTime: datetime, screeningDetail: Screening, 
                 seats: List[CinemaHallSeat], orderTotal: float, paymentDetail: 'Payment', status: int):
        self.__bookingID = Booking.nextID 
        self.__customer = customer
        self.__createdOn = createdTime
        self.__screeningDetail = screeningDetail
        self.__seats = seats
        self.__orderTotal = orderTotal
        self.__paymentDetail = paymentDetail
        self.__status = status
        Booking.nextID += 1
        

    # Getter methods for the private attributes
    @property
    def bookingID(self) -> int:
        return self.__bookingID

    @property
    def customer(self) -> 'Customer':
        return self.__customer

    @property
    def createdOn(self) -> datetime:
        return self.__createdOn

    @property
    def screeningDetail(self) -> 'Screening':
        return self.__screeningDetail

    @property
    def seats(self) -> List['CinemaHallSeat']:
        return self.__seats

    @property
    def orderTotal(self) -> float:
        return self.__orderTotal

    @property
    def paymentDetail(self) -> 'Payment':
        return self.__paymentDetail
    
    @property
    def status(self) -> int:
        return self.__status
    
    @status.setter
    def status(self, new_status):
        self.__status = new_status

class Notification:
    nextID = 100000
    def __init__(self, createdTime: datetime, content:str):
        self.__notificationID = Notification.nextID
        self.__createdOn = createdTime
        self.__content = content
        Notification.nextID += 1

    @property
    def notificationID(self):
        return self.__notificationID
    
    @property
    def createTime(self):
        return self.__createdOn
    
    @property
    def content(self):
        return self.__content

class Payment:
    nextID = 1000000
    def __init__(self, amount, createdTime, cardNumber: str, cardType: str, bankName: str, expiryDate: date, nameOnCard: str):
        self.__paymentID = Payment.nextID
        self.__amount = amount
        self.__createdTime = createdTime
        self.__cardNumber = cardNumber
        self.__cardType = cardType
        self.__bankName = bankName
        self.__expiryDate = expiryDate
        self.__nameOnCard = nameOnCard
        Payment.nextID += 1

    @property
    def paymentID(self):
        return self.__paymentID
    
    @property
    def amount(self):
        return self.__amount
    
    @property
    def createTime(self):
        return self.__createdTime
    
    @property
    def cardNumber(self) -> str:
        return self.__cardNumber

    @property
    def cardType(self) -> str:
        return self.__cardType

    @property
    def bankName(self) -> str:
        return self.__bankName

    @property
    def expiryDate(self) -> date:
        return self.__expiryDate

    @property
    def nameOnCard(self) -> str:
        return self.__nameOnCard


class Coupon:
    def __init__(self, couponID: str, expiryDate: date, discount: float):
        self.__couponID = couponID
        self.__expiryDate = expiryDate
        self.__discount = discount

    @property
    def couponID(self) -> str:
        return self.__couponID
    
    @property
    def expiryDate(self) -> date:
        return self.__expiryDate

    @property
    def discount(self) -> float:
        return self.__discount

