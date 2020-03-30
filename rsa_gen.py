import crypto.rsa as rsa
from database import rsa_db


def generate_keypair_menu():
    exit_flag = False

    while not exit_flag:
        count_input = input("How many keypairs do you want to create?")

        if count_input.isnumeric():
            count = int(count_input)
            if count <= 0:
                print("Fuck you, asshole.")
            elif count == 1:
                print("Generating single keypair...", end='')
                id = generate_rsa_keypair()
                print(f"done. Id: {id}")

                return id
            else:
                generate_rsa_keypair_sets(count)

            exit_flag = True
        elif count_input.lower() == 'q':
            exit_flag = True
        else:
            print('Come on, douchebag. Do it right. \n\n')


def generate_rsa_keypair():
    private_key, public_key = rsa.generate_rsa_key_pair(return_as_bytes=False)

    return rsa_db.insert_key_pair(private_key, public_key)


def generate_rsa_keypair_sets(num_pairs: int):
    id_list = []

    print(f'Generating {num_pairs} RSA key pairs...')
    for i in range(0, num_pairs - 1):
        print(f'{i + 1}...', end='')
        keypair_id = generate_rsa_keypair()
        id_list.append(keypair_id)
        print('done!')

    print('Done!')

    return id_list


def delete_all_keypairs():
    rsa_db.delete_all()
    print("All RSA keypairs deleted.")