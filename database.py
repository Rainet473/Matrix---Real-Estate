from email_sender import *
from tkinter import messagebox

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

def register_user(user_type, name, mobile, email, aadhar, username, password, operating_area):
    '''Function Used for Registration of Agent/Buyer/Seller'''
    flag, message = 0, ""
    connection = establish_connection()
    curr = connection.cursor()
    
    try:
        curr.execute(f"Insert into {user_type} (name, phone_number, mail_id, unique_id, username, password, operating_area) values('{name}', {mobile}, '{email}', {aadhar}, '{username}', '{password}', '{operating_area}')" if user_type=='agents'
                    else f"Insert into {user_type} values({aadhar}, '{name}', {mobile}, '{email}')")
        curr.execute(f"Select * from {user_type} where unique_id = {aadhar}" if user_type=="agents"
                     else f"Select * from {user_type} where {user_type.rstrip('s')}_uid = {aadhar}")
        user_info = curr.fetchall()[0]
        try:
            if user_type=="agents":
                email_new_registration(user_type, email, user_info)
            else:
                email_new_registration(user_type, email, user_info, agent_assigned=agent_inf)
            connection.commit()
        except:
            messagebox.showerror("Error Sending Mail", "There has been a error in sending a confirmation mail.\n Make sure your internet connection is running.")
            return 4, ""
        if user_type=="agents":
            return 0, None
        else:
            return assign_customer(user_type, aadhar, name, mobile, email)
    except:
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
    '''Used to assign a new/existing customer with the logged in agent.'''
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
            curr.execute(f"Insert into {user_type.rstrip('s')}_assigned (agent_id, {user_type.rstrip('s')}_uid) values({agentid}, {aadhar})")
            email_assigned_customer(user_type, email, agent_inf[3], (aadhar, name, mobile, email), agent_inf, new= new)
            connection.commit()
            if new==False:
                return 2, f"{user_type.rstrip('s')} is already registered. He/She has been assigned to you.\nAn Email has been sent for confirmation."
            else:
                return 0, None
    else:
        return 1, ""
    
def list_assigned_customers(customer_type, agent_id=-1):
    '''Returns all the assigned customers with the mentioned agent id'''

    connection = establish_connection()
    curr = connection.cursor()
    if agent_id==-1:
        curr.execute(f"Select x.{customer_type.rstrip('s')}_uid, name from {customer_type} x join {customer_type.rstrip('s')}_assigned y on x.{customer_type.rstrip('s')}_uid = y.{customer_type.rstrip('s')}_uid where agent_id = {agentid}")
    else:
        curr.execute(f"Select x.{customer_type.rstrip('s')}_uid, name from {customer_type} x join {customer_type.rstrip('s')}_assigned y on x.{customer_type.rstrip('s')}_uid = y.{customer_type.rstrip('s')}_uid where agent_id = {agent_id}")
    
    assigned_customers = curr.fetchall()
    for i in range(len(assigned_customers)):
        assigned_customers[i] = f"{assigned_customers[i][1]}, {assigned_customers[i][0]}"
    
    return assigned_customers

def unassign_customer(customer_type, customer_uid):
    '''Unassigns a buyer/seller from the logged in agent'''

    connection = establish_connection()
    curr = connection.cursor()

    ##Removing available properties of sellers.
    if customer_type=="sellers":
        curr.execute(f"select DISTINCT amount_per_month from availability where (house_number, pincode) in (Select house_number, pincode from owns where seller_uid = {customer_uid}) and amount_per_month is NOT NULL")
        rent_costs = curr.fetchall()
        curr.execute(f"select DISTINCT selling_price from availability where (house_number, pincode) in (Select house_number, pincode from owns where seller_uid = {customer_uid}) and selling_price is NOT NULL")
        sale_costs = curr.fetchall()
        
        try:
            curr.execute(f"Delete from availability where (house_number, pincode) in (Select house_number, pincode from owns where seller_uid = {customer_uid})")
        except:
            messagebox.showerror("Error Unassigning", "There has been some error with unassigning the customer from the database.\nIt might be due to error in connection with the database.\nPlease try again later")   
            return 1
        
        ##Checking if there are no houses left with the prices of removed houses, If so then remove those prices as the table represents a weak entity..
           
        if len(rent_costs)!=0:
            for i in rent_costs:
                curr.execute(f"select * from availability where amount_per_month = {i[0]}")
                result = curr.fetchall()
                if len(result)==0:
                    curr.execute(f"Delete from rent_cost where amount_per_month = {i[0]}")
        
        if len(sale_costs)!=0:
            for i in sale_costs:
                curr.execute(f"select * from availability where selling_price = {i[0]}")
                result = curr.fetchall()
                if len(result)==0:
                    curr.execute(f"Delete from sale_cost where selling_price = {i[0]}")

    ##Removing from buyer/seller_assigned
    try:
        curr.execute(f"Delete from {customer_type.rstrip('s')}_assigned where {customer_type.rstrip('s')}_uid = {customer_uid}")
    except:
        messagebox.showerror("Error Unassigning", "There has been some error with unassigning the customer from the database.\nIt might be due to error in connection with the database.\nPlease try again later")
        return 1
    
    curr.execute(f"Select * from {customer_type} where {customer_type.rstrip('s')}_uid = {customer_uid}")

    email_unassigned_customer(customer_type, curr.fetchone(), agent_inf)
    connection.commit()
    return 0

def remove_available_property(house_number, pincode):
    '''This removes the mentioned property from the available table'''

    connection = establish_connection()
    curr = connection.cursor()

    curr.execute(f"select DISTINCT amount_per_month from availability where (house_number, pincode) = ('{house_number}', {pincode})")
    rent_costs = curr.fetchall()
    curr.execute(f"select DISTINCT selling_price from availability where (house_number, pincode) = ('{house_number}', {pincode})")
    sale_costs = curr.fetchall()

    try:
        curr.execute(f"Delete from availability where (house_number, pincode) = ('{house_number}', {pincode})")
    except:
        messagebox.showerror("Error Unassigning", "There has been some error with unassigning the customer from the database.\nIt might be due to error in connection with the database.\nPlease try again later")   
        return 1
    
    ##Checking if there are no houses left with the prices of removed houses, If so then remove those prices as the table represents a weak entity..
           
    if len(rent_costs)!=0:
        for i in rent_costs:
            curr.execute(f"select * from availability where amount_per_month = {i[0]}")
            result = curr.fetchall()
            if len(result)==0:
                curr.execute(f"Delete from rent_cost where amount_per_month = {i[0]}")
        
    if len(sale_costs)!=0:
        for i in sale_costs:
            curr.execute(f"select * from availability where selling_price = {i[0]}")
            result = curr.fetchall()
            if len(result)==0:
                curr.execute(f"Delete from sale_cost where selling_price = {i[0]}")
    
    curr.execute(f"Select mail_id from sellers where seller_uid = (select seller_uid from owns where (house_number, pincode) = ('{house_number}', {pincode}))")
    email_property_removed_to_owner(house_number, pincode, curr.fetchone()[0])
    connection.commit()
    return 0

def get_available_properties(agent_id = -1):
    '''This function returns all the available properties under the mention agent_id'''

    connection = establish_connection()
    curr = connection.cursor()

    curr.execute(f"select house_number, pincode from availability where (house_number, pincode) in (Select house_number, pincode from owns where seller_uid in (Select seller_uid from seller_assigned where agent_id = {agentid if agent_id==-1 else agent_id}))")
    properties = curr.fetchall()

    for i in range(len(properties)):
        properties[i] = f"{properties[i][0]}, {properties[i][1]}"
    
    connection.commit()
    return properties