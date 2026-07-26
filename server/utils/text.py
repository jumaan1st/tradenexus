def filter_backticks(data):
    """Extract content between triple backticks, or return original if not found."""
    i = 0
    j = len(data) - 1

    while i < len(data) - 2:
        if data[i] == '`' and data[i+1] == '`' and data[i+2] == '`':
            i += 3
            while i < len(data):
                if data[i] == '\n':
                    break
                i += 1
            break
        i += 1

    while j >= 2:
        if data[j] == '`' and data[j-1] == '`' and data[j-2] == '`':
            j -= 3
            break
        j -= 1

    if i >= len(data) - 1 and j <= 1:
        return data
    else:
        return data[i+1:j]
