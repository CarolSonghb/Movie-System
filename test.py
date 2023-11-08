# Student Name: Carol song
# Student ID: 1154836

import pytest
from controller import *
from datetime import datetime, date
from unittest.mock import Mock, patch

# Test Guest class
def test_initial_guest_state():
    guest = Guest()
    assert guest.isRegistered == False, "New guest should not be registered"

def test_guest_registration():
    guest = Guest()
    guest.register()
    assert guest.isRegistered == True, "Guest should be registered after calling register method"

# Test User class
def test_user_login():
    user = User("username", "password", "name", "address", "email", "phone")
    assert user.login("password") == True
 
def test_user_logout():
    user = User("username", "password", "name", "address", "email", "phone")
    assert user.logout() == False

# Test Admin class
def test_admin_add_movie():
    admin = Admin("admin", "password", "name", "address", "email", "phone")
    movie = Movie("Movie Title", "Movie Description", 120, "English", date(2023, 1, 1), "USA", "Action")
    assert admin.addMovie(cinema, movie) == True


# Test Customer class
def test_customer_make_booking():
    customer = Customer("customer", "password", "name", "address", "email", "phone")
    title = "Avatar 2"
    description = "A sequel to the 2009 epic science fiction film Avatar."
    duration_mins = 180
    language = "English"
    release_date = date(2022, 12, 16)
    country = "United States"
    genre = "Science Fiction"
    movie = Movie(title, description, duration_mins, language, release_date, country, genre)
    screening_date = date(2023, 12, 25)
    start_time = datetime(2023, 12, 25, 10, 0)
    end_time = datetime(2023, 12, 25, 12, 0)
    hall = "Hall 1"
    screening = Screening(movie, screening_date, start_time, end_time, hall)
    seat1 = CinemaHallSeat(1, 'A', 'Standard', False)
    seats = [seat1]
    created_time = datetime.now()
    order_total = 100
    payment_date = datetime.now()
    card_number = '1234567890123456'
    card_type = 'Credit'
    bank_name = 'Bank of America'
    expiry_date = date(2025, 12, 31)
    name_on_card = 'John Doe'
    payment = Payment(order_total, payment_date, card_number, card_type, bank_name, expiry_date, name_on_card)
    status = 0  # Assuming 0 is the default status for a new booking
    booking = Booking(customer, created_time, screening, seats, order_total, payment, status)
    assert customer.makeBooking(booking) == True


def test_find_booking():
    customer = Customer('username', 'password', 'name', 'address', 'email', 'phone')
    screening = Screening(None, date.today(), datetime.now(), datetime.now(), 'hall')
    payment = Payment(100, datetime.now(), 'cardNumber', 'cardType', 'bankName', date.today(), 'nameOnCard')
    booking = Booking(customer, datetime.now(), screening, [], 100, payment, 1)
    customer.makeBooking(booking)
    assert customer.findBooking(booking.bookingID) == booking

def test_cancel_booking():
    customer = Customer('username', 'password', 'name', 'address', 'email', 'phone')
    screening = Screening(None, date.today(), datetime.now(), datetime.now(), 'hall')
    payment = Payment(100, datetime.now(), 'cardNumber', 'cardType', 'bankName', date.today(), 'nameOnCard')
    booking = Booking(customer, datetime.now(), screening, [], 100, payment, 1)
    customer.makeBooking(booking)
    assert customer.cancelBooking(booking) == True

def test_notification_list_setter():
    customer = Customer('username', 'password', 'name', 'address', 'email', 'phone')
    notification = Notification(datetime.now(), 'content')
    customer.notificationList = notification
    assert notification in customer.notificationList

# Test CinemaController class
def test_cinema_controller_instance():
    cinema_controller = CinemaController('Lincoln Cinema')
    assert isinstance(cinema_controller, CinemaController)

