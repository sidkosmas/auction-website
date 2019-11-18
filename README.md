# Django Tutorial

1 - Installation<br>
2 - First Steps<br>
3 - The modal layer<br>
4 - The view layer<br>
5 - The template layer<br>
6 - Forms<br>
7 - The development process<br>
8 - The admin<br>
9 - Security<br>

Sources<br>

* https://docs.djangoproject.com/en/1.7/howto/static-files/#configuring-static-files
* https://www.b-list.org/weblog/2006/sep/10/django-tips-laying-out-application/
* https://www.tutorialspoint.com/django/
* https://djangobook.com/

Required modules:

pip install Django
pip install Pillow
pip install docutils

# Next

#### Change model name User to UserDetails

	$ manage.py makemigrations
	Did you rename the website.User model to UserDetails? [y/N] y
	Migrations for 'website':
	  website\migrations\0002_auto_20191118_1400.py
		- Rename model User to UserDetails

You will get the following error:
	
	django.db.utils.NotSupportedError: Renaming the 'website_user' table while in a transaction
	is not supported on SQLite < 3.26 because it would break referential integrity. 
	Try adding `atomic = False` to the Migration class.

Why ?? https://stackoverflow.com/questions/48549068/django-db-utils-notsupportederror-in-sqlite-why-not-supported-in-sqlite

Open website/migrations/0002_auto....py
append in class Migration

	atomic = False
	
	
	$ manage.py migrate
	Operations to perform:
	  Apply all migrations: admin, auth, contenttypes, sessions, website
	Running migrations:
	  Applying website.0002_auto_20191118_1400... OK

	$ manage.py runscript do_migrations --script-args copyDataFromUserDetails
--------------------------	
	https://django-extensions.readthedocs.io/en/latest/runscript.html

	INSTALLED_APPS = [
		'website',
		...
		'django_extensions'
	]

	def run():	#Without arguments
		...

	def run(*args):		#With arguments
		...
----------------------------------------------------------------------------

#### Remove fields username, password, email and add field user_id

	user_id = models.IntegerField()

	$ manage.py makemigrations
	You are trying to add a non-nullable field 'user_id' to userdetails without a default; we can't do that (the database needs something to populate existing rows).
	Please select a fix:
	 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
	 2) Quit, and let me add a default in models.py
	Select an option: 2

	user_id = models.IntegerField(null=True)

	$ manage.py makemigrations
	Migrations for 'website':
	  website\migrations\0003_auto_20191118_1406.py
		- Remove field email from userdetails
		- Remove field password from userdetails
		- Remove field username from userdetails
		- Add field user_id to userdetails
		
	$ manage.py migrate
	Operations to perform:
	  Apply all migrations: admin, auth, contenttypes, sessions, website
	Running migrations:
	  Applying website.0003_auto_20191118_1406... OK
  
	$ manage.py runscript do_migrations --script-args setUserIDs

Now that each UserDetails record has user_id populated (not null) we will change the field to be 
Foreign Key

	$ manage.py makemigrations
	You are trying to change the nullable field 'user_id' on userdetails to non-nullable without a default; we can't do that (the database needs something to populate existing rows).
	Please select a fix:
	 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
	 2) Ignore for now, and let me handle existing rows with NULL myself (e.g. because you added a RunPython or RunSQL operation to handle NULL values in a previous data migration)
	 3) Quit, and let me add a default in models.py
	Select an option: 2
	Migrations for 'website':
	  website\migrations\0004_auto_20191118_1537.py
		- Alter field user_id on userdetails
	
	$ manage.py migrate
	Operations to perform:
	  Apply all migrations: admin, auth, contenttypes, sessions, website
	Running migrations:
	  Applying website.0004_auto_20191118_1537... OK

