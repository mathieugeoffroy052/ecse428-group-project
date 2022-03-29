#Getting Started
1. pip install -r 'requirements.txt'
2. python manage.py migrate
3. python manage.py runserver
#Authentication
To access any backend endpoint that requires the user to be authenticated, you need to do the following:
1. Send a POST request to /accounts/login with a JSON body like the following <br />
`{ username: "youremail@email.com", password: "yourpassword" }`
2. If the login was successful, you will receive a response like the following <br />
`{ expiry: "a datetime string", token: "aLongAndRandomLookingString", has_seen_tutorial: "you can ignore this for now" }`
3. From now until the expiry of the token you just received you can access any endpoint as the authenticated user by adding a header to your request like this one: Authorization: Token thatSameRandomLookingStringYouReceivedEarlier
If you don't include the header your request looks unauthenticated to the backend. If your token has expired, you'll get a different error message telling you that the token is no longer valid or something along those lines.

#Testing
##Unit tests
python manage.py test
##Behavioural tests
TODO
#Formatting
before pushing, remember to format with `black .`