def parse_ping(output):
    'Parse the output of a ``ping` in to a PingResult named tuple'
    ping_result_pattern = r'(\d+) packets transmitted, (\d+) packets received, ([0-9.]+)% packet loss'
    mo = re.search(ping_result_pattern, output)
    if mo is None:
        raise NoMatch(ping_result_pattern, output)
    transmitted, received, loss_rate = mo.groups()
    return PingResult(int(transmitted), int(received), float(loss_rate))
