import asyncio
import socket


@asyncio.coroutine
def async_resolve(host, loop):
    ips = set()
    try:
        addrinfo = yield from loop.getaddrinfo(host, 0)
        for addr in addrinfo:
            ips.add(addr[4][0])
    except socket.gaierror:
        pass
    return {host: tuple(ips)}


@asyncio.coroutine
def async_resolve_mass(hosts):
    res = dict()
    loop = asyncio.get_event_loop()
    jobs = list(async_resolve(host, loop) for host in hosts)
    jobs_res = yield from asyncio.wait(jobs)
    for job_res in jobs_res[0]:
        res.update(job_res.result())
    return res


def resolve(hosts):
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(async_resolve_mass(hosts))
    return res