from server.app import create_app

app = create_app({
    'SECRET_KEY': 'V6B3cCsuaMbbffrk',
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///store.db'
})

