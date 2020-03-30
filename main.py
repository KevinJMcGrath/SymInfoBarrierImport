from os import system, name

import config
import ib_gen
import rsa_gen
import user_gen
import user_auth
import user_import

from symphony import BotClient

bot = BotClient(config.bot_config)
bot.session.authenticate()


def run_menu():
    exit_flag = False

    while not exit_flag:
        # None of these clear screen thigns work =/
        # clear_screen()
        choice = main_menu()

        if choice == "1":
            # add key pairs
            rsa_gen.generate_keypair_menu()
        elif choice == "2":
            # add parents, children, IB groups and policies
            create_insert_random_users()
        elif choice == "3":
            user_auth.authenticate_all_bot_users()
        elif choice == "98":
            # delete RSA keys
            if verify_input("Are you sure you want to delete all RSA key pairs in the database?"):
                rsa_gen.delete_all_keypairs()
        elif choice == "99":
            # delete user data
            if verify_input("Are you sure you wish to purge all user data?"):
                pass
        elif choice == "q":
            exit_flag = True
            print('Exiting')
        else:
            input("Invalid option. Press Enter to continue.")


def create_insert_random_users():
    random_user_dict = user_gen.generate_user_data()

    if random_user_dict:
        ib_gen.populate_existing_ib_policies(bot)
        ib_gen.populate_existing_ib_groups(bot, filter_prefix='scp')
        user_import.onboard_users(random_user_dict, bot)
    else:
        print('No user data was created, probably because you screwed soemthing up. Fix it and try again.')


def clear_screen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def verify_input(message: str):
    exit_flag = False

    while not exit_flag:
        verify = input(f"{message} (y/n)")
        if verify.lower() == "y":
            return True
        elif verify.lower() == "n":
            return False
        else:
            input("Invalid confirmation input. Estupido. Press Enter.")


def main_menu():
    prompt = '''
    Select option: 
        [1] Generate RSA key pairs
        [2] Insert users into Symphony
        [3] Authenticate users
        [98] Delete all RSA key pairs
        [99] Delete all user data
        [q] Quit        
    
    >>> '''

    return input(prompt)


if __name__ == "__main__":
    run_menu()