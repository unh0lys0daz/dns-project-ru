def getdomains(hname):
    domains = []
    parts = hname.split('.')
    for i in range(len(parts)):
        domains.append('.'.join(parts[i:]))
    if domains:
        domains[-1] = '.'
    return domains

print(getdomains('thalia.nu.'))
