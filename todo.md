Dorothy:
- View visible photos and info about them:​ Finstagram shows the user the photoID,photoOwner’s name, and caption of photos that are visible to the her, arranged inreverse chronological order. Display the photo or include a link to display it.Along with each photo the following  further information should be displayed or thereshould be an option to display it:  timestamp, the first names and last names of peoplewho have been tagged in the photo (taggees), provided that they have accepted the tags(Tag.acceptedTag == true)
- needs reverse chronological order
- needs to only show photos visible

Selina:
- Post a photo:​ User enters the relevant data and a link to a real photo and a designationof whether the photo is visible to all followers (allFollowers == true) or only to membersof designated CloseFriendGroups (allFollowers == false). Finstagram inserts data aboutthe photo (including current time, and current user as owner) into the Photo table. If thephoto is not visible to all followers, Finstagram gives the user a way to designateCloseFriendGroups that the user belongs to with which the Photo is shared.
- Right now, if you upload a photo, you do not include who uploaded the photo to database.

Rachel:
- Manage Follows: (a) User enters the username of someone they want to follow. Finstagram adds anappropriate tuple to Follow, with acceptedFollow == False. (b)User sees list of requests others has made to follow them and has opportunity toaccept, by setting acceptFollow to True or to decline by removing the requestfrom the Follow table.

Extra Features:
- Delete photos functionality.
- Add comment. (G)
- Like photo/see liked photos. (G)
- Follow request if account is private, otherwise no need to get approval for public account.
- Unfollow user. (G)
- Search by tag. (G)
- Search by poster. (G)
- More secure registration (need email to register).
- Forgot password?
