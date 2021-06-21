from server.app import create_app

app = create_app({
    # OMG!!!! he posted the secret Key!1133!!!
    'SECRET_KEY': 'V6B3cCsuaMbbffrk',
    # local database storage
    'SQLALCHEMY_DATABASE_URI': 'sqlite:////data/store.db'
})
