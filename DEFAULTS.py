import os

PERSON_DF = os.path.join('data', 'server', 'persons.csv')
PERSONS_FOLDER = os.path.join('data', 'server', 'persons')
GROUPS_DF = os.path.join('data', 'server', 'groups.csv')
GROUPS_FOLDER = os.path.join('data', 'server', 'groups')
PAYMENTS_DF = os.pah.join('data', 'server', 'payments.csv')
PAYMENTS_FOLDER = os.path.join('data', 'server', 'payments')
REQUIRED_PERSON_ATTRS = ['name']
REQUIRED_GROUP_ARGUMENTS = ['name']

DEFAULT_CURRENCY ='AUD'
DEFAULT_PURPOSE = 'General expense'
DEFAULT_LOCATION = 'Somewhere over the rainbow'