import yagmail
sender_email = "arijeetpcloud@gmail.com"
password = "zzcmqcwvscfwwptk"
yag = yagmail.SMTP({sender_email: "Matrix - Real Estate"},password=password)


def email_new_registration(user_type, mail_id, user_info, agent_assigned=()):
    '''This will be used as a confirmation email for the new registration'''

    subject = "Registration Successful"
    user_name = (user_info[1].split(" "))[0]
    if user_type=='agents':
        contents = f"Welcome to the Matrix {user_name}!\n\nYour Details are as follows:\nAgent ID: {user_info[0]}\nUsername: {user_info[5]}\nPassword: {user_info[6]}\nMobile: {user_info[2]}\n\nPlease keep the username and password to yourself and do not share this to anyone.\nWe send you our well wishes in your job.\n\n\nRegards.\nAdministrator\nMatrix - Real Estate"
    else:
        contents = f"Welcome to the Matrix {user_name}!\n\nYou have been assigned to our agent:\nAgent ID: {agent_assigned[0]}\nName: {agent_assigned[1]}\nMobile: {agent_assigned[2]}\n\nFeel Free to contact our agent within the working hours (9:00 to 17:00)\nHope you enjoy our services.\n\n\nRegards.\nAdministrator\nMatrix - Real Estate."
    yag.send(mail_id,subject,contents)


def email_assigned_customer(user_type, customer_mail, agent_mail, customer_info, agent_info, new=False):
    '''This will be used to mail the agent and already existing customer(if present) for confirmation of assignment'''

    subject = "New Assignment"
    yag = yagmail.SMTP({sender_email: "Matrix - Real Estate"},password=password)
    contents = f"You have been assigned a new {user_type.rstrip('s')}.\n\n{user_type[0].upper()}{user_type.rstrip('s')[1:]}'s Details are as follows:\nName: {customer_info[1]}\nMobile: {customer_info[2]}\nMail ID: {customer_info[3]}\n\n\n Regards.\nAdministrator\nMatrix - Real Estate"
    yag.send(agent_mail, subject, contents)

    if new==False:
        subject = "Agent Assigned"
        customer_name = (customer_info[1].split(" "))[0]
        contents = f"Dear {customer_name}!\n\nYou have been assigned to our agent:\nAgent ID: {agent_info[0]}\nName: {agent_info[1]}\nMobile: {agent_info[2]}\n\nFeel Free to contact our agent within the working hours (9:00 to 17:00)\nWe are glad to have you back!\n\n\nRegards.\nAdministrator\nMatrix - Real Estate."
        yag.send(customer_mail, subject, contents)

def email_unassigned_customer(user_type, customer_info, agent_info):
    '''This is used to mail the customer who has been unassigned from the agent.'''

    subject = "Unassigned Successfully"
    customer_name = (customer_info[1].split(" "))[0]

    contents = f"Dear {customer_name},\nYou have been successfully unassigned from our agent ({agent_info[1]}).\nWe hope you reach back to us again whenever you are to buy/rent/sell any properties.\n\n\nBest Wishes\nAdministrator\nMatrix - Real Estate"
    yag.send(customer_info[3], subject, contents)

def email_property_removed_to_owner(house_number, pincode, customer_info):
    '''This is used to mail the owner of the property that it has been removed from the available section.'''

    subject = "Property Availablity Removed"
    customer_name = (customer_info[1].split(" "))[0]
    
    contents = f"Dear {customer_name},\nYour property (House Number: {house_number}, Pincode: {pincode}) has been successfully removed from the available section.\nWe hope you contact our agents again whenever you want to add a property.\n\n\nRegards\nAdministrator\nMatrix - Real Estate"
    yag.send(customer_info[3], subject, contents)
    
def email_added_property(customer_info, property_info):
    '''This will mail the seller that the information has been added/updated in the database'''

    subject = "Property Added"
    customer_name = (customer_info[1].split(" "))[0]

    contents = f"Dear {customer_name},\nYour property has been added/updated in the database.\nYour property details are as follows:\n\nHouse Number: {property_info[0]}\nStreet: {property_info[1]}\nCity: {property_info[2]}\nLocality: {property_info[3]}\nPincode: {property_info[4]}\nArea(in sqft.): {property_info[5]}\nBedrooms: {property_info[6]}\nYear of Construction: {property_info[7]}\n\nFeel Free to contact your agent if any information is incorrect. We are glad to have you use our services.\n\n\nRegards\nAdministrator\nMatrix - Real Estate"
    yag.send(customer_info[3], subject, contents)
    