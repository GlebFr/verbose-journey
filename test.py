from datetime import datetime

def check_data(message):
    try:
        user_data = datetime.strptime(message, '%d.%m.%Y').date()
        now_data = datetime.now().date()
        if user_data > now_data:
            return True
        else:
            return False


    
    except ValueError:
        return False
    


print(check_data('jdigjaoi'))
