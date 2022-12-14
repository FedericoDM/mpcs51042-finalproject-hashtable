# Federico Dominguez Molina
# CNET ID: 12351429

# Imports

from collections import namedtuple
from collections.abc import MutableMapping

# Globally defining 'item' type
item = namedtuple("item", ["key", "value", "not_deleted"])


class Hashtable(MutableMapping):
    # polynomial constant, used for _hash
    P_CONSTANT = 37

    def __init__(self, capacity, default_value, load_factor, growth_factor):
        self.capacity = capacity
        self.new_capacity = capacity
        self._items = [None] * self.capacity
        self.default_value = default_value
        self.load_factor = load_factor
        self.growth_factor = growth_factor
        self.num_items = 0

    def _hash(self, key):
        """
        This method takes in a string and returns an integer value
        between 0 and self.capacity.

        This particular hash function uses Horner's rule to compute a large polynomial.

        See https://www.cs.umd.edu/class/fall2019/cmsc420-0201/Lects/lect10-hash-basics.pdf
        """
        val = 0
        for letter in key:
            val = self.P_CONSTANT * val + ord(letter)
        return val % self.capacity

    def resize(self):
        """
        Resizes the table to a new capacity and rehashes the data
        to a new location
        """
        # We need to increase the table's capacity and migrate the data
        # Reset the number of elements
        self.num_items = 0
        self.capacity = self.capacity * self.growth_factor

        # We need to rehash the old values
        old_items = []
        for item in self._items:
            if item is not None and item.not_deleted:
                old_items.append(item)
        self._items = [None] * self.capacity

        for old_item in old_items:
            key = old_item.key
            value = old_item.value
            self.__setitem__(key, value)

    def __setitem__(self, key, val):
        """
        Sets item in the hash table

        Parameters
        ----------
        key : str
            Key corresponding to the value
        val : _type_
            Value to insert in the table
        """

        # Getting index
        index = self._hash(key)
        overwrite = False
        while self._items[index] is not None:
            # check if overwriting
            if self._items[index].key == key:
                self._items[index] = item(key=key, value=val, not_deleted=True)
                overwrite = True
                break
            #  Wrap around
            if index == self.capacity - 1:
                index = 0
            else:
                index = index + 1

        # Out of loop, we found an empty spot
        if not overwrite:
            self._items[index] = item(key=key, value=val, not_deleted=True)
            self.num_items += 1

        # Check if table has enough size:
        current_factor = self.num_items / self.capacity
        if current_factor > self.load_factor:
            self.resize()

    def __getitem__(self, key):
        """
        Gets item by providing a key

        Parameters
        ----------
        key : str
            key of the element to search

        Returns
        -------
        _type_
            searched value
        """

        index = self._hash(key)
        while self._items[index] is not None:
            if self._items[index].key == key:
                if self._items[index].not_deleted:
                    return self._items[index].value
                else:
                    return self.default_value

            if index == self.capacity - 1:
                index = 0
            else:
                index += 1

        # If not found, default value is returned
        return self.default_value

    def __delitem__(self, key):
        """
        Logically deletes item from the hash table
        Parameters
        ----------
        key : string
            key to hash
        """
        # Key to look for
        index = self._hash(key)

        # item namedtuple template
        element = self._items[index]
        if element is not None:

            # Check case when element was already deleted
            if not element.not_deleted:
                # check if key is the same, double deletion
                if element.key == key:
                    raise KeyError("Key was already deleted")
                # Collision case - we need to look for the element
                else:
                    element_key = element.key
                    while element_key != key:
                        # wrap around
                        new_element = self._items[index]
                        if new_element is not None:
                            element_key = new_element.key
                            if element_key == key:
                                # Out of loop - element found
                                self._items[index] = item(
                                    key=new_element.key,
                                    value=new_element.value,
                                    not_deleted=False,
                                )
                                self.num_items = self.num_items - 1
                                return
                        if index == self.capacity - 1:
                            index = 0
                        else:
                            index += 1

                    # Out of loop - element found
                    self._items[index] = item(
                        key=new_element.key, value=new_element.value, not_deleted=False
                    )
                    self.num_items = self.num_items - 1

            # Element was not deleted
            else:
                self._items[index] = item(
                    key=element.key, value=element.value, not_deleted=False
                )
                self.num_items = self.num_items - 1
        else:
            raise KeyError("Not found")

    def __len__(self):
        """
        Counts the number of occupied slots in the hash table
        Deleted elements are not counted

        Returns
        -------
        int
            number of occupied slots
        """
        num_elements = 0
        for element in self._items:
            if element is not None and element.not_deleted:
                num_elements += 1
                
        return num_elements

    def __iter__(self):
        """
        You do not need to implement __iter__ for this assignment.
        This stub is needed to satisfy `MutableMapping` however.)

        Note, by not implementing __iter__ your implementation of Markov will
        not be able to use things that depend upon it,
        that shouldn't be a problem but you'll want to keep that in mind.
        """
        raise NotImplementedError("__iter__ not implemented")

    def __repr__(self):
        """
        Hashtable string representation

        Returns
        -------
        str
            items in the table
        """
        return str(self._items)
