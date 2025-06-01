Budget Tracker Web App.



I used Python Djnago as the backend and React.js as the frontend.

Database used is db-sqlite

To run my web app For backend go to the path in cmd and type "python manage.py runserver"
To run frontend go to the path in cmd and type "npm start"


to install dependencies for frontend use "npm install"




TEST USER LOGIN

username: admin
password: Admin@123


for creating a super user "python manage.py createsuperuser"

now enter username ,email and password

How the app works is,

First the user have to login

if successfully login then Will show the Dashboard. In the dashboard we can see Transactions,Budget Overview and summary

in Transactions it shows the transactions occurred and also can create transactions . The datetime will be choosen as the current datetime automatically when the entry is added.
we can filter the data by entering any key related to the item shown in the table


in Budget overview it lists the transactions occurred according to the year and month.
we can filter the data by entering any key related to the item shown in the table


in the summary the current month data is loaded when the dashboard is appeared and also we can filter the data according to the year and month

