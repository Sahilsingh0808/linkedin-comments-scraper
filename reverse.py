import pandas as pd

# load the csv and user row 0 as headers
df = pd.read_csv("comments_data.csv", header=0)
df.dropna()

# reverse the data
df.iloc[::-1]

name=df['Name'].tolist()
heading = df['Profile Heading'].tolist()
email = df['Email'].tolist()
comment = df['Comment'].tolist()
name.reverse()
heading.reverse()
email.reverse()
comment.reverse()
df1 = pd.DataFrame(list(zip(name, heading, email, comment)), columns=['Name', 'Profile Heading', 'Email', 'Comment'])
                  
df1.to_csv('comments.csv', index=False)
