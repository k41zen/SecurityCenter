from tenable.sc import TenableSC

def main():
    hostip = '<IP>'
    username = '<username>'
    password = '<password>'

    sc = TenableSC(hostip)
    sc.login(username, password)

    for item in sc.get('scanResult').json()['response']['manageable']:
        if 'Running' in item['status']:
            print('{id}: {name} totalChecks completedChecks'.format(**item))

    sc.logout()

if __name__ == '__main__':
    main()
