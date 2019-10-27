# Passager (Password Manager)
Final project for University of Oulu's Faculty of ITEE's **Computer Security** course in 2019.


## What is _Passager_?
Passager is your locally run [password manager] that tries to accommodate for the middleground between automated and
manual password managing. The goal of Passager is to offer the safe password storage for all the services you use whilst
also helping you remember the passwords and train your muscle memory in writing them.

This means that Passager is not your traditional password manager. Its point isn't to handle the password managing for
you but rather to help you manage your passwords. I can already hear you thinking "But doesn't that mean Passager is
just a worse version of the already existing password managers?" Well, this depends quite a lot on your needs. If you
just want to "outsource" your password managing to a single program, this solution is not likely for you. On the other
hand, if you'd like to be able to remember your passwords yourself or to "store" them into your muscle memory, this
could be an option for you.


## How does it work?
You "create a main account" into this program (just to secure your other passwords behind this one, major password). Then
you may add as many services as you want to your account and a password for each of these. The passwords shall be stored
on your machine locally in an encrypted format. You may then (after logging in with the previously created account)
choose which service's password you'd like to train on. Passager asks you for the password for the service you chose.
You write the password and Passager informs you whether you got it correct or not. This way you may train your muscle
memory (and your cognitive memory) so that you're able to write the password down later on when you're actually logging
in to the service.

As you're not required to write down the actual name of the service or the account username for said service, the
password should not be easily utilizable by unauthorized people even **if** it were to leak (see section *Disclaimer*
for more information on the guarantees of this software).

Given the information above, it could be said that this software is ideal for the password change periods. As passwords
will be changed from time to time, it's always a little bit of a hazzle trying to remember the new password instead of
the old one. This solution offers the way to train your muscle memory with the new passwords. Yet again, an automatic
solution would be the most convenient here if you didn't care about remembering (or being able to type) the passwords
yourself. As for changing passwords, a very strong password doesn't **need** to be changed as long as it's not leaked
anywhere. However, people do change passwords from time to time (either out of own initiative or because the service
enforces a password changing policy). This software aims to aid these password changing periods.

As a password manager should do, this one does let you view your stored passwords as well. Once you've stored some
passwords and logged in with the major password, you're able to check out the passwords you've stored. This way you can
refresh your memory on the passwords you have in use.

But then again, you should be remembering those yourself, right? :)


## Disclaimer
As this project is mainly developed by one person (me) for the specific purpose of fulfilling a university course's
final project's requirements under a relatively tight schedule, this piece of software **may not actually be a secure
software solution**. I do not take any responsibility for any damages caused by the  use of this software. Use at your
own risk.

Instead of providing an actual well-tested and fully secure solution, this software is mainly meant for inspiration.
Feel free to use this for your own hobby projects or what-have-you. Just know that this is closer to a proof of concept
rather than a complete solution in terms of quality.

**This software was developed on Ubuntu and compability with other operating systems is not guaranteed.**

## Installation & Usage

1. Clone this repository
2. Install [PyCrypto]
3. Navigate terminal to this repository's directory
4. Execute the passager.py with either `python3 passager.py register` or `python3 passager.py login`

Registration is required for accessing the system's functions & features. After registration you can log in to your
account and start using the system.


[password manager]: https://en.wikipedia.org/wiki/Password_manager
[PyCrypto]: https://www.dlitz.net/software/pycrypto/
