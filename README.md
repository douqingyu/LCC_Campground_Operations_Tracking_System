# Lincoln Community Campground (LCC) Issue Tracker

## Getting Started

Here's how to get the Issue Tracker up and running:

1. Make sure you have Python and PostgreSQL installed on your computer.

2. Get a copy of the code by downloading it or using Git.

3. Create a virtual environment:
   ```
   python -m venv .venv
   ```

4. Activate your virtual environment:
   - On Windows: `.venv\Scripts\activate`
   - On Mac/Linux: `source .venv/bin/activate`

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

6. Set up the database:
   ```
   psql -U postgres -c "CREATE DATABASE lcc_issue_tracker;"
   psql -U postgres -d lcc_issue_tracker -f create_database.sql
   psql -U postgres -d lcc_issue_tracker -f populate_database.sql
   ```

7. Update the database connection in `lccapp/connect.py` to match your PostgreSQL settings.

8. Run the application:
   ```
   python run.py
   ```


## Using the System

### For Visitors

So you've found an issue at the campground and want to report it? Great! After logging in with your visitor account, click on "Report Issue" in the navigation bar. Fill in a clear title (like "Broken faucet at campsite #42") and provide details about the problem. The more specific you are, the easier it will be for our staff to fix it.

Once you've reported an issue, you can check its status anytime by clicking "My Reported Issues" from your dashboard. You'll see if it's new, being worked on, temporarily stalled, or resolved. Feel free to add comments if you remember additional details or want to say thanks when it's fixed!

### For Helpers

As a helper, you're the one who makes the magic happen! When you log in, you'll see all active issues on your dashboard, sorted by status. New issues appear at the top, so you can quickly spot what needs attention.

When you start working on an issue, change its status from "New" to "Open" using the status dropdown. This lets everyone know someone is on the case. If you need more information or you're waiting for parts, change it to "Stalled." Once you've solved the problem, mark it as "Resolved" with a comment about what you did to fix it.

You can view all the details of any issue by clicking the "View" button. This shows you the full description, all comments, and lets you add updates for the visitor who reported it.

And hey, if you happen to notice an issue yourself while working, you can report it just like a visitor would through your own dashboard.

### For Administrators

As an admin, you have all the powers of a helper plus some extra responsibilities. You can manage user accounts by clicking "Manage Users" from your dashboard. From there, you can change user roles (maybe promote a reliable visitor to helper status), activate or deactivate accounts, and generally keep things running smoothly.

You also have oversight of all issues in the system. Your dashboard shows everything currently active, and you can step in to reassign or update any issue as needed.

## How Issues Flow Through the System

We've designed a simple workflow for issues to make tracking easy. Every issue starts as "New" when it's first reported. This means it's waiting for initial review.

When a helper or admin starts working on the issue, they'll change the status to "Open." This means someone is actively addressing the problem.

Sometimes, issues hit a roadblock - maybe we need more information from the reporter, or we're waiting for replacement parts. In these cases, the status changes to "Stalled." This isn't forgotten; it's just temporarily on hold.

Finally, when the issue is fixed, it becomes "Resolved." The issue remains in the system for reference, but it's no longer shown in the active issues list.

## About Security

We take security seriously! We never store your actual password in our database. Instead, we use a secure technique called "hashing" with the bcrypt algorithm. This transforms your password into a scrambled string that can't be reversed, even if someone somehow accessed our database.

When you log in, we take the password you type, apply the same transformation, and check if it matches what we have stored. This way, we can verify your identity without ever storing your actual password.

Each password also gets its own unique "salt" - a random value that makes it impossible for attackers to use pre-computed tables to crack passwords, even if they're common ones. These security features help keep your account safe.

## Hitting a Snag?

If you run into problems getting the system running, here are some common issues and how to fix them:

Having trouble connecting to the database? Make sure PostgreSQL is running and check that the username, password, and database name in connect.py match your setup.

Getting import errors when starting the application? Ensure your virtual environment is activated and all packages are installed correctly with `pip install -r requirements.txt`.

Issues with file uploads? Check that the static/uploads directory exists and has the right permissions.

Can't log in? If you're using sample data, try the credentials from populate_database.sql. For a fresh installation, you'll need to register a new account first.

## Making It Your Own

Want to customize the application? The project is organized to make this straightforward. All the HTML templates are in the lccapp/templates directory, and static files like CSS are in lccapp/static.

The Python code is organized by functionality: admin.py for administrator features, helper.py for helper features, visitor.py for visitor features, and so on. This makes it easy to find and modify specific aspects of the system.

If you need to change the database structure, update create_database.sql and then modify the corresponding queries in the Python files.

When you're ready to deploy the application in a production environment, you'll want to switch from the built-in Flask server to something more robust like Gunicorn, set up proper database backups, and configure HTTPS for security.

Now go ahead and start tracking those campground issues! Happy camping!