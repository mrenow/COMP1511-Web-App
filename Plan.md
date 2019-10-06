# Iteration 2 Plan


## Team:
Organization meeting early this week on Tuesday. To discuss:
* Go through iteration 2 specs and discuss any rough changes to plan
* Decide on schedule
* Organize technical meeting later in the week to go over implementation structure. This can be done in the first meeting if we have time.

## Technical:

We can split the iteration development into three stages built on top of each other:


### Stage 1: Create data (3 hours)
Create data structures for objects (users, channels, messages). Write internal constructor and getter functions. No need to worry about access. By the end of this stage we should be able to change and view fields.
Write internal functions that will allow these general functionalities: 
```
_user_create
_channel_create
_message_create
_channel_get_details
_server_get_channels
_user_get_profile
_channel_get_messages
```


### Stage 2: Define fundamental interactions and access (6 hours)
Write functions required for a basic chat system and deal with access permissions. We shold have a usable system done by the end of this stage
```
auth_register
channels_create
channel_details
channels_listall
user_profile
channel_messages
admin_userpermission_change
auth_login
auth_logout
channel_leave
message_send
message_remove
channel_join
```

### Stage 3: Write remaining functionality according to user stories (???)
We should be able to immediately test each function that we write from here.



