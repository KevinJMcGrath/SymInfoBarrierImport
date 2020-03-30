import config
import symphony.authenticate.auth_jwt as auth

from database import user_db, rsa_db


def authenticate_all_bot_users():
    base_url = f"{config.bot_config['auth_host']}:{config.bot_config['auth_port']}"
    for user in user_db.get_all_users():
        private_key, _ = rsa_db.get_key_pair(user.rsa_id)

        print(f'Authenticating {user.user_id}...', end='')
        try:
            session_token, km_token, _ = authenticate_bot_user(base_url, private_key, user.username)

            user_db.update_user_session(user.user_id, session_token, km_token)
            print('success!')
        except Exception as ex:
            print(f'failed. {ex}')


def authenticate_bot_user(base_url: str, private_key, bot_username):
    return auth.authenticate_bot_by_keystring(base_url, bot_username, private_key)