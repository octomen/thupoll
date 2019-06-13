def test_connection(db_session):
    db_session.execute('SELECT 1;')
