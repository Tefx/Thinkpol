Thinkpol
========

> Big Brother is watching you!

## About

In Newspeak, "Thinkpol" means the Thought Police, the secret police of Ocenania in George Orwell's dystopian novel Nineteen Eighty-Four, who monitor almost everyone in the society.

We are building Thinkpol, not to montior any people, but to monitor every compenients' status in a large scale of cluster.

And the goals are:

1. Watching anything. 

    There are already lots of good ones for monitoring and cotroling processes remotely, like Supervisord, Monit and OpenTSDB. But all of they only monitor the external behaivor of the processes, servers or systems, such as CPU load, CPU times, memory usage, network, disk I/O etc. These are all important informations, but not the whole importants things. With these information, what we can make sure is only that our servers are alive or not. And actually we are guessing that the programgs works just fine, alone with the designed way, because everything seems no different as usual. Still water runs deep, and We can not assume the internal status by the external behavior. We want to fetch more imformation, inside and outside.

2. Transparency.

    We are **SECRET** police, that means we are not exist. To have the ability to measure and report the program's internal information, there must be some probes or others, but we want to hide as much as we can to reduce the programmer's work. 
    
## Detailed Design