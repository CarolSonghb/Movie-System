# Student Name: Carol song
# Student ID: 1154836

from datetime import date, datetime
from typing import List
from abc import ABC, ABCMeta, abstractmethod

class Movie:
    def __init__(self, title: str, description: str, durationMins: int, language: str, releaseDate: date, 
                 country: str, genre: str):
        self.__title = title
        self.__description = description
        self.__durationMins = durationMins
        self.__language = language
        self.__releaseDate = releaseDate
        self.__country = country
        self.__genre = genre
        self.__screeningList: List[Screening] = []

    @property
    def title(self):
        return self.__title
    
    @property
    def description(self):
        return self.__description
    
    @property
    def durationMins(self):
        return self.__durationMins
    
    @property
    def language(self):
        return self.__language
    
    @property
    def releaseDate(self):
        return self.__releaseDate
    
    @property
    def country(self):
        return self.__country
    
    @property
    def genre(self):
        return self.__genre

    def screeningList(self) -> List['Screening']:
        return self.__screeningList
    
    def add_screening(self, screening: 'Screening'):
        self.__screeningList.append(screening)

    def find_screening(self, screening_id: int) -> 'Screening':
        for screening in self.__screeningList:
            if screening.screeningID == screening_id:
                return screening
        return None
    
    def cancel_screening(self, screening: 'Screening'):
        if screening in self.__screeningList:
            self.__screeningList.remove(screening)
    
    def __str__(self) -> str:
        return f"{self.__title}, {self.__description}, {self.__durationMins}, {self.__language}, {self.__releaseDate}, {self.__country}, {self.__genre}"
    

class Screening:
    nextID = 2000000
    def __init__(self, movie:Movie, screeningDate: date, startTime: datetime, endTime: datetime, hall: str):
        self.__movie = movie
        self.__screeningID = Screening.nextID
        self.__screeningDate = screeningDate
        self.__startTime = startTime 
        self.__endTime = endTime
        self.__hall = hall
        Screening.nextID += 1

    
    @property
    def movie_title(self) -> str:
        return self.__movie.title
    
    @property
    def screeningID(self) ->int:
        return self.__screeningID
    
    # Getter and setter for screeningDate
    @property
    def screeningDate(self) -> date:
        return self.__screeningDate
    
    @screeningDate.setter
    def screeningDate(self, new_screeningDate: date):
        self.__screeningDate = new_screeningDate

    # Getter and setter for startTime
    @property
    def startTime(self) -> datetime:
        return self.__startTime
    
    @startTime.setter
    def startTime(self, new_startTime: datetime):
        self.__startTime = new_startTime

    # Getter and setter for endTime
    @property
    def endTime(self) -> datetime:
        return self.__endTime
    
    @endTime.setter
    def endTime(self, new_endTime: datetime):
        self.__endTime = new_endTime

    # Getter and setter for hall
    @property
    def hall(self) -> str:
        return self.__hall
    
    @hall.setter
    def hall(self, new_hall: str):
        self.__hall = new_hall

class CinemaHall:
    def __init__(self, name: str, totalSeats: int, seatPrice: float, listOfSeats: List['CinemaHallSeat']):
        self.__name = name
        self.__totalSeats = totalSeats
        self.__seatPrice = seatPrice
        self.__listOfSeats = listOfSeats
        self.__screenings = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def totalSeats(self) -> int:
        return self.__totalSeats
    
    @property
    def seatPrice(self) -> float:
        return self.__seatPrice

    @property
    def listOfSeats(self) -> List['CinemaHallSeat']:
        return self.__listOfSeats
    
    @property
    def screenings(self) -> List['Screening']:
        return self.__screenings
    
    def addScreening(self, screening: 'Screening'):
        self.__screenings.append(screening)

    def cancelScreening(self, screening: 'Screening'):
        self.__screenings.remove(screening)
    
class CinemaHallSeat:
    def __init__(self, seatNumber: int, seatRow: str, seatType: str, isReserved: bool):
        self.__seatNumber = seatNumber
        self.__seatRow = seatRow
        self.__seatType = seatType
        self.__isReserved = isReserved

    @property
    def seatNumber(self) -> int:
        return self.__seatNumber

    @property
    def seatRow(self) -> str:
        return self.__seatRow

    @property
    def seatType(self) -> str:
        return self.__seatType

    @property
    def isReserved(self) -> bool:
        return self.__isReserved
    
    @isReserved.setter
    def isReserved(self, new_isReserved: bool):
        self.__isReserved = new_isReserved
        
    @property
    def seatPrice(self) -> float:
        return self.__seatPrice
    
    def reserveSatus(self) -> str:
        if self.isReserved is False:
            return "Available"
        else:
            return "Occupied"
         
    def __str__(self) -> str:
        return f"Seat Number: {self.seatNumber}, Row: {self.seatRow}, Type: {self.seatType}, Reserved: {self.reserveSatus}, Price: {self.seatPrice}"



