class User():
    def __init__(self,
                 id,
                 account,
                 password,
                 name='buaaer',
                 email='111@111.com',
                 start='9:00',
                 end='21:00',
                 head_image='https://i.imgur.com/vUlftac.png') -> None:
        # 必要信息
        self.id = id
        self.account = account
        self.password = password
        # 非必要信息
        self.name = name
        self.email = email
        self.start = start
        self.end = end
        self.head_image = head_image  # 云端存储图像的url
