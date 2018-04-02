import uuid
from paytrack.io import PersonIO, GroupsIO
from paytrack.DEFAULTS import *
import pandas as pd


class Person:
    """
    Object that represents a person
    """
    def __init__(self, groups=None, **kwargs):
        """
        Initiates a person object
        :param kwargs: dictionary with the keyword arguments
        """

        # check whether all required arguments have been added
        self._check_required_attrs(kwargs)

        # save all attributes
        self._attrs = kwargs

        # initiate groups list
        self._groups = []

        # check whether an id has been added
        if not 'id' in self._attrs.keys():
            id = str(uuid.uuid4())
            self._attrs.update({'id': id})
            self._create()

        self._add(groups)

    def __str__(self):
        """String representation"""
        return self.name

    def _add(self, group_ids):
        """
        Internal function to add people to the group
        :param group_ids: person or list of person objects
        :return: None
        """

        # if people is None, do nothing
        if not group_ids:
            return

        # if it's a list, concatenate
        if type(group_ids) is list:
            self._groups += group_ids
        elif type(group_ids) is str:
            self._groups.append(group_ids)

    def _check_required_attrs(self, kwargs):
        """
        Checks whether all required attributes have been added to the person object
        :param kwargs: dictionary with the attributes
        :return: None
        """

        # loop over all required attributes and check whether they have been added
        # to the person object
        for attr in REQUIRED_PERSON_ATTRS:
            if not attr in kwargs.keys():
                raise AttributeError('Missing argument: \'{}\''.format(attr))

    @classmethod
    def from_id(cls, id):
        """
        Loads a person from its saved ID
        :param id: uuid string
        :return: Person object with the attributes saved under the respective ID
        """

        # load the data frame with all persons
        groups, attributes = PersonIO.get_person(id)
        return Person(groups=groups, **attributes)

    def _create(self):
        """
        Creates the new person in the person_df
        :return: None
        """

        PersonIO.add_person(self)

    def add_to_groups(self, group_ids):
        """
        Adds a person to groups
        :return: None
        """

        self._add(group_ids)

        # update the groups list
        PersonIO.update_groups_list(self)

    @property
    def groups(self):
        """Groups property"""
        return self._groups

    @property
    def name(self):
        """Name property"""
        return self._attrs['name']

    @property
    def id(self):
        """ID property"""
        return self._attrs['id']

    @property
    def attributes(self):
        """Attributes property"""
        return self._attrs

    def change_attribute(self, attr, new_val):
        """
        Change an attribute (e.g. name) of a person
        :param attr: attribute
        :param new_val: new value of the attribute
        :return: None
        """

        self._attrs[attr] = new_val
        PersonIO.update_person(self)

    def change_name(self, new_name):
        """
        Changes the name of a person
        :param new_name: new name of the person (string)
        :return: None
        """

        self.change_attribute('name', new_name)


