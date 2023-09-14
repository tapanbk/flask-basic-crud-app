# Flask Documentation

## Install Flask
```shell
pip install Flask
```

## Tutorials for Flask
https://www.tutorialspoint.com/flask/index.htm




## install flash-sqlalchemy
```shell
pip install flask-sqlalchemy
```


## Tutorials for Relationship
https://www.digitalocean.com/community/tutorials/how-to-use-many-to-many-database-relationships-with-flask-sqlalchemy


## Run the Flask in shell
```shell
flask shell
```


## Run the below code in the shell to create the database
```shell
  db.create_all()
```

## Run the below code in the shell to drop the database
```shell
  db.drop_all()
```

## Documentation url for sqlalchemy
https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/



## install flask-bcrypt
```shell
pip install flask-bcrypt
```

## Documentation for Flask bcrypt
https://www.geeksforgeeks.org/password-hashing-with-bcrypt-in-flask/

## Run the Flask in debug mode
```shell
flask --app app run --debug
```

or  
```shell
python app.py
```

### Get all the data
```shell
users = User.query.all()

```

###  save to database
```shell

user = User(**form)
db.session.add(user)
db.session.commit()

```


### filter the data
```shell
user = User.query.filter_by(id= userId).first()
OR
user = db.get_or_404(User, userId)
```

### delete data
```shell
user_instance = db.get_or_404(User, userId)
db.session.delete(user_instance)
db.session.commit()
```


### Get or 404 
```shell
user = User.query.get_or_404(user_id)
```



### Get the Users and their Posts
```shell
from app import User

users = User.query.all()

for user in users:
    print(user.email)
    print(user.posts)
```


### Get the users,their posts anc loop
```shell
from app import User

users = User.query.all()
for user in users:
    print('Email: ', user.email)
    print('-')
    print('posts:')
    for post in user.posts:
        print('>', post.content)
    print('-'*30)

```


### Create the multiple group at once
```shell
teacher = Group(name="Teacher", description="Teacher Group")
student = Group(name="Student", description="Student Group")
db.session.add_all([teacher, student])
db.session.commit()
```

### Add group to the user
```shell
user1 = User.query.get_or_404(1)
group_user = GroupUser(user_id=user1.id, group_id=teacher.id)
db.session.add(group_user)
db.session.commit()
```

### Add group to the user
```shell
user = User.query.get_or_404(1)
group_ = Group.query.get_or_404(1)
user.groups.append(group)
db.session.commit()
```