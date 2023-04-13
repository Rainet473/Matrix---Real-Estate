def establish_connection(host = '127.0.0.1', user = 'root', passwd = 'spiderman473', database= 'matrix_real_estate'):
    '''Establishes connection with local database, throws exception(not error) if connection not established'''
    import mysql.connector as cntr
    from mysql.connector import Error
    connection = None
    try:
        connection = cntr.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
            )

        return connection

    except Error as e:
        return f'An error occured : {e}'
    
def login_agent(username, password):
    '''Function used to login the agent into the GUI'''
    connection = establish_connection()
    curr = connection.cursor()

    curr.execute(f"select * from agents where username = '{username}'")
    agent_info = curr.fetchall()
    connection.commit()

    if len(agent_info)==0:
        return 1, "Invalid Username!", agent_info
    else:
        agent_info = agent_info[0]
        if agent_info[6] != password:
            return 1, "Invalid Password!", agent_info
    
    return 0, None, agent_info