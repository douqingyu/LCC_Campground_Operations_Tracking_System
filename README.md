# Lincoln Community Campground Issue Tracker
# Setup and Usage Guide

This guide will show you how to set up and use the Lincoln Community Campground (LCC) Issue Tracker application.

## System Requirements

Before you begin, you'll need Python 3.8 or higher, MySQL 5.7 or higher, a modern web browser, and an internet connection for downloading packages.

## Setting Up the Application

1. **Obtain the code**
   - Clone the repository or download and extract the ZIP file to your computer

2. **Set up Python environment**
   - Open a terminal platforms such as VS Code and navigate to the project directory
   - Create a virtual environment
   - Activate the virtual environment
   - Install required packages

3. **Set up the database**
   - Ensure MySQL Workbench server is running
   - Enter your MySQL Workbench root password
   - Create the database named lcc
   - Populate with database

4. **Configure database connection**
   - Create `connect.py` in lccapp
   - Set the connection parameters:
     ```python
     dbuser = "root"          # Your MySQL username
     dbpass = "your_password" # Your MySQL password
     dbhost = "localhost"     # Database server address
     dbport = "3306"          # MySQL port
     dbname = "lcc"           # Database name
     ```

5. **Launch the application**
   - With your virtual environment activated, run: `python run.py`
   - Open a web browser and navigate to http://127.0.0.1:5000

## Using the Application

The Issue Tracker has three different user roles: Visitors, Helpers, and Administrators. Each role has different capabilities within the system.

### Using the System as a Visitor

As a visitor to the campground, once logged in, you'll see your Visitor Dashboard showing all your reported issues, each with a status indicator: red for new issues, blue for open ones being worked on, yellow for stalled issues, and green for resolved problems. To report a new problem, click the "Report Issue" button. You'll need to provide a brief summary and a more detailed description of the problem. After submitting, you'll be returned to your dashboard with a confirmation message.

To see more details about an issue or add more information, click the "View" button next to any issue. This takes you to a detailed page showing all information and comments. If you need to provide more details or ask questions, you can add a comment at the bottom of the page.

### Using the System as a Helper

Helpers are staff members who address the reported issues. After logging in as a helper, you'll see your Helper Dashboard with all active issues in the system.

As you work on issues, you'll manage their status using the dropdown menu next to each one. When you start working on a new issue, change its status to "Open." If you're waiting for more information, mark it as "Stalled." Once the problem is fixed, set it to "Resolved."

To work with a specific issue, click the "View" button to see all details. You can review the description and any existing comments, then add your own updates using the comment form at the bottom. If you comment on a resolved issue, the system will automatically reopen it.

To check issues you've personally reported, click "My Reported Issues".

As a helper, you can also report new issues yourself using the "Report Issue" button, just like visitors do.

### Using the System as an Administrator

Administrators have the most extensive permissions in the system. After logging in as an admin, you'll see the Admin Dashboard.

Administrators can manage issues just like helpers, but also have access to user management features. Click "Manage Users" to see all accounts in the system. From this page, you can change user roles by selecting a new role from the dropdown in the "Role" column. You can also activate or deactivate accounts by changing the status in the "Status" column - inactive users won't be able to log in.

As a Administrator, you can also report new issues yourself using the "Report Issue" button, and check issues you've personally reported, click "My Reported Issues", just like visitors and helpers do. Note that when you deactivate your account, the system will automatically log out and you will not be able to log in. If you want to log in again, you must log in with another admin account and modify your deactivated status.

### Managing Your Profile

All users, regardless of role, can manage their personal profile. To access your profile settings, click on your username in the navigation bar or look for a "Profile" link.

On your profile page, you can:

**View Your Information:** The profile page displays your current information including username, email address, first and last name, location, and role in the system.

**Update Personal Details:** You can edit your email address, first name, last name, and location. After making changes, click "Save Changes" to save them. The system will validate your email address format.

**Manage Your Profile Image:** Your profile picture appears throughout the system next to your name when you report issues or add comments. You can:
- Upload a new profile image by clicking "Choose File" and selecting an image from your computer (supported formats include PNG, JPG, JPEG, and GIF)
- Remove your current profile image by clicking the "Remove Image" button

**Change Your Password:** For security, you can update your password by providing:
- Your current password for verification
- Your new password (twice to confirm)

The system enforces strong password requirements:
- At least 8 characters long
- Contains at least one letter
- Contains at least one number
- Contains at least one symbol (like !@#$%^&*)

After changing your password, you'll remain logged in, but will need to use your new password the next time you log in.