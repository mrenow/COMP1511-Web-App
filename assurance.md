#Assurance

Provide assurances that your backend implementation is fit for purpose. Consider both verification and validation when doing this. This will, at a minimum, require acceptance criteria for your user stories.


Briefly describe the strategies you followed and tools you used to achieve this in assurance.md.

##Quality Assurance

Whilst developing the backend implementation for slackr, our team has included many strategies in which would provide assurance that our program is fit for its purpose. These include utilizing pylint, black box testing, code coverage and finally assurance tests based on user stories

Pylint is a source-code, bug and quality checker for python, that our team used mainly for basic syntax based error checking. Pylint is a very reliable and commonly utilised method for these small error checking tasks and our team has incorporated that into all of our backend code. This includes using Pylint for our Black box testing and user story based tests. 

As requested in Iteration 1, our team has designed a series of tests tailored towards each of the functions that were to be implemented in Iteration 2. This provides assurance as black box testing allows us to perceive what our functions may look like in Iteration 2 and therefore, stay on track for the implementations of the backend functions.

All tests written in the Black box testing are then tested with code coverage to decrease the chances of bugs.  

We have also checked each other’s works and ask other members for verification when someone’s code is interacting with another’s, while also looking for each other’s mistake before pushing.

##Assurance Tests

Written basic assurance tests to check off if a particular capability is implemented.

* Be able to see a list of channels
    list of channels should display by default
    channel names are displayed on the list
    
    

* Be able to display members of a channel
    permission level of members should be indicated
    members of the same permission level or roles are grouped together on the list
    

* Be able to make a channel private
    channel cannot be joined by non-members
    channel cannot be viewed by non-members

* Be able to create a channel
    be able to name the channel on creation
    
* Be able to invite people to a channel
    once invited the member is automatically added to the channel
    member should be added to the member list
    private channel members can invite non-members to join

User and Auth
* Be able to access another user’s profile for basic info

* Be able to register, login, logout or switch between different account

* Be able to change own profile details

* Be able to have password encrypted so that the password itself is not directly stored on servers

* Be able to reset password in case it is forgotten

 
Messaging
*  Be able to message channels and see messages in channels
 * The text field and send button should be central and easy to find
 * There should be minimal latency for message updates
 * Messages should always display in order of time
 * Messages should have a maximum length
 * There should be countermeasures to messages spam


Pin
* Be able to flag a message so it is easy to find later
 *Only admins or channel owners should be able to pin messages
 *There should be a easy to access place in which all the pinned messages in a channel can be viewed
 * Users should have the ability to unpin messages
Search
* A search field should allow users to search for messages on the server
 * The user should have some filters avaliable, such as channel, sender, time, etc
Remove
* Users should be able to remove their own messages.
* Admins and channel owners should be able to remove any messages on that channel
 * It should be difficult to accidentally remove a message 
Delayed send
* Users should be able to pick a time to send a message
 * It should not be possible to send a message in the past
 * It should be possible to edit/remove a message pending a send
 Edit
* Users should be able to edit their own messages
* Admins and channel owners should be able to edit messages within the channel
 * Message edits should be easy and quick to perform
 Reacts
* Users should be able to react other user’s messages
 * Reacts should display with the message.
 * Users should be able to remove their own reacts
 * Admins and server owners should be able to remove reacts from messages
