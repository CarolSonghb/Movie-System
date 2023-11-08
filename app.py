# Student Name: Carol song
# Student ID: 1154836

from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages, jsonify
from datetime import date, timedelta
from Model_Cinema import *
from controller import *
import json


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

#read and populate hall info
halls = []
with open("json/halls.json", 'r') as hallfile:
    data = json.load(hallfile)
    for hall_data in data['hall']:
        seats = []
        total_seats = hall_data['seats']
        seat_price = hall_data['seatPrice']
        columns = hall_data['columns']
        rows = total_seats // columns

        seat_number = 1
        seat_row = 'A'  # Start from row 'A'
        for row in range(rows):
            for col in range(1, columns + 1):
                seat_type = hall_data['seatType']
                is_reserved = False
                
                seat = CinemaHallSeat(seat_number, seat_row, seat_type, is_reserved)
                seats.append(seat)
                seat_number += 1
            # After processing one row, move to the next row alphabetically
            seat_row = chr(ord(seat_row) + 1)

        hall = CinemaHall(hall_data['name'], total_seats, seat_price, seats)
        halls.append(hall)

# first_hall = halls[0]
# print("Hall Name:", first_hall.name)
# print("Total Seats:", first_hall.totalSeats)

# for seat in first_hall.listOfSeats:
#     print(f"Seat Number: {seat.seatNumber}, Row: {seat.seatRow}, Type: {seat.seatType}, Reserved: {seat.isReserved}")

# read movie file and create Movie object then add to the controller movie list
movies = []
with open("json/movie.json", 'r') as moviefile:
    movie_data = json.load(moviefile)
    for data in movie_data:
        title = data['title']
        description = data['description']
        durationMins = data['durationMins']
        language = data['language']
        releaseDate = data['releaseDate']
        country = data['country']
        genre = data['genre']

        # Convert releaseDate string to a date object
        release_date = date.fromisoformat(releaseDate)

        # Create a Movie object
        movie = Movie(title, description, int(durationMins), language, release_date, country, genre)
        
        # Create and add Screening objects to the Movie object
        for screening_data in data.get('screenings', []):
            screening_date = date.fromisoformat(screening_data['screeningDate'])
            start_time = screening_data['startTime']
            end_time = screening_data['endTime']
            hall_name = screening_data['hall']

            hall_instance = None
            for hall in halls:
                if hall.name == hall_name:
                    hall_instance = hall
                    break

            screening = Screening(movie, screening_date, start_time, end_time, hall_instance)
            movie.add_screening(screening) 
            hall_instance.addScreening(screening)
        # Append the Movie object to the temporary list
        movies.append(movie)

# Create an instance of CinemaController
cinema = CinemaController("Lincoln Cinema")
cinema.add_movies(movies)

# read user file and create User objects then add to controller customer list
# Initialize empty lists for each role
admins = []
front_desk_staff = []
customers = []
with open("json/user.json", 'r') as userfile:
    data = json.load(userfile)
    for user in data:
        username = user['username']
        password = user['password']
        role = user['role']
        fullname = user['fullname']
        address = user['address']
        email = user['email']
        phone = user['phone']
        if role == "admin":
            admin = Admin(username, password, fullname, address, email, phone)
            admins.append(admin)
        elif role == "staff":
            staff = FrontDeskStaff(username, password, fullname, address, email, phone)
            front_desk_staff.append(staff)
        elif role == "customer":
            customer = Customer(username, password, fullname, address, email, phone)
            customers.append(customer)
            cinema.addCustomer(customer)


