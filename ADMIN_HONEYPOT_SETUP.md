# Admin Honeypot Setup

## Overview
A custom admin honeypot has been implemented to enhance security by creating a fake Django admin login page that logs unauthorized access attempts while hiding the real admin interface.

## Features

### 🔒 Security Features
- **Fake admin login** - Looks identical to real Django admin
- **Access logging** - Records all login attempts with IP, user agent, credentials
- **Real admin hidden** - Moved to secure URL `/securelogin/`
- **Admin interface** - View logged attempts in real admin

### 📊 Monitoring
- **LoginAttempt model** - Stores all unauthorized access attempts
- **Admin interface** - View attempts in Django admin
- **Logging** - Writes to Django logger for monitoring
- **IP tracking** - Records source IP addresses

## URL Structure

### Public URLs (Honeypot)
- **`/admin/`** - Fake admin interface (honeypot)
- **`/admin/login/`** - Fake login page (honeypot)

### Secure URLs (Real Admin)
- **`/securelogin/`** - Real Django admin interface
- **`/securelogin/login/`** - Real admin login page

## Implementation Details

### 1. Custom App Structure
```
custom_admin_honeypot/
├── __init__.py
├── apps.py
├── models.py
├── views.py
├── urls.py
├── admin.py
└── migrations/
    └── 0001_initial.py
```

### 2. Models
```python
class LoginAttempt(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    username = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
```

### 3. Views
- **`fake_admin_login`** - Handles fake login attempts and logs them
- **`honeypot_admin`** - Shows fake admin interface

### 4. Templates
- **`login.html`** - Fake Django admin login page
- **`admin.html`** - Fake Django admin interface

## Setup Instructions

### 1. App Configuration
```python
# settings.py
INSTALLED_APPS = [
    # ... other apps
    'custom_admin_honeypot',  # Security: Custom fake admin login page
    # ... other apps
]
```

### 2. URL Configuration
```python
# urls.py
from custom_admin_honeypot import urls as custom_admin_honeypot_urls

urlpatterns = [
    # Fake admin login page (honeypot) - catches unauthorized access attempts
    path('admin/', include(custom_admin_honeypot_urls)),
    # Real admin login page - secure URL
    path('securelogin/', admin.site.urls),
    # ... other URLs
]
```

### 3. Database Migration
```bash
python manage.py makemigrations custom_admin_honeypot
python manage.py migrate
```

## Usage

### 1. Accessing Real Admin
- **URL**: `http://your-domain.com/securelogin/`
- **Login**: Use your actual admin credentials
- **Security**: Only accessible to authorized users

### 2. Monitoring Attempts
- **Admin Interface**: Go to `/securelogin/` → Login Attempts
- **View Details**: IP address, username, password, timestamp, user agent
- **Filter/Search**: By IP, username, date range

### 3. Logging
- **Django Logger**: Check logs for warning messages
- **Database**: All attempts stored in `LoginAttempt` model
- **Real-time**: Immediate logging of access attempts

## Security Benefits

### 1. Attack Detection
- **Brute force attempts** - Track repeated login tries
- **Credential stuffing** - Monitor username/password combinations
- **Bot activity** - Identify automated attacks
- **Geographic analysis** - Track IP locations

### 2. Attack Deterrence
- **Hidden admin** - Real admin not discoverable
- **Realistic honeypot** - Looks like real Django admin
- **Immediate feedback** - Attackers think they're succeeding
- **No real access** - All attempts are logged, not authenticated

### 3. Monitoring & Alerting
- **Admin dashboard** - View all attempts in real admin
- **Log analysis** - Search and filter attempts
- **Alert integration** - Can be extended with email alerts
- **Statistics** - Track attack patterns and frequency

## Admin Interface Features

### 1. LoginAttempt Admin
```python
@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'username', 'timestamp', 'user_agent_short']
    list_filter = ['timestamp', 'ip_address']
    search_fields = ['ip_address', 'username']
    readonly_fields = ['ip_address', 'user_agent', 'username', 'password', 'timestamp']
    ordering = ['-timestamp']
```

### 2. Viewing Attempts
- **List view** - See all attempts with key details
- **Filter by date** - Find attempts in specific time ranges
- **Search by IP** - Find attempts from specific addresses
- **Read-only** - Cannot modify logged attempts (security)

## Customization

### 1. Styling
- **Templates** - Modify `login.html` and `admin.html`
- **CSS** - Update styles to match your site
- **Branding** - Add your logo or custom elements

### 2. Logging
- **Additional fields** - Add more data to `LoginAttempt` model
- **External logging** - Send to external security services
- **Email alerts** - Notify administrators of attempts

### 3. Advanced Features
- **IP blocking** - Automatically block repeated offenders
- **Rate limiting** - Limit attempts per IP
- **Geolocation** - Add country/city tracking
- **Integration** - Connect with security monitoring tools

## Testing

### 1. Test Honeypot
```bash
# Visit fake admin
curl http://localhost:8000/admin/

# Try fake login
curl -X POST http://localhost:8000/admin/login/ \
  -d "username=admin&password=test"
```

### 2. Test Real Admin
```bash
# Visit real admin
curl http://localhost:8000/securelogin/
```

### 3. Check Logs
```python
# In Django shell
from custom_admin_honeypot.models import LoginAttempt
print(LoginAttempt.objects.count())
print(LoginAttempt.objects.first())
```

## Production Considerations

### 1. Security
- **Keep URL secret** - Don't share `/securelogin/` URL
- **Strong passwords** - Use complex admin passwords
- **HTTPS only** - Ensure admin access over HTTPS
- **IP restrictions** - Consider IP whitelisting

### 2. Monitoring
- **Regular checks** - Review login attempts regularly
- **Alert setup** - Configure alerts for suspicious activity
- **Log rotation** - Manage log file sizes
- **Backup** - Include attempts in database backups

### 3. Performance
- **Database indexing** - Add indexes for common queries
- **Cleanup** - Periodically clean old attempts
- **Caching** - Consider caching for high-traffic sites

## Result

✅ **Admin Honeypot Successfully Implemented!**

- **Security enhanced** - Real admin hidden, fake admin deployed
- **Attack monitoring** - All attempts logged and tracked
- **Admin interface** - Easy monitoring of security events
- **Production ready** - Fully functional and secure

The admin honeypot is now active and protecting your Django admin interface!
