import utility

from database import rsa_db
from models.user import NewUserData


def generate_user_data():

    company_count = company_count_menu()
    if company_count < 1:
        return []

    users_per_company = users_per_company_menu()
    if users_per_company < 1:
        return []

    # get a list of unreserved keypair ids from database
    keypair_ids = rsa_db.get_unreserved_keypair_ids()
    if not keypair_count_check(company_count, keypair_ids):
        input("Press Enter to continue")
        return []

    # create users
    random_user_dict = {}
    for i in range(company_count):
        user_list = []
        keypair_id = keypair_ids[i]
        _, pubkey = rsa_db.get_key_pair(keypair_id)

        parent_user = gen_random_parent_user(keypair_id, pubkey)
        user_list.append(parent_user)

        for j in range(users_per_company):
            user_list.append(gen_random_child_user(parent_user))

        dict_key = parent_user.username
        random_user_dict[dict_key] = user_list

    return random_user_dict


def gen_random_parent_user(keypair_id: str, public_key: str):
    return gen_random_user_attributes(keypair_id, public_key)


def gen_random_child_user(parent_user):
    return gen_random_user_attributes(parent_user)


def gen_random_user_attributes(keypair_id: str = None, public_key: str = None, parent_user=None):
    user = NewUserData()
    user.first_name = utility.get_random_string().title()
    user.last_name = utility.get_random_string(7, 14).title()
    user.username = f'scp_{user.first_name}_{user.last_name}_{utility.rand_number_n_digits(6)}'

    if parent_user:
        user.domain = parent_user['domain']
        user.parent_username = parent_user['username']
        user.keypair_record_id = parent_user['keypair_id']
        user.rsa_public_key = parent_user['pubkey']
    else:
        user.domain = utility.get_random_string(3, 8) + ".com"
        user.parent_username = None
        user.keypair_record_id = keypair_id
        user.rsa_public_key = public_key

    user.email = f'{user.first_name}.{user.last_name}@{user.domain}'

    return user


def keypair_count_check(company_count, keypair_ids):
    keypair_count = 0
    if keypair_ids:
        keypair_count = len(keypair_ids)

    if keypair_count < company_count:
        print(f'ERROR: Requested company count was {company_count}; available keypairs: {keypair_count}')
        return False

    return True


def company_count_menu():
    while True:
        count_input = input('How many "companies" do you want to create?')
        if count_input.isnumeric():
            count = int(count_input)
            if count <= 0:
                print("Fuck you, asshole.")
            else:
                return count
        elif count_input.lower() == 'q':
            return -1
        else:
            print('Come on, douchebag. Do it right. \n\n')


def users_per_company_menu():
    while True:
        count_input = input('How many users per company')
        if count_input.isnumeric():
            count = int(count_input)
            if count <= 0:
                print("Fuck you, asshole.")
            else:
                return count
        elif count_input.lower() == 'q':
            return -1
        else:
            print('Come on, douchebag. Do it right. \n\n')