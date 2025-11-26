import os
import json
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from workos import WorkOSClient

# Initialize WorkOS client with credentials from environment variables
workos = WorkOSClient(
    api_key=os.getenv("WORKOS_API_KEY"),
    client_id=os.getenv("WORKOS_CLIENT_ID")
)

# Configuration from environment variables
WORKOS_ORGANIZATION_ID = os.getenv("WORKOS_ORGANIZATION_ID", "")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/auth/callback")


def login(request):
    """
    Main login view - displays login page or success page based on session state.
    
    If user is not authenticated (no active session), show the login page.
    If user is authenticated (active session exists), show the success page with user info.
    """
    session_active = request.session.get("session_active", False)
    
    print(f"Login view - session_active: {session_active}")
    
    if not session_active:
        return render(request, "sso/login.html")

    # User is authenticated - show success page with their information
    return render(
        request,
        "sso/login_successful.html",
        {
            "first_name": request.session.get("first_name", ""),
            "last_name": request.session.get("last_name", ""),
            "organization_id": request.session.get("organization_id", ""),
            "organization_name": request.session.get("organization_name", ""),
            "raw_profile": json.dumps(request.session.get("raw_profile", {}), indent=2),
        },
    )


def auth(request):
    """
    Initiates the SSO authentication flow.
    
    When user clicks "Sign in with Test Provider", this function:
    1. Validates that WORKOS_ORGANIZATION_ID is configured
    2. Generates an authorization URL using WorkOS SDK
    3. Redirects user to WorkOS Test Provider for authentication
    """
    if not WORKOS_ORGANIZATION_ID:
        print("❌ WORKOS_ORGANIZATION_ID not configured")
        return HttpResponse(
            "Error: WORKOS_ORGANIZATION_ID environment variable is not set.",
            status=500
        )
    
    try:
        # Generate authorization URL for organization-based SSO
        authorization_url = workos.sso.get_authorization_url(
            redirect_uri=REDIRECT_URI,
            organization_id=WORKOS_ORGANIZATION_ID,
        )
        
        print(f"Redirecting to WorkOS authorization URL")
        return redirect(authorization_url)
        
    except Exception as e:
        print(f"❌ Error in auth: {str(e)}")
        return HttpResponse(f"Error: {str(e)}", status=500)


def auth_callback(request):
    """
    Handles the callback from WorkOS after user authenticates.
    
    This is called by WorkOS after user completes authentication:
    1. Checks for errors in the callback
    2. Extracts authorization code from URL
    3. Exchanges code for user profile using WorkOS SDK
    4. Extracts user information (first name, last name, organization ID)
    5. Fetches organization name (bonus requirement)
    6. Stores all data in session
    7. Redirects to login page (which will show success page)
    """
    # Check if WorkOS returned an error
    error = request.GET.get("error")
    if error:
        error_description = request.GET.get("error_description", "Unknown error")
        print(f"❌ Authentication error: {error}")
        print(f"   Description: {error_description}")
        return HttpResponse(
            f"<h1>Authentication Error</h1><p>{error_description}</p>"
            f"<p><a href='/'>Return to login</a></p>",
            status=400
        )
    
    # Get authorization code from callback URL
    code = request.GET.get("code")
    if not code:
        print("❌ No authorization code received")
        return redirect("login")
    
    try:
        # Exchange authorization code for user profile
        profile_response = workos.sso.get_profile_and_token(code)
        profile = profile_response.profile
        
        # Convert Pydantic model to dictionary for easier access
        if hasattr(profile, 'model_dump'):
            profile_dict = profile.model_dump()
        else:
            profile_dict = {}
        
        # Extract user information from profile
        first_name = profile_dict.get('first_name', '') or getattr(profile, 'first_name', '')
        last_name = profile_dict.get('last_name', '') or getattr(profile, 'last_name', '')
        organization_id = profile_dict.get('organization_id', '') or getattr(profile, 'organization_id', '')
        
        print(f"✓ Extracted user info - First: '{first_name}', Last: '{last_name}', Org ID: '{organization_id}'")
        
        # Fetch organization name (bonus requirement - requires additional API call)
        organization_name = ""
        if organization_id:
            try:
                organization = workos.organizations.get_organization(organization_id)
                organization_name = getattr(organization, 'name', '') or ''
                print(f"✓ Fetched organization name: '{organization_name}'")
            except Exception as e:
                print(f"⚠️  Error fetching organization name: {str(e)}")
                # Continue without organization name - not critical
        
        # Store user information in session
        request.session["first_name"] = first_name
        request.session["last_name"] = last_name
        request.session["organization_id"] = organization_id
        request.session["organization_name"] = organization_name
        request.session["raw_profile"] = profile_dict
        request.session["session_active"] = True
        request.session.modified = True  # Ensure session is saved
        
        print(f"✓ Session data stored successfully")
        print(f"  First Name: {first_name}")
        print(f"  Last Name: {last_name}")
        print(f"  Organization ID: {organization_id}")
        print(f"  Organization Name: {organization_name}")
        
        # Redirect to login page (which will detect active session and show success page)
        return redirect(reverse("login"))
        
    except Exception as e:
        print(f"❌ Error in auth_callback: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return redirect("login")


def logout(request):
    """
    Logs out the user by clearing the session.
    
    Clears all session data and redirects back to login page.
    """
    request.session.clear()
    print("✓ User logged out")
    return redirect("login")
