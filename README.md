# Heaven pizza

[View Heaven Pizza live website here](https://heaven-pizza-d4d6b12eae4a.herokuapp.com/)

## Features 

### Existing features

- Home page

    - Shows the title and an introduction to heaven pizza followed by the options to see the menu and book a table.

        ![Home logged in](documentation/readme_images/home-loggedin.png)

    - Alternatively if the user its not logged in he gonna see an option to sign up instead.

        ![Home logged out](documentation/readme_images/home-loggedout.png)

- Menu page

    - Here we have the menu items with the option to filter them by type.
    - When go to menu page Starter item filter is selected by default.

        ![Menu](documentation/readme_images/menu-items.png)

- Location page

    - Here we have a map with the location of the restaurant marked on it(the location it's ficticious).

        ![Location](documentation/readme_images/location-img.png)

- Sign up page

    - Here we have a form to sign up to heaven pizza with multiple password requirements.

        ![Sign up](documentation/readme_images/signup-1.png)

    - Note that the username needs to be unique.

        ![User already exists](documentation/readme_images/signup-2.png)

    - Theres also a link to sign in if already have an account.

        ![Already have account?](documentation/readme_images/signup-3.png)

- Sign in page 

    - Here we have a form to log in, aswell with a link to sign up if needed.

        ![Sign in](documentation/readme_images/signin.png)

- Book now page

    - Here we have the form to book a table.
    - Booking name its requierd
    - Number of guest must be 1-10
    - Date and time its prefilled with the actual date and time.
    - Allergies, Table preferences and child chair are optionals.

        ![booking form](documentation/readme_images/book-form-1.png)

    - If try to find a table on the past, you get a message saying that you can't.

        ![Invalid date](documentation/readme_images/book-form-2.png)

    - When you try to find a table and there its not available you get 3 alternative options.

        ![Alternatives](documentation/readme_images/book-form-3.png)

    - If something went wrong you get a message saying so. 

        ![Error](documentation/readme_images/book-form-4.png)

- My bookings page

    - Here you can see you bookings splited in active and past.
    - Note that the server time its on UTC +0 so the active and past may differ depending on your timezone.

        ![My bookings](documentation/readme_images/my-booking-1.png)

    - The active bookings have the options to modify and cancel meanwhile the past one only have the option to cancel.

        ![My bookings buttons](documentation/readme_images/my-booking-2.png)

    - By pressing cancel you get a message poping up asking you if you are sure and if you confirm then you delete the booking.

        ![Cancel modal](documentation/readme_images/my-booking-5.png)

    - By pressing on modify booking you get a form that works the same way that the one on Booking page.
    - The form its prefilled with the booking data.

        ![Modify form](documentation/readme_images/my-booking-3.png)

    - When modifying a booking, the logic to check the availability ignore the actual booking when checking availability.

        ![Logic fragment](documentation/readme_images/my-booking-4.png)

- Log out page

    - By pressing sign out you logout and get redirected to the home page

        ![Log out](documentation/readme_images/logout.png)

- Navbar 

    - Here we have a responsive menu that change to a dropdown for mobile.

        ![navbar mobile](documentation/readme_images/navbar-3.png)

    - If the user its not logged in he will see sign up and login.

        ![navbar loggedout](documentation/readme_images/navbar-2.png)

    - If the user its logged in he will see book now, my bookings and logout,along with a hello **username** 

        ![navbar loggedin](documentation/readme_images/navbar-1.png)

- Footer
    
    - Here we have the contact details and the social medias
    - All social medias opens a link on a new tab.

        ![footer](documentation/readme_images/footer.png)

- Messages

    - When the user login, logout, signup or create, modify or delete a booking a closeable descriptive message will appear behind the navbar.

        ![Messages](documentation/readme_images/message.png)