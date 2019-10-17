def factorial(x):
    if x <= 1:
        return 1
    return x * factorial(x - 1)


def indented_list_sort(indented_list, indent="    "):
    # The entry structure
    # alphabetic for clarity
    KEY, ITEM, CHILDREN = range(3)

    # Turning a list of strings into a list of entries.
    def add_entry(level, key, item, chidren):
        if level == 0:
            chidren.append((key, item, []))  # Notice this thinking
        else:
            # The item is a child of the last item in the children list.
            add_entry(level - 1, key, item, chidren[-1][CHILDREN])

    def update_indented_list(entry):
        indented_list.append(entry[ITEM])
        for subentry in sorted(entry[CHILDREN]):
            update_indented_list(subentry)

    entries = []
    for item in indented_list:
        level = 0
        i = 0
        # Determine the level of the item
        while item.startswith(indent, i):
            i += len(indent)
            level += 1
        key = item.strip().lower()
        add_entry(level, key, item, entries)

    indented_list = []
    for entry in sorted(entries):
        update_indented_list(entry)
    return indented_list
