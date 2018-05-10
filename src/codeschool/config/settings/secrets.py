import json
import os
import random
import string

from boogie.configurations import Conf

choice = random.SystemRandom().choice
data = {}


class SecretsConf(Conf):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        secrets_path = os.path.join(self.LOCAL_DIR, 'secrets.json')
        try:
            with open(secrets_path, 'r') as F:
                data = json.load(F)
                self.SECRET_KEY = data['secret-key']

        except (FileNotFoundError, KeyError) as e:
            print('Creating a new secrets file at local/secrets.json')

            chars = ''.join([string.ascii_letters, string.digits, string.punctuation])
            SECRET_KEY = ''.join([choice(chars) for i in range(50)])
            data['secret-key'] = SECRET_KEY

            with open(secrets_path, 'w') as F:
                json.dump(data, F)
