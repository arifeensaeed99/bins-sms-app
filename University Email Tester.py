import requests

def is_uni_email(email):

    # Start traversing the string
    for i in range(len(email)):
 
        if (email[i] == '@'):
            break
 
    domain = email[i+1: len(email)]

    # print(domain)

    # Send a request to Universities HipoLabs for a domain search, use Get Request and Len of Json
    uni_email = requests.get("http://universities.hipolabs.com/search?domain=" + str(domain))

    # print(uni_email.json())

    if len(uni_email.json()):
        #print('Data is here')
        return True
    else:
        #print('No data here')
        return False

print(is_uni_email('michaelsanchez@oxford.ac.uk'))
    



 