# Database Migration Plan

This document outlines the plan for migrating from the custom `Voter` model to using Django's built-in `User` model with a `VoterProfile` extension.

## Background

Currently, the application uses a custom `Voter` model for user authentication and profile information. This approach has several drawbacks:

1. It doesn't leverage Django's built-in authentication system
2. It requires custom implementation of authentication features
3. It doesn't integrate well with third-party Django apps that expect the standard User model

The migration will move us to using Django's built-in `User` model with a `VoterProfile` model that extends it through a one-to-one relationship.

## Migration Steps

### 1. Pre-Migration Tasks

- [x] Create the new `VoterProfile` model
- [x] Update serializers to work with both models
- [x] Update views to work with both models
- [x] Update URLs to support both old and new endpoints
- [x] Create migration file to handle data transfer

### 2. Database Migration

Run the following commands to apply the migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

The migration will:
1. Create the new `VoterProfile` model
2. For each existing `Voter`:
   - Create a corresponding Django `User`
   - Create a `VoterProfile` linked to that user
   - Copy all relevant data from `Voter` to `User` and `VoterProfile`

### 3. Code Transition Period

During the transition period:
- Both the old `Voter` model and new `VoterProfile` model will coexist
- New registrations will create both a `User`/`VoterProfile` and a legacy `Voter` record
- The API will support both old and new endpoints

### 4. Post-Migration Tasks

After the migration is complete and all clients have been updated:

1. Remove the legacy `Voter` model
2. Remove legacy serializers and views
3. Remove legacy endpoints
4. Create a final migration to clean up the database

## API Changes

### Legacy Endpoints (to be deprecated)

- `POST /api/voter/register/` - Register a new voter using the legacy model

### New Endpoints

- `POST /api/voter/user/register/` - Register a new user with the Django User model
- `GET /api/voter/profiles/` - List all voter profiles (authenticated users only)
- `GET /api/voter/profiles/{id}/` - Get a specific voter profile
- `GET /api/voter/profiles/me/` - Get the current user's profile
- `POST /api/voter/profiles/{id}/follow_bill/` - Follow a bill
- `POST /api/voter/profiles/{id}/unfollow_bill/` - Unfollow a bill

## Testing

Before deploying to production:

1. Test the migration on a staging environment
2. Verify that all existing `Voter` records are properly migrated
3. Test both legacy and new endpoints
4. Verify that authentication works with the new model

## Rollback Plan

If issues are encountered during migration:

1. Revert the migration: `python manage.py migrate voter 0001_initial`
2. Revert code changes to use the legacy `Voter` model
3. Deploy the reverted code

## Timeline

1. Deploy code changes with both models (Week 1)
2. Run migration on production (Week 1)
3. Update clients to use new endpoints (Weeks 2-4)
4. Remove legacy code and models (Week 5) 