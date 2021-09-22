DTL Website
=====================================

# Requirements
1. Python 2.7

# Installation
```bash
git clone gitlab@10.200.79.103:ynguyen/dtl-website.git
cd dtl-website
./setup.sh
source env/bin/activate
python manage.py migrate

# create superuser (for login admin panel)
python manage.py createsuperuser

```
# Run server locally
```
# Run server
./scripts/dev/runserver.sh

```

# Deploy to production
```
source env/bin/activate

# run server
./gunicorn/start.sh

# put all you test files (i.e developer-en.pdf, ...) to ./media/ folder.
```


# Update test files

- Check configuration in `dtlweb/settings/prod.py`.
- Currently all test files are kept in `media/` folder, and put to git repository too
in order to have version control of those test files.

- To update, just replace the file in `media/` folder, push to git and pull the change
on the deployment server.


# Other Notes

- Resumes are kepts in `media/resumes` folder.

# Recuitment Campain

- We run a recruitment campaign every year, every campaign is different, they have requirements for each one. We probably need to archive every applications of past year and start over for the new year.

## Design
- There will be a page for the year campaign which shows agenda and application form which also is the target for the year campaign marketing. The content is dynamically editable. Each year there can be different actions.

## Model
- CampaignOnlineApplication: Storing all candidate applications

## The Process of 2021
- Application statuses
    |From|To|Action|
    |----|--|------|
    |`None`|`New`|a candidate submits the form successfully|
    |`New` | `Invite_Sent`|The application has been passed and an invitation email has been sent|
    |`New` | `Failed`| The application was rejected, no notice to the applicant is needed|
    |`Invite_Sent` | `Invite_Accepted`| The candidate has accepted to attend the Joint test, the credentials email will be sent|
    |`Invite_Sent` | `Invite_Refused`| The candidate has refused to attend the Joint test, they will schedule the test like normal instead|
    |`Invite_Accepted`|`Reminder_1_Sent`||
    |`Reminder_1_Sent`|`Reminder_2_Sent`||

# Run unittest
```
source env/bin/activate
export DJANGO_SETTINGS_MODULE=dtlweb.settings.test
python manage.py test main.tests
```

# TODO
- Test, CI
- limit log file size
