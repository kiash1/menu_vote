### Disclaimer:
* I  keep env separate (maybe it will be private repo or somewhere secure we can access the variables from)

### User Registration:
* User registration here is a direct api call where the superuser submits the employee name and password.
* After the superuser creates the user with a username and password, the user can be logged in by requesting for 
a jwt token and using that to authenticate oneself as the organization's user where it is required to do so.


### Voting constraints:
I've assumed some of the constraints that wasn't explicitly mentioned in the requirements such as:
* retrieving a single object when asking for published vote results instead of a list.
* I'm putting an api to publish the results that any authenticated employee can access and publish since the superuser
might not be present at the organization and people will still be able to vote and decide.

### Getting Started:
* Clone the repository in to the directory and machine of choice.
* this is built on docker and docker-compose version 3 so make sure you have those 
necessary modules installed and running in your system.
* Start the application using: `make up-build`
* Run the tests using: `make test`
* Create a superuser to access admin panel using: `make createsuperuser` and follow the prompts.
* Go to: `http://0.0.0.0:8000` on your browser of choice to view the docs.
* Go to: `http://0.0.0.0:8000/admin` on your browser of choice to view the admin panel.