def test_cinema_controller_add_remove_movie():
    cinema_controller = CinemaController("Lincoln Cinema")
    title = "Avatar 2"
    description = "A sequel to the 2009 epic science fiction film Avatar."
    duration_mins = 180
    language = "English"
    release_date = date(2022, 12, 16)
    country = "United States"
    genre = "Science Fiction"
    movie = Movie(title, description, duration_mins, language, release_date, country, genre)
    cinema_controller.add_newmovie(movie)
    assert movie in cinema_controller.allMovies
    cinema_controller.cancel_movie(movie)
    assert movie not in cinema_controller.allMovies


def test_cinema_controller_get_movie():
    cinema_controller = CinemaController("Lincoln Cinema")
    movie = Movie("Movie Title", "Description", 120, "English", date(2023, 1, 1), "USA", "Action")
    cinema_controller.add_newmovie(movie)
    found_movie = cinema_controller.find_movie('Movie Title')
    assert found_movie is not None
    assert found_movie.title == 'Movie Title'
    assert found_movie.description == 'Description'
    assert found_movie.durationMins == 120
    assert found_movie.language == 'English'
    assert found_movie.releaseDate == date(2023, 1, 1)
    assert found_movie.country == 'USA'
    assert found_movie.genre == 'Action'

# Test Movie class
def test_movie_instance():
    movie = Movie("Movie Title", "Movie Description", 120, "English", date.today(), "USA", "Action")
    assert isinstance(movie, Movie)

# Test Screening class
def test_screening_instance():
    movie = Movie("Movie Title", "Movie Description", 120, "English", date.today(), "USA", "Action")
    screening = Screening(movie, date.today(), datetime.now(), datetime.now(), "Hall 1")
    assert isinstance(screening, Screening)

# Test CinemaHallSeat class
def test_cinema_hall_seat_instance():
    seat = CinemaHallSeat(1, "A", "Standard", False)
    assert isinstance(seat, CinemaHallSeat)

# Test Payment class
def test_payment_instance():
    payment = Payment(100, datetime.now(), 'cardNumber', 'cardType', 'bankName', date.today(), 'nameOnCard')
    assert isinstance(payment, Payment)

# Test Booking class
def test_booking_instance():
    customer = Customer('username', 'password', 'name', 'address', 'email', 'phone')
    screening = Screening(None, date.today(), datetime.now(), datetime.now(), 'hall')
    payment = Payment(100, datetime.now(), 'cardNumber', 'cardType', 'bankName', date.today(), 'nameOnCard')
    booking = Booking(customer, datetime.now(), screening, [], 100, payment, 1)
    assert isinstance(booking, Booking)

# Test Notification class
def test_notification_instance():
    created_time = datetime.now()
    content = 'Notification content'
    notification = Notification(created_time, content)
    assert isinstance(notification, Notification)

class TestAdminAddMovie:
    def test_add_movie_success(self):
        cinema = Mock()
        movie = Mock()
        admin = Admin(
            username="admin1",
            password="1234",
            name="Admin One",
            address="123 Main St",
            email="admin1@example.com",
            phone="555-1234",
        )

        cinema.add_newmovie.return_value = None  # Mock the return value of add_newmovie

        result = admin.addMovie(cinema, movie)

        cinema.add_newmovie.assert_called_once_with(movie)  # Assert that add_newmovie was called with the movie
        assert result == True  # Assert that the function returned True

    def test_add_movie_failure(self):
        cinema = Mock()
        movie = Mock()
        admin = Admin(
            username="admin1",
            password="1234",
            name="Admin One",
            address="123 Main St",
            email="admin1@example.com",
            phone="555-1234",
        )

        cinema.add_newmovie.side_effect = Exception("Test error")  # Mock an exception being raised

        result = admin.addMovie(cinema, movie)

        cinema.add_newmovie.assert_called_once_with(movie)  # Assert that add_newmovie was called with the movie
        assert result == False  # Assert that the function returned False

import pytest
from unittest.mock import Mock, patch

