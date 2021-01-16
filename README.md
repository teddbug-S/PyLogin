# PyLogin
This project is a fully featured login system written in Python. It uses the sqlite3 database and has support for admins of different types with different permissions or privileges admins can use to control users registered in their app.

# Usage
  - First find the start method of the Main class located in main.py and change the context to either ON_LOGIN_USER for a normal user or ON_LOGIN_ADMIN for admin
  same for the sign up too, ON_SIGN_UP_USER for creating a user account and ON_SIGN_UP_ADMIN for creating an admin account.
  
  - Just run the main.py file
  
  - If deleting a user, clearing of database and deleting admin raises an error, got verifiers.py and fill in the your gmail creds. You still need some setups with your gmail first. See [enable lesss secure apps in gmail ](https://www.lifewire.com/unlock-gmail-for-a-new-email-program-or-service-1171974#:~:text=To%20enable%20%22less%20secure%22%20email%20programs%20to%20access,sure%20Allow%20less%20secure%20apps%20is%20On%20.) for more details.
