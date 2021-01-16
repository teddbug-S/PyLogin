from hmac import compare_digest
from enum import Enum, unique
from getpass import getpass
from math import ceil, e
from pprint import pprint
from time import sleep
import random

from admin import Admin
from user import User
from resources.options import Option
from resources.arts import welcome_text
from services.print_rich import PrintRich
from user import User
from services import auths
from system.info_types import InfoTypes as it
from services.username_generator import generate_names
from services.verifiers import Verify, Action, VerifyInfo
from services._crypt import generate_token
from resources.arts import home_logos, profile_panel_user, welcome_text, profile_panel_admin
from services.print_rich import PrintRich


@unique
class Context(Enum):

    ON_START = 1
    ON_DASH  = 2
    ON_ADMIN_DASH  = 3
    ON_ADMIN = 4
    ON_SEARCH_USER = 5
    ON_SEARCH_ADMIN = 6
    ON_BLOCK_USER = 7
    ON_UNBLOCK_USER = 8
    ON_DELETE_USER = 9
    ON_DELETE_ADMIN = 10
    ON_CLEAR_DB = 11
    ON_LOGIN_ADMIN = 12
    ON_LOGIN_USER = 13
    ON_SIGN_UP_ADMIN = 14
    ON_SIGN_UP_USER = 15
    ON_START_ADMIN = 16
    ON_GET_TOKEN = 17
    ON_VERIFY_ACTION = 18



