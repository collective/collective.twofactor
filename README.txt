.. contents::

Introduction
============

This product provides "Two-factor" authorization mechanism for Plone.
It does this by subscribing to a Zope event fired after a successful traverse
has been done. If the authentication member has decided to use one of the
methods for Two-factor authentication, and his session is no longer valid,
then he will not be able to go anywhere in the site, unless he enters a valid
authentication token.


Methods
=======

Currently, this package provides 2 methods for getting an authorization token.
It is intended in the future to include additional ones.

Email
-----

A member of the site, can choose to receive a random code by email. For this,
make sure you have your E-mail system properly configured in your site.
If you have a problem with your email settings, then members might get
locked out of the system, since they cannot receive their authorization code.

The authorization code sent by mail is good to be used for a week, and once
the member has entered a valid code, there's no need for him to enter it again
for a day.
Users can request to reset their code, in the case they lost it, in which
case they will receive a new one.

SMS
---

A member of the site, can choose to receive a random code by SMS. For this,
make sure you have your Twilio account properly configured in your site.
If you have a problem with your sms settings, then members might get
locked out of the system, since they cannot receive their authorization code.

The authorization code sent by SMS is good to be used for a week, and once
the member has entered a valid code, there's no need for him to enter it again
for a day.
Users can request to reset their code, in the case they lost it, in which
case they will receive a new one.

Note: At this moment there is no validation for the member's cell phone, so they
must be sure to use a valid phone number. If they entered an invalid cell phone
number, they will get locked out of the system.

