from utils.db_utils.base_db import Database

# Global key variables
hostname = 'localhost'
port_num = 3306
username = 'root'
password = ''
db_name = 'sentiment_db'

# Connectting to user
sentiment_db = Database(host=hostname, port=port_num, user=username, passwd=password, db=db_name)
sentiment_db.connect()

user_social = sentiment_db.fetch_all(select='birthday, about, emails, city, country, category, description, user_id', from_clause='user_social',data_as_dataframe=True)

# About and Description coulms tokenization and categorization
from utils.text_processing_utils.categoryCalculation import CategorySimilarity
cat_sim = CategorySimilarity()

user_social[' about'] = user_social[' about'].apply(lambda x: cat_sim.getStringCategory(x))

user_social[' description'] = user_social[' description'].apply(lambda x: cat_sim.getStringCategory(x))

# Email feature parsing
def getEmailType(email):
    if email == None:
        return email
    
    i = email.index('@')    
    email_type = email[i+1:]
    i = email_type.index('.')
    
    return email_type[:i]

user_social[' emails'] = user_social[' emails'].apply(getEmailType)

# Birthday column parse and split into three separate columns: day, month and year
user_social['day'] = user_social['birthday'].apply(lambda x: int(x.split('/')[0]) if x is not None else None)
user_social['month'] = user_social['birthday'].apply(lambda x: int(x.split('/')[1]) if x is not None else None)
user_social['year'] = user_social['birthday'].apply(lambda x: int(x.split('/')[2]) if x is not None else None)

# Saving preprocessed dataset
# user_social.to_csv('user_social_new.csv', sep='\t', encoding='utf-8')
