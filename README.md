# auth0_Solution_App

This sample python web application demonstrates usage of auth0 management API's to create a list of Rules for registered Applications in the auth0 account.

# Getting Started

* To run the sample, make sure you have python and pip installed.

* Log into your auth0 account, select Applications and after click on Create application button.

* Select the Application type as Regular Web Application, click on Create. In the list of technologies available select python. Rename you  app accordingly.

* Auth0 will open client application dashboard, on the dashboard client settings tab Register http://localhost:3000/callback as Allowed Callback URLs and http://localhost:3000 as Allowed Logout URLs.

# Additional configurations

* Since the application uses management APIs to list rules and clients. We need to provide authorization to be able to generate access t tokens for the API.

* Select APIs tab, next select Auth0 Management API. Click on Machine to Machine Applications tab. In this section you will see a list Applications. Select your Sample App and toggle to Authorized. Additionaly you need to expand the same row to get the list of scopes that should be granted to this client.

* Please select only read:clients and read:rules scope in order to allow limited access. Click on UPADTE button below and settings are saved.

# Rules to be applied

* This Sample application will whitelist users based on email address. So that only authorized users are able to access the application.
Below is the sample rule to achieve the above objective.

```
function (user, context, callback) {

  if(context.clientName === 'Solution_App'){
    // authorized users
	  const whitelist = [ 'solutionApp.user1@example.com','solutionApp.user2@example.com']; 
	  const userHasAccess = whitelist.some(function (email) {
    return email === user.email;
    });    
    if (!userHasAccess) {
      return callback(new UnauthorizedError('Email Access denied.'));
    }
  }
callback(null, user, context);
} 
```
# Running the auth0_Solution_App

* Download the source code from below link:

* Rename .env.example in sample application to .env and populate it with the client ID, domain, secret, callback URL and audience for your Auth0 app.

* Run pip install -r requirements.txt to install the dependencies

* Run python server.py, in the application folder.The app will be served at http://localhost:3000/. 
![login page](/images/Login_Page.png)

* Once login is clicked, user will be redirected to auth0 authication page. 
  * If the user is authorized to access application following page will be displayed
![Dashboard](/images/dashboard.png)
  * If the user is not authorized following page will be displayed
 ![Unauthorised](/images/Unauthorised.png)
 
* On the dashboard page, user can click **APPRULE** to get rules associated with all the application
![ClientApprule](/images/Application_Rule_Display.png)

# Application code details:

Application has been implemented to handle unauthorised access



