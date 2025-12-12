#!/usr/bin/env python
"""
Script to fix circular migration dependencies between laws and county apps.

This script will:
1. Delete all existing migrations (except __init__.py)
2. Recreate migrations in the correct order
3. Ensure no circular dependencies

USAGE:
    python fix_circular_migrations.py

WARNING: This will delete your migration history. Only use in development!
"""

import os
import shutil
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent
RECALL_SERVER = BASE_DIR / "recall_server"

# Apps with potential circular dependencies
APPS_TO_RESET = [
    "users",
    "polling_station", 
    "county",
    "voter",
    "mps",
    "voting",
    "laws",
    "recall",
    "discussions",
    "issues",
    "diaspora",
]

def backup_migrations():
    """Backup existing migrations"""
    backup_dir = BASE_DIR / "migrations_backup"
    backup_dir.mkdir(exist_ok=True)
    
    print("📦 Backing up migrations...")
    for app in APPS_TO_RESET:
        app_migrations = RECALL_SERVER / app / "migrations"
        if app_migrations.exists():
            backup_path = backup_dir / app
            if backup_path.exists():
                shutil.rmtree(backup_path)
            shutil.copytree(app_migrations, backup_path)
            print(f"   ✅ Backed up {app}/migrations")
    
    print(f"✅ Migrations backed up to: {backup_dir}\n")

def delete_migrations():
    """Delete all migration files except __init__.py"""
    print("🗑️  Deleting old migrations...")
    for app in APPS_TO_RESET:
        migrations_dir = RECALL_SERVER / app / "migrations"
        if migrations_dir.exists():
            for file in migrations_dir.glob("*.py"):
                if file.name != "__init__.py":
                    file.unlink()
                    print(f"   🗑️  Deleted {app}/migrations/{file.name}")
    print("✅ Old migrations deleted\n")

def delete_pycache():
    """Delete __pycache__ directories"""
    print("🗑️  Cleaning __pycache__...")
    for pycache in RECALL_SERVER.rglob("__pycache__"):
        shutil.rmtree(pycache)
    print("✅ Cache cleaned\n")

def main():
    print("=" * 60)
    print("🔧 Django Migration Circular Dependency Fix")
    print("=" * 60)
    print()
    
    # Confirm
    response = input("⚠️  This will DELETE all migrations. Continue? (yes/no): ")
    if response.lower() != "yes":
        print("❌ Aborted")
        return
    
    # Step 1: Backup
    backup_migrations()
    
    # Step 2: Delete migrations
    delete_migrations()
    
    # Step 3: Clean cache
    delete_pycache()
    
    # Step 4: Instructions
    print("=" * 60)
    print("✅ MIGRATIONS RESET COMPLETE!")
    print("=" * 60)
    print()
    print("📋 NEXT STEPS:")
    print()
    print("1. Create fresh migrations:")
    print("   python manage.py makemigrations")
    print()
    print("2. Review the new migrations to ensure no circular deps")
    print()
    print("3. If using PostgreSQL, drop and recreate database:")
    print("   docker-compose down -v")
    print("   docker-compose up -d db")
    print()
    print("4. Run migrations:")
    print("   python manage.py migrate")
    print()
    print("5. Create superuser:")
    print("   python manage.py createsuperuser")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
