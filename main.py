class Rist:
    """
    Flexible R style list-like container supporting optional named elements.

    Features:
        - Access elements by index or name.
        - Supports nested Rist objects.
        - Pretty string representation with tree structure.
        - Attribute access for named elements.
        - Safe combination of multiple Rist objects without duplicate names.

    Attributes:
        values (list): List of stored elements.
        names (list): List of names or None for unnamed elements.
        _name_to_index (dict): Mapping of names to indices for fast lookup.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize a Rist object.
    
        Args:
            *args: Positional arguments (unnamed elements or a single dict).
            **kwargs: Keyword arguments (named elements).
        """
        # Special case: one dict argument with no kwargs
        if len(args) == 1 and isinstance(args[0], dict) and not kwargs:
            dict_items = args[0]
            self.values = list(dict_items.values())
            self.names = list(dict_items.keys())
        else:
            self.values = list(args) + list(kwargs.values())
            self.names = [None] * len(args) + list(kwargs.keys())
    
        self._name_to_index = {name: idx for idx, name in enumerate(self.names) if name is not None}

    def __getitem__(self, key):
        """
        Retrieve an element by index or name.

        Args:
            key (int or str): Index or name of the element.

        Returns:
            Any: The requested element.

        Raises:
            KeyError: If the name does not exist.
            TypeError: If the key is not int or str.
        """
        if isinstance(key, int):
            return self.values[key]
        elif isinstance(key, str):
            idx = self._name_to_index.get(key)
            if idx is None:
                raise KeyError(f"Name '{key}' not found")
            return self.values[idx]
        else:
            raise TypeError("Key must be int or str")
        
    def __setitem__(self, key, value):
        """
        Set an element by index or name.

        Args:
            key (int or str): Index or name of the element.
            value (Any): Value to assign.

        Behavior:
            - If key is int:
                * Sets the value at the given index.
                * Automatically extends the list with None if index is beyond current length.
            - If key is str:
                * Overwrites existing value if name exists.
                * Appends as a new named element if name does not exist.

        Raises:
            IndexError: If key is a negative integer.
            TypeError: If key is neither int nor str.
        """
        if isinstance(key, int):
            if key < 0:
                raise IndexError("Negative indexing not supported")
            while key >= len(self.values):
                self.values.append(None)
                self.names.append(None)
            self.values[key] = value
        elif isinstance(key, str):
            idx = self._name_to_index.get(key)
            if idx is not None:
                self.values[idx] = value
            else:
                self.values.append(value)
                self.names.append(key)
                self._name_to_index[key] = len(self.values) - 1
        else:
            raise TypeError("Key must be int or str")

    def __getattr__(self, name):
        """
        Enable attribute-like access to named elements.

        Args:
            name (str): Name of the element.

        Returns:
            Any: The requested element.

        Raises:
            AttributeError: If the name does not exist.
        """
        idx = self._name_to_index.get(name)
        if idx is not None:
            return self.values[idx]
        raise AttributeError(f"'Rist' object has no attribute '{name}'")

    def __iter__(self):
        return iter(self.values)

    def __dir__(self):
        base = super().__dir__()
        return list(base) + [n for n in self.names if n is not None]

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return f"Rist({self.names})"

    def __str__(self):
        """
        Return a tree-style string representation of contents.

        Returns:
            str: Formatted string showing the nested structure.
        """
        return self._str_with_indent(name="(root)", parent_prefix="", is_last=True)

    def _str_with_indent(self, name, parent_prefix, is_last):
        """
        Helper to recursively build the tree-style string representation.

        Args:
            name (str): Name or label of the current node.
            parent_prefix (str): Prefix for alignment.
            is_last (bool): Whether this is the last child.

        Returns:
            str: Multi-line string for this node and children.
        """
        lines = []
        connector = "└── " if is_last else "├── "

        # Determine label text
        label_text = f"{connector}.{name} (Rist)" if name != "(root)" else f".(Rist)"
        lines.append(parent_prefix + label_text)

        # Build new prefix for children
        new_prefix = parent_prefix + ("    " if is_last else "│   ")

        for i, (child_name, child_value) in enumerate(zip(self.names, self.values)):
            is_child_last = (i == len(self.values) - 1)
            if child_name is None:
                child_label = f"[{i}]"
            else:
                child_label = child_name

            if isinstance(child_value, Rist):
                # Recursively format nested Rist
                lines.append(
                    child_value._str_with_indent(
                        name=child_label,
                        parent_prefix=new_prefix,
                        is_last=is_child_last
                    )
                )
            else:
                # Leaf node
                connector_child = "└── " if is_child_last else "├── "
                line = new_prefix + f"{connector_child}.{child_label} ({type(child_value).__name__})"
                lines.append(line)
                # Indent value lines
                repr_lines = repr(child_value).splitlines()
                for rline in repr_lines:
                    lines.append(new_prefix + ("    " if is_child_last else "│   ") + rline)
        return "\n".join(lines)
    
    def __add__(self, other):
        """
        Combine two Rist objects into a new Rist.

        Args:
            other (Rist): Another Rist to combine.

        Returns:
            Rist: New combined Rist object.

        Raises:
            ValueError: If duplicate names are detected.
        """
        if not isinstance(other, Rist):
            return NotImplemented
    
        # Check duplicate names
        self_names_set = {n for n in self.names if n is not None}
        other_names_set = {n for n in other.names if n is not None}
        duplicates = self_names_set & other_names_set
    
        if duplicates:
            dup_list = ", ".join(f"'{d}'" for d in duplicates)
            raise ValueError(f"Duplicate name(s) {dup_list} detected during addition.")
    
        # Combine
        combined = Rist()
        combined.values = self.values + other.values
        combined.names = self.names + other.names
        combined._name_to_index = {n: i for i, n in enumerate(combined.names) if n is not None}
        return combined

    def append(self, *args, **kwargs):
        """
        Append an element to the Rist.

        Usage:
            - append(obj): Append unnamed element.
            - append(name=obj): Append named element (must be unique).

        Args:
            *args: Single unnamed element.
            **kwargs: Single named element.

        Raises:
            ValueError: If both positional and keyword arguments are provided,
                        more than one argument is provided,
                        or name duplicates exist.
        """
        if args and kwargs:
            raise ValueError("Cannot use both positional and keyword arguments.")
        if len(args) > 1:
            raise ValueError("Only one positional argument allowed.")
        if len(kwargs) > 1:
            raise ValueError("Only one keyword argument allowed.")
    
        if args:
            obj = args[0]
            self.values.append(obj)
            self.names.append(None)
        elif kwargs:
            name, obj = next(iter(kwargs.items()))
            if name in self._name_to_index:
                raise ValueError(f"Name '{name}' already exists in this Rist.")
            self.values.append(obj)
            self.names.append(name)
            self._name_to_index[name] = len(self.values) - 1
        else:
            raise ValueError("No object provided to append.")