class Group:
    """
    Object that represents a group of people in which payments are shared
    """
    def __init__(self, people=None, payments=None, **kwargs):
        """
        Initiates a new group object
        :param name: name of the group
        :param people: person object or list of person objects
        """

        # check whether all required arguments have been added
        self._check_required_attrs(kwargs)

        # save all attributes
        self._attrs = kwargs

        # members list
        if not people:
            people = []
        self._people = people

        # payments
        if not payments:
            payments = []
        self._payments = payments

        # check whether an id has been added (if no, it's a new group)
        if not 'id' in self._attrs.keys():
            id = str(uuid.uuid4())
            self._attrs.update({'id': id})
            self._create()

        self._add(people)

    def __str__(self):
        """String representation"""
        return self.name

    @classmethod
    def from_id(cls, id):
        """
        Loads a person from its saved ID
        :param id: uuid string
        :return: Person object with the attributes saved under the respective ID
        """

        # load the data frame with all persons
        people, attributes = GroupsIO.get_group(id)
        return Group(people=[Person.from_id(p.id) for p in people], **attributes)

    def _check_required_attrs(self, kwargs):
        """
        Checks whether all required attributes have been added to the person object
        :param kwargs: dictionary with the attributes
        :return: None
        """

        # loop over all required attributes and check whether they have been added
        # to the person object
        for attr in REQUIRED_PERSON_ATTRS:
            if not attr in kwargs.keys():
                raise AttributeError('Missing argument: \'{}\''.format(attr))

    def _add(self, people):
        """
        Internal function to add people to the group
        :param people: person or list of person objects
        :return: None
        """

        # if people is None, do nothing
        if not people:
            return

        # if it's a list, concatenate
        if type(people) is list:
            self._people += people

            # add the group to each person's group list
            for p in people:
                p.add_to_groups(self.id)

        elif type(people) is Person:
            self._people.append(people)

            # add the group to the person's group list
            people.add_to_groups(self)

    def add_people(self, people):
        """
        Adds people to a group
        :param people: person or list of person objects
        :return: None
        """

        self._add(people)

        # update the members list
        GroupsIO.update_group_members(self)

    def _create(self):
        """
        Creates the new person in the person_df
        :return: None
        """

        GroupsIO.add_group(self)

    @property
    def name(self):
        """Name property"""
        return self._attrs['name']

    @property
    def people(self):
        """People property"""
        return self._people

    @property
    def id(self):
        """ID property"""
        return self._attrs['id']

    @property
    def attributes(self):
        """Attributes property"""
        return self._attrs

    def change_attribute(self, attr, new_val):
        """
        Change an attribute (e.g. name) of a group
        :param attr: attribute
        :param new_val: new value of the attribute
        :return: None
        """

        self._attrs[attr] = new_val
        GroupsIO.update_group(self)

    def change_name(self, new_name):
        """
        Changes the name of a group
        :param new_name: new name of the group (string)
        :return: None
        """

        self.change_attribute('name', new_name)

    def add_payment(self, payment):
        """
        Adds a payment to the group
        :param payment: payment object
        :return: None
        """

        # make sure the payment is for the right group
        try:
            assert payment.group_id == self.id

        except AssertionError:
            raise ValueError('Payment is private to group {}, but was tried to be added to group {}.'.format(payment.group.id, self.id))

        self._payments.append(payment)


class Payment:
    """
    Represents payments
    """
    def __init__(self, by, group_id, amount, people=None, currency=None, location=None, purpose=None):
        """
        Creates a new payment
        :param by: person by whom the payment was made
        :param group_id: group for which the payment was made
        :param people: people in the group for which the payment was made
        :param amount: floating point representation of the amount
        :param currency: string representing the currency
        """

        self._by = by
        self._group_id = group_id
        self._amount = amount

        if not people:
            people = group_id.people
        self._people = people

        if not currency:
            currency = DEFAULT_CURRENCY
        self._currency = currency

        if not location:
            location = DEFAULT_LOCATION
        self._location = location

        if not purpose:
            purpose = DEFAULT_PURPOSE
        self._purpose = purpose

    @classmethod
    def from_dict(cls, payment_dict):
        """
        Creates a payment from a dataframe with the respective structure
        :return: payment object
        """
        return Payment(by=payment_dict['by'],
                       group_id=payment_dict['group_id'],
                       amount=payment_dict['amount'],
                       currency=payment_dict['currency'],
                       purpose=payment_dict['purpose'],
                       location=payment_dict['location'],
                       people=payment_dict['people'])

    @property
    def by(self):
        return self._by

    @property
    def group(self):
        return self._group

    @property
    def people(self):
        return self._people

    @property
    def amount(self):
        return self._amount

    @property
    def currency(self):
        return self._currency

    @property
    def purpose(self):
        return self._purpose

    @property
    def location(self):
        return self._location

    def to_df(self):
        """
        Transforms the payment into a pandas dataframe
        :return: dataframe representation of the payment
        """

        dct = {'by': [self.by],
               'amount': [self.amount],
               'currency': [self.currency],
               'purpose': [self.purpose],
               'location': [self.location]}

        # add people
        for p in self.group.people:
            if p in self.people:
                dct.update({p.id: [True]})
            else:
                dct.update({p.id: [False]})

        # turn into a dataframe and return
        return pd.DataFrame(dct)