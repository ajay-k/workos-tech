# WorkOS SSO Example Application

This Django application demonstrates how to integrate WorkOS Single Sign-On (SSO) using the Test Provider. After successful authentication, the application displays the user's first name, last name, organization ID, and organization name.

## Features

- ✅ SSO authentication using WorkOS Test Provider
- ✅ Displays user's first name and last name
- ✅ Displays organization ID
- ✅ Displays organization name (bonus feature - requires additional API call)

## Prerequisites

- **Python 3.6 or higher** (check with `python3 --version`)
- **A free WorkOS account** 
- **pip** (Python package manager)

## Detailed Steps to Run the App Locally

### Step 1: Navigate to the Project Directory

Navigate to the `python-django-sso-example` directory:

```bash
cd python-django-sso-example
```

### Step 2: Create a Virtual Environment

Create and activate a Python virtual environment to isolate dependencies:

```bash
# Create virtual environment
python3 -m venv env

# Activate virtual environment
# On macOS/Linux:
source env/bin/activate

# On Windows:
# env\Scripts\activate
```

You should see `(env)` at the beginning of your command prompt, indicating the virtual environment is active.

### Step 3: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- Django 4.1.3
- WorkOS Python SDK (v5.33.0+)
- python-dotenv (for loading environment variables)
- Other dependencies

### Step 4: Set Up WorkOS Account and Get Credentials

#### 4.1 Create WorkOS Account

1. Go to [https://dashboard.workos.com/](https://dashboard.workos.com/)
2. Sign up for a free account if you don't have one

#### 4.2 Get API Key and Client ID

1. **Get API Key:**
   - In the WorkOS Dashboard, navigate to **Developer** → **API Keys**
   - Copy your API Key (starts with `sk_test_...` or `sk_live_...`)

2. **Get Client ID:**
   - In the WorkOS Dashboard, navigate to **Configuration** → **Authentication**
   - Copy your Client ID (starts with `client_01...`)

#### 4.3 Set Up Test Provider

1. Navigate to **Organizations** in the WorkOS Dashboard
2. Create a new organization (or use an existing one)
3. **Save the Organization ID**
4. Click on your organization to open it
5. Go to the **Connections** tab
6. Click **Add Connection** or **New Connection**
7. Select **Test Provider** as the connection type
8. Assign it to your organization
9. Save the connection

#### 4.4 Configure Redirect URI

1. In the WorkOS Dashboard, go to **Configuration** → **Authentication**
2. Find the **Redirect URIs** or **Allowed Redirect URIs** section
3. Add: `http://localhost:8000/auth/callback`
4. Save the configuration

**⚠️ CRITICAL: Test Provider Email Domain Requirement**

The WorkOS Test Provider **only accepts email addresses ending with `@example.com`**. 

**You must:**
- Use an email like `test@example.com`, `user@example.com`, or `anything@example.com`

**To ensure this works:**
- In WorkOS Dashboard → Organizations → [Your Organization] → Settings
- Make sure `example.com` is in the allowed domains list, OR
- Disable domain restrictions for the Test Provider connection

### Step 5: Configure Environment Variables

Create a `.env` file in the `python-django-sso-example` directory:

```bash
# Create .env file
touch .env
```

Open the `.env` file in a text editor and add the following environment variables:

```bash
# WorkOS API Configuration
# Get these from WorkOS Dashboard → Developer → API Keys
WORKOS_API_KEY=Insert your WorkOS API key here

# Get this from WorkOS Dashboard → Configuration → Authentication
WORKOS_CLIENT_ID=Insert your WorkOS Client ID here

# Organization ID for Test Provider
# Get this from WorkOS Dashboard → Organizations → [Your Organization] → Copy Organization ID
WORKOS_ORGANIZATION_ID=Insert your Organization ID here

# Redirect URI - must match what you configured in WorkOS Dashboard
REDIRECT_URI=http://localhost:8000/auth/callback
```

**Replace the placeholder values with your actual credentials:**

- `WORKOS_API_KEY`: Your API Key from Step 4.2 (starts with `sk_test_...` or `sk_live_...`)
- `WORKOS_CLIENT_ID`: Your Client ID from Step 4.2 (starts with `client_01...`)
- `WORKOS_ORGANIZATION_ID`: Your Organization ID from Step 4.3 (starts with `org_01...`)
- `REDIRECT_URI`: Keep as `http://localhost:8000/auth/callback` (must match WorkOS Dashboard configuration)

**Example `.env` file:**
```bash
WORKOS_API_KEY=Insert your WorkOS API key here
WORKOS_CLIENT_ID=Insert your WorkOS Client ID here
WORKOS_ORGANIZATION_ID=Insert your Organization ID here
REDIRECT_URI=http://localhost:8000/auth/callback
```

**⚠️ Important:** Replace all placeholder values with your actual credentials from the WorkOS Dashboard. Never commit real API keys to version control.

### Step 6: Run Database Migrations

Initialize the Django database:

```bash
python manage.py migrate
```

You should see output like:

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### Step 7: Start the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

You should see output similar to:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 4.1.3, using settings 'workos_django.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

**Note:** If you see CSS/images not loading, you may need to run with the `--insecure` flag:

```bash
python manage.py runserver --insecure
```

Please let me know if you have run into any issues