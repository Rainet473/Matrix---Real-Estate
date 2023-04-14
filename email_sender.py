import yagmail
sender_email = "arijeetpcloud@gmail.com"
password = "zzcmqcwvscfwwptk"
yag = yagmail.SMTP(user = sender_email,password=password)


def email_new_registration(user_type, mail_id, user_info, agent_assigned=()):
    '''This will be used as a confirmation email for the new registration'''

    subject = "Registration Successful"
    if user_type=='agents':
        contents = f"Welcome to the Matrix {user_info[1]}!\n\nYour Details are as follows:\nAgent ID: {user_info[0]}\nUsername: {user_info[5]}\nPassword: {user_info[6]}\nMobile: {user_info[2]}\n\nPlease keep the username and password to yourself and do not share this to anyone.\nWe send you our well wishes in your job.\n\n\nRegards.\nAdministrator\nMatrix - Real Estate"
    else:
        contents = f"Welcome to the Matrix {user_info[1]}!\n\nYou have been assigned to our agent:\nAgent ID: {agent_assigned[0]}\nName: {agent_assigned[1]}\nMobile: {agent_assigned[2]}\n\nFeel Free to contact our agent within the working hours (9:00 to 17:00)\nHope you enjoy our services.\n\n\nRegards.\nAdministrator\nMatrix - Real Estate."
    yag.send(mail_id,subject,contents)


def email_assigned_customer(user_type, customer_mail, agent_mail, customer_info, agent_info, new=False):
    '''This will be used to mail the agent and already existing customer(if present) for confirmation of assignment'''

    subject = "New Assignment"
    yag = yagmail.SMTP({sender_email: "Matrix - Real Estate"},password=password)
    contents = f"You have been assigned a new {user_type.rstrip('s')}.\n\n{user_type.rstrip('s')}'s Details are as follows:\nName: {customer_info[1]}\nMobile: {customer_info[2]}\nMail ID: {customer_info[3]}\n\n\n Regards.\nAdministrator\nMatrix - Real Estate"
    yag.send(agent_mail, subject, contents)

    if new==False:
        subject = "Agent Assigned"
        contents = f"Dear {customer_info[1].strip()[0]}!\n\nYou have been assigned to our agent:\nAgent ID: {agent_info[0]}\nName: {agent_info[1]}\nMobile: {agent_info[2]}\n\nFeel Free to contact our agent within the working hours (9:00 to 17:00)\nWe are glad to have you back!\n\n\nRegards.\nAdministrator\nMatrix - Real Estate."
        yag.send(customer_mail, subject, contents)
