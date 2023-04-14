from email_sender import *

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
    global agentid, agent_inf
    agent_inf = agent_info
    agentid = agent_info[0]

    return 0, None, agent_info

def register_user(user_type, name, mobile, email, aadhar, username, password, operating_area = "Garia, Kolkata"):
    '''Function Used for Registration of Agent/Buyer/Seller'''

    connection = establish_connection()
    curr = connection.cursor()
    
    try:
        curr.execute(f"Insert into {user_type} (name, phone_number, mail_id, unique_id, username, password, operating_area) values('{name}', {mobile}, '{email}', {aadhar}, '{username}', '{password}', '{operating_area}')" if user_type=='agents'
                    else f"Insert into {user_type} values({aadhar}, '{name}', {mobile}, '{email}')")
        curr.execute(f"Select * from {user_type} where unique_id = {aadhar}" if user_type=="agents"
                     else f"Select * from {user_type} where {user_type.rstrip('s')}_uid = {aadhar}")
        user_info = curr.fetchall()[0]

        if user_type=="agents":
            email_new_registration(user_type, email, user_info)
        else:
            email_new_registration(user_type, email, user_info, agent_assigned=agent_inf)
        connection.commit()
        if user_type=="agents":
            return 0, None
        else:
            return assign_customer(user_type, aadhar, name, mobile, email)
    except:
        flag, message = 0, ""

        if user_type=="agents":
            curr.execute(f"Select * from {user_type} where username = '{username}'")
            result = curr.fetchall()
            if len(result)!=0:
                flag, message = 1, "Username"
            curr.execute(f"Select * from {user_type} where operating_area = '{operating_area}'")
            result = curr.fetchall()
            if len(result)!=0:
                flag, message = 1, "Operating Area"
        else:
            flag, message = assign_customer(user_type, aadhar, name, mobile, email, new=False)

        if flag==1 and message == "":
            curr.execute(f"Select * from {user_type} where unique_id = {aadhar}" if user_type=="agents" 
                     else f"Select * from {user_type} where {user_type.rstrip('s')}_uid = {aadhar}")
            result = curr.fetchall()
            if len(result)!=0:
                flag, message = 1, "Aadhar Number"
    
            curr.execute(f"Select * from {user_type} where phone_number = {mobile}")
            result = curr.fetchall()
            if len(result)!=0:
                flag, message = 1, "Phone Number"
            
            curr.execute(f"Select * from {user_type} where mail_id = '{email}'")
            result = curr.fetchall()
            if len(result)!=0:
                flag, message = 1, "E-Mail ID"
        
        connection.commit()
    return flag, message

def assign_customer(user_type, aadhar, name, mobile, email, new=True):
    connection = establish_connection()
    curr = connection.cursor()
    
    ## Check if it is assigned.
    curr.execute(f"Select * from {user_type} where {user_type.rstrip('s')}_uid = {aadhar} and name = '{name}' and phone_number = {mobile} and mail_id = '{email}'")
    result = curr.fetchall()

    if len(result)!=0:
        curr.execute(f"Select * from {user_type.rstrip('s')}_assigned where {user_type.rstrip('s')}_uid = {aadhar}")
        result = curr.fetchall()
        if len(result)!=0:
            return 3, f"Username is already assigned to Agent_ID {result[0][0]}"
        ##Otherwise assign it to agent (Global Variable)
        else:
            curr.execute(f"Insert into {user_type.rstrip('s')}_assigned values({agentid}, {aadhar})")
            email_assigned_customer(user_type, email, agent_inf[3], (aadhar, name, mobile, email), agent_inf, new= new)
            connection.commit()
            if new==False:
                return 2, f"{user_type.rstrip('s')} is already registered. He/She has been assigned to you.\nAn Email has been sent for confirmation."
            else:
                return 0, None
    else:
        return 1, ""