class Main:

    def __init__(self) -> None:
        self.context = None
        self.banner = None
        self.option = Option._init_option()
        self.auth_types = auths.AuthTypes
        self.prompt = None
        self.current_user = None
        self.current_admin = None
        self.rich = PrintRich()
    

    @staticmethod
    def _add_index(data):
        for d in range(len(data)):
            data[d] = f"[{d+1}]-{data[d]}"
        return data

    @staticmethod
    def clear_screen():
        from os import system
        system('cls')
    
    @property
    def _usernames(self):
        """
        Returns usernames based on context.
        """
        __admin = Admin() # admin object
        usernames = __admin._get_usernames() if self.context == Context.ON_SIGN_UP_USER else __admin._get_admin_usernames()
        if usernames == it.TABLE_NOT_FOUND:
            return []
        return usernames
    
    def _check_username(self, *args, func):
        """
        A decorator function for auths.auth_username
        for avoiding duplicate usernames
        """
        if (result := func(*args)) == self.auth_types.SUCCESS:
            username = args[0]
            if username in self._usernames:
                return self.auth_types.USERNAME_ALREADY_EXISTS
            return self.auth_types.SUCCESS
        return result

    
    def _get_menu(self):
        """
        Returns a menu which is a list of options,
        based on the current context of the application
        """
        if self.context == Context.ON_START:
            return self.option.start_options[:]
        elif self.context == Context.ON_DASH:
            return self.option.dashboard_options[:]
        elif self.context == Context.ON_ADMIN_DASH:
            return self.option.admin_dashboard_options[:]
        elif self.context == Context.ON_ADMIN:
            return self.option.admin_options[:]

    
    def print_menu(self):
        """
        Displays the available options in a nicely formatted way.
        """
        
        data = self._add_index(self._get_menu())
        per_row = 3 if len(data) // 3 > 0 else len(data)
        index = 0
        row_num = 1 if per_row < 3 else ceil(len(data)/per_row)
        for _ in range(row_num):
            for _ in range(per_row):
                try:  # EAFP
                    print(data[index], end='\t   '.expandtabs(len(max(data, key=lambda x: len(x)))-len(data[index])))
                    index += 1
                except:
                    pass
            print()

    
    @staticmethod
    def _print_home(data):
        """
        Displays the data in the home screen
        """
        for userdata in data:
            print(userdata)

    
        
    def delete_user(self):
        if self.context == Context.ON_DELETE_USER:
            admin = self.current_admin
            username = self._get_input_data() # get the username
            # first we search the username in the database
            response_1 = admin.search_user(username)
            if type(response_1) == it: # handle info type responses
                self.handle_response(response_1)
            else:
                user = response_1 # else if we get the data we want
                self.rich.print_data_panel([user.data_to_dict()], profile_panel_user )# print it out and confirm
                self.context = Context.ON_VERIFY_ACTION
                data = self._get_input_data()  # get yes or no from the admin
                if data == 'Y': # if admin wishes to proceed verify his or her legitimacy
                    # create a verifier object with reciepient set to email of admin and
                    # action of authentication
                    verifier = Verify(action=Action.AUTHENTICATE)
                    token = generate_token() # generate token
                    # generate the message with the token 
                    msg = verifier.generate_message(to=admin.logged_in_admin.email, username=username, token=token)
                    response = verifier.send_message(msg) # send message to admin
                    if response == VerifyInfo.SUCCESS:
                        self.context = Context.ON_GET_TOKEN # set context to on_get_token
                        data =  self._get_input_data() # ask admin to enter token
                        if compare_digest(data, token): # if tokens match
                            response_2 = admin._delete_user(username)
                            if response_2 == it.USER_DELETED_SUCCESSFULLY: # handle success response internally
                                print(f"\n{username} deleted successfully.✅")
                            else: # else if not success response, call the handler
                                self.handle_response(response_2)
                        else: # if tokens don't match
                            self.handle_response(it.WRONG_TOKEN)
                    else:
                        # call response handler
                        self.handle_response(response)
                elif data == 'N': # admin wants to abort action
                    self.handle_response(it.ACTION_ABORTED)
                else: # handle invalid input and abort action
                    self.handle_response(it.INVALID_INPUT)
                    self.handle_response(it.ACTION_ABORTED)
        else:
            pass

    
    def delete_admin(self):
        if self.context == Context.ON_DELETE_ADMIN:
            admin = self.current_admin
            username = self._get_input_data() # get the username
            # first we search the username in the database
            response_1 = admin.search_admin(username)
            if type(response_1) == it: # handle info type responses
                self.handle_response(response_1)
            else:
                user = response_1 # else if we get the data we want
                self.rich.print_data_panel([user.data_to_dict()], profile_panel_admin) # print it out and confirm
                self.context = Context.ON_VERIFY_ACTION
                data = self._get_input_data()  # get yes or no from the admin
                if data == 'Y': # if admin wishes to proceed verify his or her legitimacy
                    # create a verifier object with reciepient set to email of admin and
                    # action of authentication
                    verifier = Verify(action=Action.AUTHENTICATE)
                    token = generate_token() # generate token
                    # generate the message with the token 
                    msg = verifier.generate_message(to=admin.logged_in_admin.email, username=username, token=token)
                    response = verifier.send_message(msg) # send message to admin
                    if response == VerifyInfo.SUCCESS:
                        self.context = Context.ON_GET_TOKEN # set context to on_get_token
                        data =  self._get_input_data() # ask admin to enter token
                        if compare_digest(data, token): # if tokens match
                            response_2 = admin._delete_admin(username)
                            if response_2 == it.ADMIN_DELETED_SUCCESSFULLY: # handle success response internally
                                print(f"\n👨‍💻 Admin {username} deleted successfully.✅")
                            else: # else if not success response, call the handler
                                self.handle_response(response_2)
                        else: # if tokens don't match
                            self.handle_response(it.WRONG_TOKEN)
                    else:
                        # call response handler
                        self.handle_response(response)
                elif data == 'N': # admin wants to abort action
                    self.handle_response(it.ACTION_ABORTED)
                else: # handle invalid input and abort action  
                    self.handle_response(it.INVALID_INPUT)
                    self.handle_response(it.ACTION_ABORTED)
        else:
            pass

    
    def clear_db(self):
        """
        A method handler for Context.ON_CLEAR_DB
        """
        if self.context == Context.ON_CLEAR_DB:
            self.context = Context.ON_VERIFY_ACTION
            admin = self.current_admin
            print("\nThis action will wipe out the user database completely! 🤨")
            data = self._get_input_data() # get input
            if data == 'Y':
                # create a verifier object with reciepient set to email of admin and
                # action of authentication
                verifier = Verify(action=Action.AUTHENTICATE)
                token = generate_token() # generate token
                username = admin.logged_in_admin.username
                # generate the message with the token 
                msg = verifier.generate_message(to=admin.logged_in_admin.email, username=username, token=token)
                response = verifier.send_message(msg) # send message to admin
                if response == VerifyInfo.SUCCESS: # check if message was delivered
                    self.context = Context.ON_GET_TOKEN # set context to on_get_token
                    data = self._get_input_data() # ask admin to enter token
                    if compare_digest(data, token): # if tokens match
                        response = admin._clear_database()
                        if response == it.DATABASE_CLEARED_SUCCESSFULLY: # handle success response internally
                            print(f"\n 📀 Database cleared successfully.✅")
                        else: # else if not success response, call the handler
                            self.handle_response(response)
                    else: # if tokens don't match
                        self.handle_response(it.WRONG_TOKEN)
                else:
                    self.handle_response(response)
            elif data == 'N': # admin wants to abort action
                self.handle_response(it.ACTION_ABORTED)
            else:
                self.handle_response(it.INVALID_INPUT)
                self.handle_response(it.ACTION_ABORTED)

    def block_user(self):
        """
        A method handler for Context.ON_BLOCK_USER
        """
        if self.context == Context.ON_BLOCK_USER:
            admin = self.current_admin # set admin
            username = self._get_input_data() # get username
            response_1 = admin.search_user(username)
            if type(response_1) == it: # get response handler
                self.handle_response(response_1)
            else:
                user = response_1
                if not user.blockstatus: # check if user has not been already blocked.
                    self.rich.print_data_panel([user.data_to_dict()], profile_panel_user)# print it out and confirm
                    self.context = Context.ON_VERIFY_ACTION
                    data = self._get_input_data() # get input
                    if data == 'Y':
                        response_2 = admin.block_user(user.username) # get response on block user
                        if response_2 == it.USER_BLOCKED_SUCCESSFULLY:  
                            print(f"\n{username} blocked successfully.✅") # handle success response internally
                        else:
                            # else get response handler to do it
                            self.handle_response(response_2)
                    elif data == 'N':
                        self.handle_response(it.ACTION_ABORTED)
                    else:
                        # handle invalid input and abort action
                        self.handle_response(it.INVALID_INPUT)
                        self.handle_response(it.ACTION_ABORTED)
                else:
                    # call response handler
                    self.handle_response(it.USER_ALREADY_BLOCKED)
    
    
    def unblock_user(self):
        """
        A method handler for Context.ON_BLOCK_USER
        """
        if self.context == Context.ON_UNBLOCK_USER:
            admin = self.current_admin # set admin
            username = self._get_input_data() # get username
            response_1 = admin.search_user(username)
            if type(response_1) == it: # get response handler
                self.handle_response(response_1)
            else:
                user = response_1
                if user.blockstatus: # check if user has been blocked.
                    self.rich.print_data_panel([user.data_to_dict()], profile_panel_user) # print it out and confirm
                    self.context = Context.ON_VERIFY_ACTION
                    data = self._get_input_data() # get input
                    if data == 'Y':
                        response_2 = admin.unblock_user(user.username) # get response on block user
                        if response_2 == it.USER_UNBLOCKED_SUCCESSFULLY:  
                            print(f"\n{username} unblocked successfully.✅") # handle success response internally
                        else:
                            # else get response handler to do it
                            self.handle_response(response_2)
                    elif data == 'N':
                        self.handle_response(it.ACTION_ABORTED)
                    else:
                        # handle invalid input and abort action
                        self.handle_response(it.INVALID_INPUT)
                        self.handle_response(it.ACTION_ABORTED)
                else:
                    # call response handler
                    self.handle_response(it.USER_ALREADY_UNBLOCKED)

    def index_option(self, option, admin_type):
        """
        A method to redirect options selected by other admins apart
        from admin_types.ALMIGHTY to match the corresponding handler.

        Args:
            option: digit str
            admin_type: type of admin
        """
        permissions_count = (1, 13) # total number of permissions
        exclude = (0,) # number of excluded permissions
        # change the excludes based on the admins
        if admin_type == self.current_admin.admin_types.STANDARD:
            exclude = (2, 3) # exclude option 2 and 3 from standard admin
        elif admin_type == self.current_admin.admin_types.GUEST:
            exclude = (1, 2, 3, 4, 8) # exclude option 1, 2, 3, 4, 8 from guest
        # get the index from the permissions
        index = dict.fromkeys([i for i in range(1, len(self.current_admin.show_permissions())+1)])
        key = 1 # for matching the keys or the index
        for value in range(*permissions_count): # value is the total number of permissions
            if value in exclude: # now if an admin has excludes
                continue # skip it, don't add it
            index[key] = str(value) # else add it
            key += 1 # update key
        try:
            # now try to return the option
            return index[int(option)]
        except (KeyError, ValueError): # if option not found
            self.handle_response(it.INVALID_INPUT)
             # call the response handler with the appropriate response


    def _get_input_data(self):
        """
        An Interface for taking user inputs in one place,
        based on the current context of the application
        """
        if self.context in (Context.ON_LOGIN_ADMIN, Context.ON_LOGIN_USER):
            username = input("\nUsername: ")
            password = getpass("Password: ")
            return (username, password)
        
        elif self.context in (Context.ON_SIGN_UP_USER, Context.ON_SIGN_UP_ADMIN):
            data = []
            while True:
                firstname = input("Firstname: ")
                if auths.auth_name(firstname) == self.auth_types.SUCCESS:
                    data.append(firstname.title())
                    break
                print("Firstname contains an illegal character.")
            
            while True:
                lastname = input("Lastname: ")
                if auths.auth_name(lastname) == self.auth_types.SUCCESS:
                    data.append(lastname.title())
                    break
                print("Lastname contains an illegal character.")
            
            while True:
                check, age = auths.auth_age(input("Age: "), genesis := 12)
                if check == self.auth_types.SUCCESS:
                    data.append(age)
                    break
                elif check == self.auth_types.NOT_AN_INTEGER:
                    print("Illegal character, age should be an integer.")
                else:
                    print(f"Age should be above {genesis} years.")

            while True:
                username = input("Username: ")
                if (check := self._check_username(username, func=auths.auth_username)) == self.auth_types.SUCCESS:
                    data.insert(0, username)
                    break
                elif check == self.auth_types.ILLEGAL_START:
                    print("Username can only start with an alphabet")
                elif check == self.auth_types.LONG_USERNAME:
                    print("Username too long, max length is 15")
                elif check == self.auth_types.CONTAINS_ILLEGAL_CHARS:
                    print("Username contains can only contain an underscore and digits apart from the alphabets.")
                elif check == self.auth_types.USERNAME_ALREADY_EXISTS:
                    print("\nUsername already taken")
                    print(f"Available: {generate_names(data[0], data[1], self._usernames, 5)}\n")
            
            while True:
                password = getpass("Password: ")
                confirm_password = getpass("Re-enter password: ")
                if (check := auths.auth_password(password, confirm_password)) == self.auth_types.SUCCESS:
                    data.append(password)
                    break
                elif check == self.auth_types.LONG_PASSWORD:
                    print("Password too long max length is 30.")
                elif check == self.auth_types.PASSWORDS_MISMATCH:
                    print("Passwords you entered do not match.")
                else:
                    print('Password should be at least 8 characters long.')
            
            while True:
                email = input("Email: ")
                if not email.isspace() or not email == None:
                    data.append(email)
                    break
            
            if self.context == Context.ON_SIGN_UP_ADMIN:
                print("\n Types 🔴 available: [1, 2, 3].\n 👊 They vary in permissions. ⭕")
                while True:
                    type_ = input("Choose admin type: ")
                    try:
                        type_ = int(type_)
                    except ValueError:
                        print("👩‍💻 Hmm, Please enter a digit.❌ Can you not see👀 from the available options 👆 above?")
                    else:
                        data.append(type_)
                        break
                
                return tuple(data)
            
            for _ in range(3):
                data.append(True)
            return tuple(data)

        elif self.context in (
            Context.ON_BLOCK_USER,
            Context.ON_UNBLOCK_USER,
            Context.ON_SEARCH_USER,
            Context.ON_DELETE_USER,
            Context.ON_SEARCH_ADMIN,
            Context.ON_DELETE_ADMIN):

            data = input("username: ")
            return data
        
        elif self.context == Context.ON_VERIFY_ACTION:
            data = input("Do you wish to proceed?_Y/N: ").upper()
            return data
        
        elif self.context == Context.ON_GET_TOKEN:
            data = input("Token🔑: ").strip()
            return data

    
    def handle_response(self, response):
        """ Handles common responses

        Args:
            response
            Type: InfoTypes
        """
        # handle access denied
        if response == it.ACCESS_DENIED:
            print("\n❌ Access Denied! 🔐🔐 ")  
        # handle user not found                        
        elif response == it.USER_NOT_FOUND:
            print("\n❌User not found❌. Please check the username you entered.")
        # handle no logged it admin                               
        elif response == it.NO_LOGGED_IN_ADMIN:
            print("\nImpossible!")
        # handle table not found
        elif response == it.TABLE_NOT_FOUND:
            print("\nExcuse me🙄? Database is dried up!")
        # handle invalid input
        elif response == it.INVALID_INPUT:
            print("\n❌Invalid input❌, can you not see👀 the menu?🤣😄")
        # handle login successful for admin
        elif response == it.LOGIN_ADMIN_SUCCESSFUL:
            self.context = Context.ON_ADMIN_DASH
        # handle login successful for user
        elif response == it.LOGIN_USER_SUCCESSFUL:
            self.context = Context.ON_DASH
        # handle account created successful response
        elif response == it.CREATE_ACCOUNT_SUCCESSFUL:
            print("\n Account👨‍💻 created successfully! ✅🤜")
        # handle username already exists response
        elif response == it.USERNAME_ALREADY_EXISTS:
            print("\n Hmm🤨, that's wierd! 🤖")
        # handle wrong token response
        elif response == it.WRONG_TOKEN:
            print("\n❌❌ Wrong token ❌❌! Are you sure you're the right admin?🤨")
        # handle action aborted response
        elif response == it.ACTION_ABORTED:
            print("\n3️⃣7️⃣ Action Aborted successfully.✅")
        # handle wrong psasword response
        elif response == it.WRONG_PASSWORD:
            print("\n 👀🤣 Incorrect Password. ❌")
        # handle wrong username response
        elif response == it.WRONG_USERNAME:
            print("\n❌ Wrong username 🙄")
        # handle no admins found response
        elif response == it.NO_ADMINS_FOUND:
            print("\n 🤔 I think there no other admins apart from you! 💞💞")
        # handle connection errors from verifier
        elif response == VerifyInfo.CONNECTION_FAILED:
            print("\n Ooops, Connection🔗 Failed!❌\n Check your connection.")
        # handle connection timed out
        elif response == VerifyInfo.CONNECTION_TIMED_OUT:
            print("\n Connection🔗 timed out.🕗\n Check your connection.")
        # handle user already blocked
        elif response == it.USER_ALREADY_BLOCKED:
            print("\n Umm, user has been already blocked🛑.🙄")
        # handle user already unblocked
        elif response == it.USER_ALREADY_UNBLOCKED:
            print("\n Damn!💥 This is a free user.🙂")
        
        # handle uncommon responses between processes
        else:
            return response


    def start(self):
        """
        Handles the start screen
        """
        if self.context == Context.ON_START:
            self.clear_screen()
            self.rich.print_welcome_panel(welcome_text)
            self.print_menu()
            self.prompt = input("\npylogin> ")
            if self.prompt == '1':
                self.context = Context.ON_LOGIN_ADMIN
            elif self.prompt == '2':
                self.context = Context.ON_SIGN_UP_ADMIN
            elif self.prompt == 'exit':
                exit(" Good Bye.")
            else:
                self.handle_response(it.INVALID_INPUT)
        else:
            pass
    

    def login(self):
        """
        Handles the login screen.
        """
        # check login type
        if self.context == Context.ON_LOGIN_USER:
            username, password = self._get_input_data() # get input data
            user = User() # a user object
            response = user.login_user(username, password) # try to login
            self.handle_response(response) # call self.handle_response to handle the response
            if user.logged_in_user:
                self.current_user = user
                self.clear_screen()
                self.print_menu()
            else: # go back to start screen
                self.context = Context.ON_START
        # if admin
        elif self.context == Context.ON_LOGIN_ADMIN:
            username, password = self._get_input_data() # get input data
            admin = Admin() # create an admin object
            response = admin.login_admin(username, password) # try to login
            self.handle_response(response) # call self.handle_response to handle the response
            if admin.logged_in_admin:
                self.current_admin = admin
                self.clear_screen()
                self.print_menu()
            else: # go back to start screen
                self.context = Context.ON_START

        else:
            pass

    def sign_up(self):
        """
        Handles the sign up screen or activity
        """
        # check account type
        if self.context == Context.ON_SIGN_UP_USER:
            # get input data
            data = self._get_input_data() # get input data
            user = User() # create a user object
            response = user.create_account(data) # get response
            self.handle_response(response) # call self.handle_response to handle the response
            self.context = Context.ON_START # go back
        # if admin
        elif self.context == Context.ON_SIGN_UP_ADMIN:
            data = self._get_input_data() # getting data
            admin = Admin() # create an admin object
            # get response
            response = admin.create_account(data) 
            self.handle_response(response) # call self.handle_response to handle the response
            self.context = Context.ON_START # go back


    def dashboard(self):
        """
        Handles the user dashboard screen
        """
        # check if it's time to work
        if self.context == Context.ON_DASH:
            # display a nice prompt with the name of the logged in user
            while True:
                self.prompt = input(f'\n{self.current_user.logged_in_user.username}@pylogin> ')
                if self.prompt == '1': # if option is 1 which is home,
                    response = self.current_user.get_home() # get home data
                    # handle any response apart from the data
                    if type(response) == it:
                        self.handle_response(response)
                    else:
                        data = response
                        self.clear_screen() # clear the screen
                        self.print_menu() # and print the menu
                        self.rich.print_home_data(data, home_logos[random.randint(0, 4)]) # finally the data print it out
                elif self.prompt == '2': # else if option is 2 which is my profile
                    response = self.current_user.get_profile() # get data on current user
                    # handle other reponses apart from the data
                    if type(response) == it:
                        self.handle_response(response)
                    else:
                        data = response
                        self.clear_screen() # clear the screen
                        self.print_menu() # and print the menu
                        # just pretty print it for now
                        self.rich.print_data_panel([data], profile_panel_user)
                # else if option is 3 which is logout
                elif self.prompt == '3':
                    self.current_user.logout() # logout from the user class
                    self.current_user = None # set current user to none
                    # 
                    self.context = Context.ON_START
                    break
                else:
                    self.handle_response(it.INVALID_INPUT)

    
    def admin_dashboard(self):
        """
        A method handler for admin_dahsboard
        """
        if self.context == Context.ON_ADMIN_DASH:
            admin = self.current_admin # set admin
            self.clear_screen() # clear the screen
            self.print_menu() # print menu
            while True:
                prompt = f"\n{admin.logged_in_admin.username}@pylogin> " # a nice prompt
                # set prompt
                self.prompt = input(prompt)
                if self.prompt == '1':
                    # get home
                    response = admin.get_all_users() # get response
                    if type(response) == it:
                        self.handle_response(response) # call response handler
                    else:
                        data = response
                        self.clear_screen()
                        self.print_menu()
                        self.rich.print_data_panel([user.data_to_dict() for user in data], profile_panel_user)
                elif self.prompt ==  '2':
                    # my profile
                    data = admin.logged_in_admin.data_to_dict() # get data on admin
                    self.clear_screen()
                    self.print_menu()
                    self.rich.print_data_panel([data], profile_panel_admin)
                elif self.prompt == '3': # administrative
                    self.context = Context.ON_ADMIN  # change context
                    break # break loop
                # logout
                elif self.prompt == '4':
                    admin.logged_in_admin = None # set logged in admin to none
                    self.current_admin = None # same for this class
                    self.context = Context.ON_START_ADMIN # change context and
                    # break loop
                    break
        else:
            pass

    
    def admin(self):
        """
        Handles the admin dashboard
        """
        if self.context == Context.ON_ADMIN:
            admin = self.current_admin # set admin
            _admin_options = [op.name.replace('_', ' ').title() for op in admin.show_permissions()] # get options
            _admin_options.append('Go Back') # a go back option to the previous screen
            self.option.set_admin_options(_admin_options)  # set admin options
            self.clear_screen()
            self.print_menu()
            while True:           
                prompt = f"\nadmin_{admin.logged_in_admin.username}@pylogin> " # a nice prompt
                # set the prompt and call self.set_option to redirect the option chosen
                self.prompt = self.index_option(input(prompt), admin.logged_in_admin.type)
                # now that we've got everything in place, let's write the option handlers
                if self.prompt == '1': # we know what to do
                    # that it option delete user
                    self.context = Context.ON_DELETE_USER
                    # print the menu
                    #self.print_menu()
                    self.delete_user() # call appropriate handler
                elif self.prompt == '2':
                    # option delete admin
                    self.context = Context.ON_DELETE_ADMIN
                     # print the menu
                    #self.print_menu()
                    self.delete_admin() # call appropriate handler
                # clear the database
                elif self.prompt == '3':
                    self.context = Context.ON_CLEAR_DB
                     # print the menu
                    #self.print_menu()
                    self.clear_db()  # call appropriate handler
                # see all users in then database
                elif self.prompt == '4':
                    # no needed context
                    # also can handle it here
                    #self.print_menu()  # print the menu
                    response = admin.get_all_users()
                    if type(response) == it:
                        # call response handler
                        self.handle_response(response)
                    else: # if it's the data
                        data = response
                        self.rich.print_data_panel([user.data_to_dict() for user in data], profile_panel_user)
                elif self.prompt == '5':
                    # option block user
                    #self.print_menu()  # print the menu
                    self.context = Context.ON_BLOCK_USER
                    self.block_user()  # call appropriate handler
                elif self.prompt == '6': # option unblock user
                    self.context = Context.ON_UNBLOCK_USER
                    #self.print_menu()  # print the menu
                    self.unblock_user() # call appropriate handler
                # option search user
                elif self.prompt == '7':
                    self.context = Context.ON_SEARCH_USER
                    #self.print_menu()  # print the menu
                    username = self._get_input_data() # get username
                    response = admin.search_user(username) # get response on search user
                    if type(response) == it:
                        # call response handler
                        self.handle_response(response)
                    else:
                        # if it's data
                        data = response
                        self.rich.print_data_panel([data.data_to_dict()], profile_panel_user)
                # option search for admin
                elif self.prompt == '8':
                    self.context = Context.ON_SEARCH_ADMIN
                    #self.print_menu()  # print the menu
                    username = self._get_input_data() # get username
                    response = admin.search_admin(username) # get response on search admin
                    if type(response) == it:
                        # call response handler
                        self.handle_response(response)
                    else:
                        # if it's data
                        data = response
                        self.rich.print_data_panel([data.data_to_dict()], profile_panel_admin)
                elif self.prompt == '9':
                    # no need for context
                    response = admin.get_users_count()
                    #self.print_menu()  # print the menu
                    if type(response) == it:
                        # call response handler
                        self.handle_response(response)
                    else:
                        # if it's data
                        data = response
                        print(f"\n {data} registered user(s) in database.") # print it
                # see all admins in the database
                elif self.prompt == '10':
                    # no need for context
                    response = admin.get_all_admins() # get reponse on get all admins
                    #self.print_menu()  # print the menu
                    if type(response) == it:
                        # call response handler
                        self.handle_response(response)
                    else:
                        # if it's data
                        data = response
                        self.rich.print_data_panel([user.data_to_dict() for user in data], profile_panel_admin)
                # get number of admins
                elif self.prompt == '11':
                    # and lastly no need for context
                    #self.print_menu()  # print the menu
                    response = admin.get_admins_count()
                    if type(response) == it:
                        # call response handler
                        self.handle_response(response)
                    else:
                        # if it's data
                        data = response
                        print(f"\n {data} registered admin(s) in database.") # print it
                # go back to admin dashboard
                elif self.prompt == '12':
                    self.clear_screen() # clear screen
                    self.context = Context.ON_ADMIN_DASH
                    break
                # clear screen
                elif self.prompt == 'cls':
                    self.clear_screen()
    
    def main(self):
        """
        The main application handler.
        """
        # Let's get started.
        self.context = Context.ON_START
        while True:
            if self.context == Context.ON_START:
                sleep(0.77)
                self.start()
            elif self.context in (Context.ON_LOGIN_ADMIN, Context.ON_LOGIN_USER):
                self.login()
            elif self.context in (Context.ON_SIGN_UP_ADMIN, Context.ON_SIGN_UP_USER):
                self.sign_up()
            elif self.context == Context.ON_DASH:
                self.dashboard()
            elif self.context == Context.ON_ADMIN_DASH:
                self.admin_dashboard()
            elif self.context == Context.ON_ADMIN:
                self.admin()
            else:
                self.context = Context.ON_START
            


main = Main()
main.main()
