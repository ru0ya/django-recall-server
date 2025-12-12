# Fix Circular Migration Dependency: laws ↔️ county

## Problem
```
CircularDependencyError: laws.0001_initial, county.0001_initial
```

The Bill model has ForeignKeys to Senator and MCA, creating a circular dependency.

---

## Solution 1: Delete & Recreate (RECOMMENDED for Development) ⭐

### Step 1: Backup Database
```bash
# If using Docker PostgreSQL
docker-compose exec db pg_dump -U your_user your_db > backup.sql
```

### Step 2: Delete Migrations
```bash
# Delete all migration files except __init__.py
find recall_server/*/migrations -name "*.py" ! -name "__init__.py" -delete

# Clean pycache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
```

### Step 3: Drop Database (Docker)
```bash
docker-compose down -v
docker-compose up -d db
```

### Step 4: Recreate Migrations in Correct Order
```bash
# Create migrations for base apps first (no dependencies)
python manage.py makemigrations users
python manage.py makemigrations polling_station
python manage.py makemigrations county

# Then apps that depend on county
python manage.py makemigrations mps
python manage.py makemigrations voting

# Then apps that depend on multiple apps
python manage.py makemigrations voter
python manage.py makemigrations laws
python manage.py makemigrations recall
python manage.py makemigrations discussions
python manage.py makemigrations issues
python manage.py makemigrations diaspora

# Or create all at once (Django will figure out order)
python manage.py makemigrations
```

### Step 5: Apply Migrations
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## Solution 2: Comment Out ForeignKeys Temporarily

### Step 1: Comment out the problematic fields in laws/models.py
```python
# In recall_server/laws/models.py, lines 100-120
# Comment these out temporarily:

# nationalassembly_proposal = models.ForeignKey(
#     'mps.MemberOfParliament',
#     on_delete=models.SET_NULL,
#     null=True,
#     blank=True,
#     related_name='nationalassembly_proposals'
# )
# senate_proposal = models.ForeignKey(
#     'county.Senator',
#     on_delete=models.SET_NULL,
#     null=True,
#     blank=True,
#     related_name='senate_proposals'
# )
# county_assembly_proposal = models.ForeignKey(
#     'county.MCA',
#     on_delete=models.SET_NULL,
#     null=True,
#     blank=True,
#     related_name='county_assembly_proposals'
# )
```

### Step 2: Delete migrations and recreate
```bash
find recall_server/*/migrations -name "*.py" ! -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Uncomment the fields
```python
# Uncomment the fields in laws/models.py
```

### Step 4: Create a new migration
```bash
python manage.py makemigrations laws
python manage.py migrate
```

---

## Solution 3: Manual Migration Dependency Fix (Production Safe)

If you have existing data and can't delete migrations:

### Step 1: Find the migration files
```bash
ls -la recall_server/laws/migrations/
ls -la recall_server/county/migrations/
```

### Step 2: Edit laws/migrations/0001_initial.py

Add this at the top of the Migration class:
```python
class Migration(migrations.Migration):
    dependencies = [
        ('county', '0001_initial'),  # Add this line
        ('mps', '0001_initial'),     # Add this line
        # ... other dependencies
    ]
```

### Step 3: Remove circular dependency from county
Edit county/migrations/0001_initial.py and ensure it doesn't depend on laws:
```python
class Migration(migrations.Migration):
    dependencies = [
        # Should NOT have ('laws', '0001_initial')
    ]
```

### Step 4: Fake the migrations if already applied
```bash
python manage.py migrate --fake
```

---

## Solution 4: Use RunPython Script (Advanced)

Create migrations without ForeignKeys first, then add them via RunPython.

This is complex and only needed for production with existing data.

---

## Recommended Approach for Your Case

Since you're in development (using Docker), **use Solution 1**:

```bash
# Quick commands:
cd /home/ru0ya/django-recall-server

# Run the Python script
python fix_circular_migrations.py

# Or manually:
find recall_server/*/migrations -name "*.py" ! -name "__init__.py" -delete
docker-compose down -v
docker-compose up -d db
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## Prevention for Future

To avoid this in the future:

1. **Use string references** in ForeignKeys (you already do this ✅)
2. **Make ForeignKeys nullable** (you already do this ✅)
3. **Create migrations incrementally** - don't add cross-app ForeignKeys in initial migrations
4. **Use a clear app dependency hierarchy**:
   ```
   users (base)
   ├── county
   ├── mps
   ├── voting
   └── laws (depends on county, mps)
       └── recall (depends on laws, county, mps)
   ```

The issue is that Django creates all `0001_initial.py` migrations at once, and they reference each other.
