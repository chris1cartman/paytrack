import pandas as pd
import os
from paytrack.DEFAULTS import *


class PersonIO:
    """
    IO class for persons
    """

    @staticmethod
    def _load_persons_list():
        """
        Loads the persons list, adjust this method if the file saving structure changes
        :return: persons list
        """
        # append the new person
        try:
            p_df = pd.read_csv(PERSON_DF)
        except FileNotFoundError:
            p_df = pd.DataFrame(columns=['name', 'id'])

        # set the index column
        p_df.index = p_df.loc[:, 'id']

        return p_df

    @staticmethod
    def _remove_from_list(p_list, person):
        """
        Removes a person from the list, adjust this method if the file saving structure changes
        :param p_list: persons list
        :param person: person object
        :return: persons list
        """

        p_list.drop(person.id, axis=0, inplace=True)
        return p_list

    @staticmethod
    def _update_person_in_list(p_list, person):
        """
        Updates a person in the list, adjust this method if the file saving structure changes
        :param p_list: persons list
        :param person: person object (with changed attributes)
        :return: None
        """

        # first remove the old version
        p_list = PersonIO._remove_from_list(p_list, person)

        # then add the new one
        p_list = PersonIO._add_person_to_list(p_list, person)

        # return the result
        return p_list

    @staticmethod
    def _add_person_to_list(p_list, person):
        """
        Adds a person to the list, adjust this method if the file saving structure changes
        :param p_list: persons list
        :param person: person object
        :return: None
        """

        p_df = pd.DataFrame({k: [person.attributes[k]] for k in person.attributes.keys()})
        p_df.index = p_df.loc[:, 'id']
        p_list = p_list.append(p_df)
        return p_list


    @staticmethod
    def _extract_person_from_list(p_list, id):
        """
        Extracts a single person from the list (given its uuid)
        :param p_list: persons list
        :param id: uuid of the person to extract
        :return: dictionary with the person attributes
        """

        return p_list.loc[p_list.index == id].iloc[0].to_dict()

    @staticmethod
    def _save_persons_list(p_list):
        """
        Saves the persons list
        :return: None
        """

        p_list.to_csv(PERSON_DF, index=False)

    @staticmethod
    def _load_groups_list(id):
        """
        Loads the groups list for a person
        :param id: uuid of a person
        :return: groups list
        """

        f_name = os.path.join(PERSONS_FOLDER, id + '.csv')

        try:
            groups_df = pd.read_csv(f_name)
        except FileNotFoundError:
            groups_df = pd.DataFrame(columns=['groups'])

        return list(groups_df.loc[:, 'groups'])

    @staticmethod
    def _update_groups_list(person):
        """
        Updates the groups list of a person
        :param member_list: groups list
        :param person: person object
        :return: None
        """

        f_name = os.path.join(PERSONS_FOLDER, person.id + '.csv')
        pd.DataFrame({'groups': person.groups}).to_csv(f_name, index=False)

    @staticmethod
    def _delete_groups_list(person):
        """
        Deletes a groups list for a person
        :param person: person object
        :return: None
        """

        f_name = os.path.join(PERSONS_FOLDER, person.id + '.csv')
        os.remove(f_name)

    @staticmethod
    def remove_person(person):
        """
        :param person: Person object
        :return: None
        """

        # remove the person from all groups
        p_list = PersonIO._load_persons_list()
        p_list = PersonIO._remove_from_list(p_list, person)
        PersonIO._save_persons_list(p_list)

        # remove groups list
        PersonIO._delete_groups_list(person)

    @staticmethod
    def add_person(person):
        """
        :return: None
        """

        # update person list
        p_list = PersonIO._load_persons_list()
        p_list = PersonIO._add_person_to_list(p_list, person)
        PersonIO._save_persons_list(p_list)

        # update the groups list
        PersonIO._update_groups_list(person)

    @staticmethod
    def update_person(person):
        """
        Saves the persons list
        :return: None
        """

        # update the person list
        p_list = PersonIO._load_persons_list()
        p_list = PersonIO._update_person_in_list(p_list, person)
        PersonIO._save_persons_list(p_list)

    @staticmethod
    def update_groups_list(person):

        # update the groups list for that person
        PersonIO._update_groups_list(person)

    @staticmethod
    def get_person(id):
        """
        Get a person from the list, given its id
        :param id: uuid of the person
        :return: dictionary with all person attributes
        """

        # attributes
        p_list = PersonIO._load_persons_list()
        attrs = PersonIO._extract_person_from_list(p_list, id)

        # groups list
        g_list = PersonIO._load_groups_list(id)

        return g_list, attrs


