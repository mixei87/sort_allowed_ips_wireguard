class Ip:
    def __init__(self, ip_string: str):
        if '/' in ip_string:
            ip_string, self.mask = ip_string.split('/')
            self.mask = int(self.mask)
        else:
            self.mask = 32
        self.first, self.second, self.third, self.fourth = map(int, (ip_string.split('.')))

    def __str__(self):
        if self.mask != 32:
            return f'{self.first}.{self.second}.{self.third}.{self.fourth}/{self.mask}'
        return f'{self.first}.{self.second}.{self.third}.{self.fourth}'

    def __lt__(self, other):
        s = (self.first, self.second, self.third, self.fourth, self.mask)
        o = (other.first, other.second, other.third, other.fourth, self.mask)
        for i in range(5):
            if s[i] != o[i]:
                if s[i] < o[i]:
                    return True
                return False
        else:
            return False


with open('/etc/wireguard/wg0.conf', 'r+') as f:
    start_word = 'AllowedIPs'
    other_content = f.read().split(start_word)[0].strip()
    f.seek(0)
    lines = [line.split('=')[1].strip() for line in f if line.startswith(start_word)]
    ips = [Ip(line) for line in lines]
    ips_string = '\n\nAllowedIPs = ' + '\nAllowedIPs = '.join(map(str, (sorted(ips)))) + '\n\n#AllowedIPs = 0.0.0.0/0'
    f.truncate(0)
    f.seek(0)
    f.write(other_content + ips_string)
