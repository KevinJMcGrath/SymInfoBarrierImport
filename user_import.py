from typing import List

import ib_gen

from database import user_db, rsa_db
from symphony import BotClient
from utility import timeit
from models.user import NewUserData


def onboard_users(user_dict: dict, bot_client: BotClient):
    for group_name, user_list in user_dict.items():
        print(f'Inserting Symphony data for group {group_name}...')
        # create IB group
        ib_group_id = ib_gen.create_ib_group(group_name, bot_client)

        # Onboard users
        user_ids = insert_users(user_list, bot_client)

        # Add users to IB group
        ib_gen.add_users_to_ib_group(ib_group_id, user_ids, bot_client)

        # Add IB Policies
        ib_gen.create_all_policy_combinations(ib_group_id, bot_client)


# @timeit
def insert_users(user_list: List[NewUserData], bot_client: BotClient):
    p_id = None

    sym_user_id_list = []
    for user in user_list:
        # Insert new user into Symphony
        sym_user = bot_client.User.create_service_user(user.first_name, user.last_name, user.email,
                                                       user.username, user.company_name, user.rsa_public_key)

        user_id = sym_user['userSystemInfo']['id']
        parent_id = None

        # establish parent_id
        if not p_id:
            p_id = user_id
        else:
            parent_id = p_id

        sym_user_id_list.append(user_id)

        # Insert new user into database
        user_db.insert_user_session(user_id, None, None, user.keypair_record_id, user.username, parent_id)
        # Reserve rsa keypair
        rsa_db.reserve_key_pair(user.keypair_record_id)

    return sym_user_id_list

# for each company requested, do the following:
# 1. create the parent user in symphony
# 2. add parent user to database
# 3. for each user_per_company, create user in symphony
# 4. add each user_per_company to database
# 5. get list of all existing IB groups on pod
# 6. create IB group for each parent user (name "cusc_" + {parent_user_id})
# 7. add parent and all children to IB group
# for each new IB group:
# 8. add IB policy for each group id in existing list
# 9. add IB group to existing IB group list
# 10. goto 8.