class GroupsIO:
    """
    IO class for groups
    """

    @staticmethod
    def _load_groups_list():
        """
        Loads the groups list, adjust this method if the file saving structure changes
        :return: groups list
        """

        try:
            g_df = pd.read_csv(GROUPS_DF)
        except FileNotFoundError:
            g_df = pd.DataFrame(columns=['name', 'id'])

        # set the index column
        g_df.index = g_df.loc[:, 'id']

        return g_df

    @staticmethod
    def _remove_from_list(g_list, group):
        """
        Removes a group from the list, adjust this method if the file saving structure changes
        :param g_list: groups list
        :param group: group object
        :return: groups list
        """

        g_list.drop(group.id, axis=0, inplace=True)
        return g_list

    @staticmethod
    def _update_group_in_list(g_list, group):
        """
        Updates a group in the list, adjust this method if the file saving structure changes
        :param g_list: groups list
        :param group: group object (with changed attributes)
        :return: None
        """

        # first remove the old version
        g_list = GroupsIO._remove_from_list(g_list, group)

        # then add the new one
        g_list = GroupsIO._add_group_to_list(g_list, group)

        # return the result
        return g_list

    @staticmethod
    def _add_group_to_list(g_list, group):
        """
        Adds a group to the list, adjust this method if the file saving structure changes
        :param g_list: groups list
        :param group: group object
        :return: None
        """

        p_df = pd.DataFrame({k: [group.attributes[k]] for k in group.attributes.keys()})
        p_df.index = p_df.loc[:, 'id']
        g_list = g_list.append(p_df)
        return g_list

    @staticmethod
    def _load_member_list(id):
        """
        Loads the member list of a group
        :param id: uuid of a group
        :return: member list
        """

        f_name = os.path.join(GROUPS_FOLDER, id + '.csv')

        try:
            member_df = pd.read_csv(f_name)
        except FileNotFoundError:
            member_df = pd.DataFrame(columns=['members'])

        return list(member_df.loc[:, 'members'])

    @staticmethod
    def _update_member_list(group):
        """
        Updates the member list of a group
        :param member_list: member list
        :param group: group object
        :return: member list
        """

        f_name = os.path.join(GROUPS_FOLDER, group.id + '.csv')
        pd.DataFrame({'members': [p.id for p in group.people]}).to_csv(f_name, index=False)

    @staticmethod
    def _delete_member_list(group):
        """
        Deletes a member list of a group
        :param group: group object
        :return: None
        """

        f_name = os.path.join(GROUPS_FOLDER, group.id + '.csv')
        os.remove(f_name)

    @staticmethod
    def _extract_group_from_list(g_list, id):
        """
        Extracts a single group from the list (given its uuid)
        :param g_list: groups list
        :param id: uuid of the pgroup to extract
        :return: dictionary with the group attributes
        """

        return g_list.loc[g_list.index == id].iloc[0].to_dict()

    @staticmethod
    def _save_groups_list(g_list):
        """
        Saves the groups list
        :return: None
        """

        g_list.to_csv(GROUPS_DF, index=False)

    @staticmethod
    def _load_payment_table(id):
        """
        Loads the payment table for a group
        :param id: uuid of a group
        :return: payment table
        """

        f_name = os.path.join(PAYMENTS_FOLDER, id + '.csv')

        try:
            payment_table = pd.read_csv(f_name)
        except FileNotFoundError:
            members = GroupsIO._load_member_list(id)
            payment_table = pd.DataFrame(columns=['by', 'amount', 'currency', 'purpose', 'location'] + members)

        return payment_table

    @staticmethod
    def _add_person_to_table(group_id, payments_table):
        """
        Adds a person to a payment table (a person that later joined a group)
        :param payments_table: payment table
        :return: payment table
        """

        f_name = os.path.join(PAYMENTS_FOLDER, group_id + '.csv')

        # get member list and make it a set
        member_list = set(GroupsIO._load_member_list(group_id))

        # get persons currently in the payment table and make them a set
        current_group = set(payments_table.columns) ^ {'by', 'amount', 'currency', 'purpose', 'location'}

        # add the person
        new_people = member_list ^ current_group
        new_person = new_people.pop()

        # add to the payments table
        payments_table.loc[:, new_person] = False

        # save
        payments_table.to_csv(f_name, index=False)

    @staticmethod
    def _add_payment_to_table(payment, payment_table):
        """
        Updates the payment table for a group
        :param payment_table: payment table
        :return: payment table
        """

        f_name = os.path.join(PAYMENTS_FOLDER, payment.group_id + '.csv')

        # add the line to the payment table
        payment_table = payment_table.append(payment.to_df())

        # save
        payment_table.to_csv(f_name, index=False)

    @staticmethod
    def _delete_member_list(group):
        """
        Deletes a member list of a group
        :param group: group object
        :return: None
        """

        f_name = os.path.join(GROUPS_FOLDER, group.id + '.csv')
        os.remove(f_name)

    @staticmethod
    def remove_group(group):
        """
        :param group: Group object
        :return: None
        """

        # remove from the groups list
        g_list = GroupsIO._load_groups_list()
        g_list = GroupsIO._remove_from_list(g_list, group)
        GroupsIO._save_groups_list(g_list)

        # remove group file
        GroupsIO._delete_member_list(group)

    @staticmethod
    def add_group(group):
        """
        :return: None
        """

        # add to the group list
        g_list = GroupsIO._load_groups_list()
        g_list = GroupsIO._add_group_to_list(g_list, group)
        GroupsIO._save_groups_list(g_list)

        # update members list
        GroupsIO._update_member_list(group)

    @staticmethod
    def update_group(group):
        """
        Saves the groups list
        :return: None
        """

        # update groups list
        g_list = GroupsIO._load_groups_list()
        g_list = GroupsIO._update_group_in_list(g_list, group)
        GroupsIO._save_groups_list(g_list)

    @staticmethod
    def update_group_members(group):
        """
        Updates the group members list
        :param group: group object
        :return: None
        """
        # update members list
        GroupsIO._update_member_list(group)

    @staticmethod
    def get_group(id):
        """
        Get a group from the list, given its id
        :param id: uuid of the group
        :return: dictionary with all group attributes
        """

        # group attributes
        g_list = GroupsIO._load_groups_list()
        attrs = GroupsIO._extract_group_from_list(g_list, id)

        # members
        m_list = GroupsIO._load_member_list(id)

        return m_list, attrs

    @staticmethod
    def get_payments(group_id, n=None):
        """
        Get all payments of a group
        :param group_id: id for the group
        :return: dictionary with the payment details
        """

        payments_table = GroupsIO._load_payment_table(group_id)

        s = len(payments_table)

        if n is None or n > s:
            n = s

        table_slice = payments_table[s-n:s, :]

        # get persons currently in the payment table and make them a set
        cols = ['by', 'amount', 'currency', 'purpose', 'location']
        whole_group = set(payments_table.columns) ^ set(cols)

        # loop over rows and create dicts
        res = []
        for _, row in table_slice:

            payment_dict = {}

            # get the people
            people = []
            for p in whole_group:
                if row[p]:
                    people.append(p)
            payment_dict.update({'people': people})

            # get all other variables
            for col in cols:
                payment_dict.update({col: row[col]})

            # append to the result list
            res.append(payment_dict)

        # return the result
        return res

    @staticmethod
    def add_payment(group_id, payment):
        """
        Adds a payment to a group
        :param group_id: id of the group
        :param payment: payment object
        :return: None
        """

        payments_table = GroupsIO._load_payment_table(group_id)
        GroupsIO._add_payment_to_table(payments_table, payment)