class TestAdminAddScreening:
    def test_add_screening_success(self):
        admin = Admin(
            username="admin1",
            password="1234",
            name="Admin One",
            address="123 Main St",
            email="admin1@example.com",
            phone="555-1234",
        )
        movie = Mock()
        hall = Mock()
        screening = Mock()
        screening.movie = movie
        screening.hall = hall

        movie.add_screening.return_value = None  # Mock the return value of add_screening
        hall.addScreening.return_value = None  # Mock the return value of addScreening

        result = admin.addScreening(screening)

        movie.add_screening.assert_called_once_with(screening)  # Assert that add_screening was called with the screening
        hall.addScreening.assert_called_once_with(screening)  # Assert that addScreening was called with the screening
        assert result == True  # Assert that the function returned True

    def test_add_screening_failure(self):
        admin = Admin(
            username="admin1",
            password="1234",
            name="Admin One",
            address="123 Main St",
            email="admin1@example.com",
            phone="555-1234",
        )
        movie = Mock()
        hall = Mock()
        screening = Mock()
        screening.movie = movie
        screening.hall = hall

        movie.add_screening.side_effect = Exception("Test error")  # Mock an exception being raised

        result = admin.addScreening(screening)

        movie.add_screening.assert_called_once_with(screening)  # Assert that add_screening was called with the screening
        assert result == False  # Assert that the function returned False

class TestAdminCancelMovie:
    def test_cancel_movie_success(self):
        admin = Admin(
            username="admin1",
            password="1234",
            name="Admin One",
            address="123 Main St",
            email="admin1@example.com",
            phone="555-1234",
        )
        cinema = Mock()
        movie = Mock()

        cinema.cancel_movie.return_value = None  # Mock the return value of cancel_movie

        result = admin.cancelMovie(cinema, movie)

        cinema.cancel_movie.assert_called_once_with(movie)  # Assert that cancel_movie was called with the movie
        assert result == True  # Assert that the function returned True

    def test_cancel_movie_failure(self):
        admin = Admin(
            username="admin1",
            password="1234",
            name="Admin One",
            address="123 Main St",
            email="admin1@example.com",
            phone="555-1234",
        )
        cinema = Mock()
        movie = Mock()

        cinema.cancel_movie.side_effect = Exception("Test error")  # Mock an exception being raised

        result = admin.cancelMovie(cinema, movie)

        cinema.cancel_movie.assert_called_once_with(movie)  # Assert that cancel_movie was called with the movie
        assert result == False  # Assert that the function returned False

class TestAdminCancelScreening:
    def test_cancel_screening_success(self):
        admin = Admin(
            username="admin1",
            password="1234",
            name="Admin One",
            address="123 Main St",
            email="admin1@example.com",
            phone="555-1234",
        )
        cinema = Mock()
        movie = Mock()
        hall = Mock()
        screening = Mock()
        screening.movie = movie
        screening.hall = hall

        movie.cancel_screening.return_value = None  # Mock the return value of cancel_screening
        hall.cancelScreening.return_value = None  # Mock the return value of cancelScreening

        result = admin.cancelScreening(cinema, screening)

        movie.cancel_screening.assert_called_once_with(screening)  # Assert that cancel_screening was called with the screening
        hall.cancelScreening.assert_called_once_with(screening)  # Assert that cancelScreening was called with the screening
        assert result == True  # Assert that the function returned True

    def test_cancel_screening_failure(self):
        admin = Admin(
            username="admin1",
            password="1234",
            name="Admin One",
            address="123 Main St",
            email="admin1@example.com",
            phone="555-1234",
        )
        cinema = Mock()
        movie = Mock()
        hall = Mock()
        screening = Mock()
        screening.movie = movie
        screening.hall = hall

        movie.cancel_screening.side_effect = Exception("Test error")  # Mock an exception being raised

        result = admin.cancelScreening(cinema, screening)

        movie.cancel_screening.assert_called_once_with(screening)  # Assert that cancel_screening was called with the screening
        assert result == False  # Assert that the function returned False

