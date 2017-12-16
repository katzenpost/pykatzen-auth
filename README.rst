a minimalistic katzenpost-auth module
=====================================

registering an user
-------------------
use the convenience cli for testing::

  SERVER=http://lutecia:7900 ./katzenkey add foobar@idefix 5E49D63CA6FB54C3056BB2DB333D1DE221505FC34F3AD402E2F2A65568C92301

discover a key for an user::

  SERVER=http://lutecia:7900 ./katzenkey get foobar@idefix
  5E49D63CA6FB54C3056BB2DB333D1DE221505FC34F3AD402E2F2A65568C92301

or use curl::
  
  curl -X POST --data user=user@lutecia --data key=5E49D63CA6FB54C3056BB2DB333D1DE221505FC34F3AD402E2F2A65568C92301 http://lutecia:7900/add
  curl -X POST --data user=user@lutecia http://lutecia:7900/getkey

changes ahead
-------------
this API still needs to change.

* [ ] decide what parts are public and which endpoints are internal only.
* [ ] send IDKey and LINKKey separatedly.
