import shutil

def format_value_dynamic_width(value):
    if isinstance(value, list) and all(isinstance(v, (int, float)) for v in value):
        width = shutil.get_terminal_size((80, 20)).columns
        prefix_width = 6  # e.g., "[0]  "
        lines = []
        current_line = ""
        idx = 0
        i = 0
        while i < len(value):
            if not current_line:
                current_line = f"[{idx}] "
                current_len = prefix_width
            s = str(value[i])
            if current_len + len(s) + 1 > width:
                lines.append(current_line.rstrip())
                idx = i
                current_line = ""
                current_len = 0
            else:
                current_line += s + " "
                current_len += len(s) + 1
                i += 1
        if current_line:
            lines.append(current_line.rstrip())
        return "\n".join(lines)
    else:
        return str(value)

class Rist:
    def __init__(self, *args, **kwargs):
        self.values = list(args) + list(kwargs.values())
        self.names = [None] * len(args) + list(kwargs.keys())
        self._name_to_index = { name: idx for idx, name in enumerate(self.names) if name is not None }

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.values[key]
        elif isinstance(key, str):
            idx = self._name_to_index.get(key)
            if idx is None:
                raise KeyError(f"Name '{key}' not found")
            return self.values[idx]
        else:
            raise TypeError("Key must be int or str")

    def __getattr__(self, name):
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
        out_lines = []
        for idx, (name, value) in enumerate(zip(self.names, self.values)):
            if name is None:
                label = f"[{idx}] ({type(value).__name__})"
            else:
                label = f".{name} ({type(value).__name__})"
            out_lines.append(label)
            out_lines.append(self._format_value(value))
            out_lines.append("")
        return "\n".join(out_lines)

    def _format_value(self, value):
        return repr(value)
    

#class Rist:
#    def __init__(self, *args, **kwargs):
#        # Store unnamed and named values
#        self.values = list(args) + list(kwargs.values())
#        # Names: None for unnamed
#        self.names = [None] * len(args) + list(kwargs.keys())
#        self._name_to_index = { name: idx for idx, name in enumerate(self.names) if name is not None }
#
#    def __getitem__(self, key):
#        if isinstance(key, int):
#            return self.values[key]
#        elif isinstance(key, str):
#            idx = self._name_to_index.get(key)
#            if idx is None:
#                raise KeyError(f"Name '{key}' not found")
#            return self.values[idx]
#        else:
#            raise TypeError("Key must be int or str")
#
#    def __getattr__(self, name):
#        idx = self._name_to_index.get(name)
#        if idx is not None:
#            return self.values[idx]
#        raise AttributeError(f"'Rist' object has no attribute '{name}'")
#
#    def __dir__(self):
#        base = super().__dir__()
#        return list(base) + [n for n in self.names if n is not None]
#
#    def __len__(self):
#        return len(self.values)
#
#    def __repr__(self):
#        return f"Rist({self.names})"
#
#    def __str__(self):
#        out_lines = []
#        for idx, (name, value) in enumerate(zip(self.names, self.values)):
#            # Label: [0], [1], ... for unnamed; .name for named
#            if name is None:
#                out_lines.append(f"[{idx}]")
#            else:
#                out_lines.append(f".{name}")
#            out_lines.append(self._format_value(value))
#            out_lines.append("")
#        return "\n".join(out_lines)
#
#    def _format_value(self, value):
#        # Format numeric lists with dynamic width
#        if isinstance(value, list) and all(isinstance(v, (int, float)) for v in value):
#            return format_value_dynamic_width(value)
#        # Format list of strings
#        elif isinstance(value, list) and all(isinstance(v, str) for v in value):
#            return "[0] " + " ".join(f'"{v}"' for v in value)
#        # Format single string
#        elif isinstance(value, str):
#            return f'[0] "{value}"'
#        else:
#            return f"[0] {value}"
