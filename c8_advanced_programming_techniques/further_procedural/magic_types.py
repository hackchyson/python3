def get_file_type(magic, ext):
    d = {'.py': 'Python', '.tex': 'LaTex', 'org': 'Emacs Org', '.pdf': 'PDF'}
    if ext in d:
        return d[ext]
    else:
        return None
