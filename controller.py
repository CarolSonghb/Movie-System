# Student Name: Carol song
# Student ID: 1154836

from Model_User import *
from Model_Cinema import *

class CinemaController:
    def __init__(self, cname):
        self.__allMovies: List[Movie] = []
        self.__allCustomers: List[Customer] = []
        self.__allBookings: List[Booking] = []
        self.__cinemaName = cname
    
    @property
    def allMovies(self) -> List[Movie]:
        return self.__allMovies
    
    @property
    def allCustomers(self) -> List[Customer]:
        return self.__allCustomers
    
    @property
    def allBookings(self) -> List[Booking]:
        return self.__allBookings
    
    @property
    def cinemaName(self):
        return self.__cinemaName
    
    # Method for adding movies to the controller
    def add_movies(self, movies: List[Movie]):
        self.__allMovies.extend(movies)
    
    def add_newmovie(self, movie: Movie):
        self.__allMovies.append(movie)

    def cancel_movie(self, movie:Movie):
        self.__allMovies.remove(movie)
            
    def addCustomer(self, customer: Customer):
        self.allCustomers.append(customer)
    
    def find_movie(self, title: str) -> Movie:
        for movie in self.allMovies:
            if title == movie.title:
                return movie

    def find_customer(self, username: str) -> Customer:
        for customer in self.allCustomers:
            if customer.username == username:
                return customer
            
    def get_customer(self, fullname: str) -> Customer:
        for customer in self.allCustomers:
            if customer.pName == fullname:
                return customer
        
    def search_movies(self, criteria: str, query: str, movies: List[Movie]) -> List[Movie]:
        filtered_movies = []
        for movie in movies:
            if criteria == 'title' and query.lower() in movie.title.lower():
                filtered_movies.append(movie)
            elif criteria == 'language' and query.lower() in movie.language.lower():
                filtered_movies.append(movie)
            elif criteria == 'genre' and query.lower() in movie.genre.lower():
                filtered_movies.append(movie)
            elif criteria == 'releaseDate' and query.lower() in str(movie.releaseDate).lower():
                filtered_movies.append(movie)
            elif criteria == 'country' and query.lower() in movie.country.lower():
                filtered_movies.append(movie)
        return filtered_movies
    
    def add_booking(self, booking: Booking):
        self.__allBookings.append(booking)
        
    def get_bookings(self, screening: Screening) -> List[Booking]:
        return [booking for booking in self.allBookings if booking.screeningDetail == screening]
            
    def cancel_booking(self, booking: Booking):
        self.__allBookings.remove(booking)


        
    
cinema = CinemaController("Lincoln Cinema")


