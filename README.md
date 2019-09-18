# auth0_Solution_App

This sample python web application demonstrates usage of auth0 management API's to create a list of Rules for registered Applications in the auth0 account.

# Getting Started

* To run the sample, make sure you have python and pip installed.

* Log into your auth0 account, select Applications and click on Create application button.

* Select the Application type as Regular Web Application, click on Create. In the list of technologies available select Python. Rename you  application accordingly.

* Auth0 will open client application dashboard, on the dashboard client settings tab Register http://localhost:3000/callback as Allowed Callback URLs and http://localhost:3000 as Allowed Logout URLs.

# Additional configurations

* Since the application uses management APIs to list rules and clients. We need to provide authorization to be able to generate access  tokens for the API.

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
```
https://github.com/sidharth240887/auth0_Solution_App.git
```
* Rename .env.Sample in sample application to .env and populate it with the client ID, domain, secret, callback URL and audience for your Auth0 app.

* Run pip install -r requirements.txt to install the dependencies

* Run python server.py, in the application folder.The app will be served at http://localhost:3000/. 
![login page](/images/Login_Page.PNG)

* Once login is clicked, user will be redirected to auth0 authication page. 
  * If the user is authorized to access application following page will be displayed
 ![Dashboard](/images/dashboard.PNG)
  * If the user is not authorized following page will be displayed
 ![Unauthorised](/images/Unauthorised.PNG)
 
* On the dashboard page, user can click **APPRULE** to get rules associated with all the application
![ClientApprule](/images/Application_Rule_Display.PNG)

# Application code details:

```auth0_Solution_App``` Application objective is to display a set of rules applied for each application. Since rules
and applications do not have a direct relationship, Rules are parsed to check for application name and id in 
order to establish which rules are applied to which application.

This code logic is implemented in file ```manageapi.py```

**Algorithm:**
* Get a list of applications and rules using the auth0 management APIs
* For each application parse all the rules to check for following conditions:
	* If rule contains application name or id, add the rule to the application
	* If rule contains not condition(!==) for the application name or id, do not add
	  rule for the application. This rule will be applicable for rest of the applications, 
	  hence will be added to them.
	* If rule has no application id or name, it will be added to all the applications.

**Application Flow details:**

When user hits the **/home** page, is prompted for a Log in. After Login is clicked, user is redirected to 
auth0 authentication page. If the user is authorised to access the application, and successfuly authenticates
user is redirected to **/dashboard** page with user information. 
Else if user is unauthorised, user is redirected to **/unauthorised** page with error details displayed.

User authorisation is checked using rule in the authentication pipeline, which whitelists allowed users.

Once user is in **/dashboard** page, user can click on AppRules button to display list of Rules for each 
Application on **/appruledisplay** page. 