@app.route('/')
def home():
    return render_template ('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None  # Initialize error message

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and the password is correct
        user = None
        for admin in admins:
            if admin.username == username and admin.login(password):
                user = admin
                break
        if user is None:
            for staff in front_desk_staff:
                if staff.username == username and staff.login(password):
                    user = staff
                    break
        if user is None:
            for customer in customers:
                if customer.username == username and customer.login(password):
                    user = customer
                    break

        if user is not None:
            # Store the user's role in the session
            session['user_role'] = user.role
            session['user_fullname'] = user.pName
            session['user_id'] = user.username

            if session['user_role'] == 'customer':
                return redirect(url_for('browse_movie'))
            elif session['user_role'] == 'staff':
                return redirect(url_for('staff'))
                pass
            elif session['user_role'] == 'admin':
                return redirect(url_for('admin'))
        else:
            # Set an error message for incorrect login attempt
            error_message = "Incorrect username or password, please try again."

    # If it's a GET request or authentication fails, or after form submission, render the login page
    return render_template('login.html', error_message=error_message)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # Retrieve registration form data
        username = request.form['registerUsername']
        password = request.form['registerPassword']
        fullname = request.form['registerName']
        address = request.form['registerAddress']
        email = request.form['registerEmail']
        phone = request.form['registerPhone']

        # Check if username already exists in any of the lists
        existing_usernames = [admin.username for admin in admins]
        existing_usernames += [staff.username for staff in front_desk_staff]
        existing_usernames += [customer.username for customer in customers]

        if username in existing_usernames:
            flash('Username already exists, please choose another one.','error')
            return redirect(url_for('login'))

        # Create a new user (e.g., Customer) with the registration data
        new_customer = Customer(username, password, fullname, address, email, phone)
        customers.append(new_customer)  # Add the new user to your list of customers
        cinema.addCustomer(new_customer)

        # Flash a success message
        flash(f'New customer {fullname} has been registered', 'success')

        user_role = request.form.get('user_role')
        if user_role == 'staff':
            return redirect(url_for('staff'))
        
        return redirect(url_for('login'))


@app.route('/browse-movie')
def browse_movie():
    return render_template('browsemovie.html', cinema_movie = cinema.allMovies)

@app.route('/search-movie', methods=['GET'])
def search_movie():
    # Get the search criteria from the URL query parameters
    criteria = request.args.get('criteria')
    query = request.args.get('query')
    filtered_movies = cinema.search_movies(criteria, query, cinema.allMovies)
    print(filtered_movies)

    # Render the template with the filtered movies
    return render_template('browsemovie.html', cinema_movie=filtered_movies)

@app.route('/screening_list')
def screening_list():
    movie_title = request.args.get('movie_title')
    movie = cinema.find_movie(movie_title)
    return render_template('screeninglist.html', selected_movie = movie)

@app.route('/seats/screening<int:screening_id>')
def seats(screening_id):
    if 'user_id' not in session:
        flash("You must log in first to book tickets")
        return redirect(url_for('login'))
    movie_title = request.args.get('movie_title')
    movie = cinema.find_movie(movie_title)
    screening = movie.find_screening(screening_id)
    screening_hall = screening.hall
    return render_template('screeningseats.html', selected_movie=movie, screening=screening, 
                           screening_hall=screening_hall)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        session['movie_title'] = request.form.get('title')
        session['screeningID'] = request.form.get('screeningid')
        session['seatSelected'] = request.form.get('seats')
        session['totalPrice'] = request.form.get('price')

    movie = cinema.find_movie(session['movie_title'])
    screening = movie.find_screening(int(session['screeningID']))
    screening_hall = screening.hall
    return render_template('payment.html', movie=movie, screening=screening, 
                           seatSelected=session['seatSelected'], totalPrice=session['totalPrice'], 
                           screening_hall=screening_hall)

# read and populate coupon info
@app.route('/api/coupons', methods=['GET'])
def get_coupons():
    couponList = []
    with open('json/coupon.json', 'r') as couponfile:
        data = json.load(couponfile)
        for coupon_data in data:
            couponID = coupon_data['couponID']
            expiryDate = coupon_data['expiryDate']
            discount = coupon_data['discount']
            coupon = Coupon(couponID, expiryDate, discount)
            coupon_dict = {
                'couponID': coupon.couponID,
                'expiryDate': coupon.expiryDate,
                'discount': coupon.discount
            }
            couponList.append(coupon_dict)
    return jsonify(couponList)

@app.route('/create-payment', methods=['POST'])
def create_payment():
    amount = request.form.get('amount')
    card_number = request.form.get('cardNumber')
    card_type = request.form.get('cardType')
    bank_name = request.form.get('bankName')
    expiry_date = request.form.get('expiryDate')
    name_on_card = request.form.get('nameOnCard')

    # Check if the payment type is Cash, and skip card validations
    if card_type != 'Cash':
        bank_name = request.form.get('bankName')
        expiry_date = request.form.get('expiryDate')
        name_on_card = request.form.get('nameOnCard')
        
        # Card number validation: 16 digits
        if not card_number or not card_number.isdigit() or len(card_number) != 16:
            flash('Invalid card number. Please enter a valid 16-digit card number.', 'error')
            return redirect(url_for('payment'))

        # Bank name validation
        if not bank_name or not bank_name.replace(' ', '').isalpha():
            flash('Invalid bank name. Please enter a valid bank name.', 'error')
            return redirect(url_for('payment'))

        # Expiry date validation
        try:
            exp_date_obj = datetime.strptime(expiry_date, '%Y-%m-%d').date()
            if exp_date_obj < datetime.now().date():
                flash('Invalid expiry date. Please select a future date.', 'error')
                return redirect(url_for('payment'))
        except:
            flash('Invalid expiry date format.', 'error')
            return redirect(url_for('payment'))

        # Name on card validation
        if not name_on_card or not name_on_card.replace(' ', '').isalpha():
            flash('Invalid name. Please enter a valid name on the card without any numbers or special characters.', 'error')
            return redirect(url_for('payment'))
    else:  # This is for the 'Cash' scenario
        bank_name = None
        expiry_date = None
        name_on_card = None
    
    created_time = datetime.now()
    payment = Payment(amount, created_time, card_number, card_type, bank_name, expiry_date, name_on_card)
    
    if session['user_role'] == 'customer':
        customer = cinema.find_customer(session['user_id'])
    elif session['user_role'] == 'staff':
        customer_name = request.form.get('customerName')
        customer = cinema.get_customer(customer_name)
        print(customer)
        # Check if customer is None or not found
        if customer is None:
            flash("Customer name doesn't exist, please register the new customer first.", 'error')
            return redirect(url_for('payment'))


    screeningID = int(request.form.get('screening_id'))
    movie_title = request.form.get('movie_title')
    movie = cinema.find_movie(movie_title)
    screening = movie.find_screening(screeningID)
    seats = request.form.get('seatSelected')
    payment = payment 
    status = 1
    initial_len = len(customer.bookingList)
    booking = Booking(customer, created_time, screening, seats, amount, payment, status)
    customer.makeBooking(booking)
    cinema.add_booking(booking)
    print(f"length: {len(cinema.allBookings)}")
    if len(customer.bookingList) == initial_len + 1:
        flash('Booking added successfully', 'success')
    else:
        flash('Error: Booking could not be added', 'error')
    content = f"You have made a booking for Movie {movie_title} on {screening.screeningDate} from {screening.startTime} to {screening.endTime} with the following seats: {seats}"
    notification = Notification(created_time, content)
    customer.notificationList = notification

    # change seat status
    seats_list = seats.split(",")
    print(seats_list)
    seat_numbers = [int(''.join(filter(str.isdigit, seat))) for seat in seats_list] 
    for seat_num in seat_numbers:
        for seat in screening.hall.listOfSeats:
            if seat.seatNumber == seat_num:
                seat.isReserved = True
                break
    if session['user_role'] == 'customer':
        return redirect(url_for('user_profile'))
    elif session['user_role'] == 'staff':
        return redirect(url_for('staff'))

@app.route('/user-profile')
def user_profile():
    customer = cinema.find_customer(session['user_id'])
    booking = customer.bookingList
    notifications = sorted(customer.notificationList, key=lambda x: x.createTime, reverse=True)
    return render_template('userprofile.html', customer=customer, booking = booking, notification=notifications)

@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    customer = cinema.find_customer(session['user_id'])
    booking = customer.findBooking(booking_id)
    customer.cancelBooking(booking)
    flash("Booking canceled")
    created_time = datetime.now()
    content = f"You have canceled booking {booking_id} "
    notification = Notification(created_time, content)
    customer.notificationList = notification
    return redirect(url_for('user_profile')) 

@app.route('/adminstaff-portal')
def adminstaff():
    return render_template('login.html')

@app.route('/admin')
def admin():
    movie = cinema.allMovies
    hall = halls
    return render_template('admin.html', movie = movie, hall = hall)

@app.route('/add_movie', methods=['POST'])
def add_movie():
    # Extracting data from form
    title = request.form['title']
    description = request.form['description']
    durationMins = int(request.form['durationMins'])
    language = request.form['language']
    
    releaseDate_parts = request.form['releaseDate'].split('-')
    releaseDate = date(int(releaseDate_parts[0]), int(releaseDate_parts[1]), int(releaseDate_parts[2]))
    
    country = request.form['country']
    genre = request.form['genre']

    # Create a new movie instance
    new_movie = Movie(title, description, durationMins, language, releaseDate, country, genre)
    cinema.add_newmovie(new_movie)

    flash('Movie added successfully!', 'success')
    return redirect(url_for('browse_movie')) 

@app.route('/add_screening', methods=['GET','POST'])
def add_screening():
    title = request.form['movie']
    screening_date = request.form['screeningDate']
    print(screening_date)
    print(type(screening_date))
    new_screening_date = datetime.strptime(screening_date, '%Y-%m-%d').date()
    print(type(new_screening_date))
    start_time_str = request.form['startTime']
    hall_number = request.form['hall']
    movie = cinema.find_movie(title)
    print(hall_number)

    # Convert start_time to a datetime object
    start_time = datetime.strptime(screening_date + " " + start_time_str, '%Y-%m-%d %H:%M')
    # Calculate end_time using movie's duration
    end_time = start_time + timedelta(minutes=movie.durationMins)
    # Extract the time components
    start_time = start_time.time()
    end_time = end_time.time()
    
    hall_instance = None
    for hall in halls:
        if hall.name == hall_number:
            hall_instance = hall
            break
    
    for screening in hall_instance.screenings:
        if screening.screeningDate == new_screening_date:
            print("date matches")
            if (start_time >= screening.startTime and start_time < screening.endTime) or \
           (end_time > screening.startTime and end_time <= screening.endTime):
                print("Time overlaps")
            flash('Adding new screenig failed. There is already a screening in the same hall during that time period!', 'error')
            return redirect(url_for('screening_list', movie_title=movie.title))

            
    screening = Screening(movie, new_screening_date, start_time, end_time, hall_instance)
    movie.add_screening(screening)
    hall_instance.addScreening(screening)
    flash('Screening added successfully!', 'success')
    # Redirect to the movie's screening list page after adding
    return redirect(url_for('screening_list', movie_title=movie.title))

@app.route('/cancel-movie', methods=['POST'])
def cancel_movie():
    movie_title = request.form.get('movie')
    movie = cinema.find_movie(movie_title)

    # For each screening of the movie
    for screening in movie.screeningList():
        bookings = cinema.get_bookings(screening)
        for booking in bookings:
            customer = booking.customer
            notification_content = (f"The Movie {movie_title}, including the screening you booked on {screening.screeningDate} has been canceled. "
                                    f"The amount of {booking.orderTotal} has been refunded to your {booking.paymentDetail.cardType}.")
            new_notification = Notification(datetime.now(), notification_content)
            customer.notificationList = new_notification
            customer.cancelBooking(booking)
    cinema.cancel_movie(movie)
    flash(f'Movie {movie_title} has been canceled.')
    return render_template('browsemovie.html', cinema_movie = cinema.allMovies)

@app.route('/cancel-screening', methods=['POST'])
def cancel_screening():
    movie_title = request.form.get('movie_title')
    screening_id = request.form.get('screeningID')
    movie = cinema.find_movie(movie_title)
    screening = movie.find_screening(int(screening_id))
    movie.cancel_screening(screening)
    bookings = cinema.get_bookings(screening)
    print(bookings)
    for booking in bookings:
        customer = booking.customer
        notification_content = (f"The screening for {movie_title} on {screening.screeningDate} has been canceled. "
                                f"The amount of {booking.orderTotal} has been refunded to your {booking.paymentDetail.cardType}.")
        new_notification = Notification(datetime.now(), notification_content)
        customer.notificationList = new_notification
        customer.cancelBooking(booking)
    
    print(screening)
    print(screening.hall)
    hall_instance = None
    for hall in halls:
        if hall == screening.hall:
            hall_instance = hall
            break
    hall_instance.cancelScreening(screening)
    
    flash(f'Screening {screening_id} has been canceled, and a notification has been sent to customers who booked the screening.', 'success')
    return redirect(url_for('screening_list', movie_title=movie.title))

@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/allbookings')
def allbookings():
    bookings = cinema.allBookings
    return render_template('allbookings.html', bookings = bookings)

@app.route('/cancelbooking', methods=['POST'])
def cancelbooking():
    booking_id = int(request.form.get('bookingID'))
    customerName = request.form.get('customerName')
    customer = cinema.get_customer(customerName)
    booking = customer.findBooking(booking_id)
    print(f"length: {len(cinema.allBookings)}")
    cinema.cancel_booking(booking)
    customer.cancelBooking(booking)
    flash(f'Booking{booking_id} for {customerName} has been canceled')
    return redirect(url_for('allbookings', bookings = cinema.allBookings))



@app.route('/logout')
def logout():
    # Clear the session data to log the user out
    session.pop('user_role', None)
    session.pop('user_fullname', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
