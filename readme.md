Hi.  You're probably expecting a really nice fancy python script that maps IP to Port.
Unfortunately I suck at coding and just custom tailored some stuff to work in my environment.

My environment is campus edge routing for the access layer, so my hosts hang off the switch stacks directly without having to branch down several legs of switches.

Additionally my IP/SVI scheme is templated and standardized which allows me to easily script something like this.  

The idea is here however of how you would map IP to switchport in a trivial case.  This is not meant to be a very refined script, it is primarily a "this is how I did it, now you figure it out for your environment" type of deal.

Good luck.


CAVEATS: this is running on a webserver on ubuntu.  You'll need to port it to whatever you use.  Change string "SNMPKEY" to whatever your RO string is in your environment.
