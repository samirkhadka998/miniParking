# miniParking
mini parking system
#### Video Demo:  <URL HERE>
#### Description:
This is parking system. It has vehicle brand, number, vehicle type with hourly rate, 
discount based on type of customer. Here are some major backbones of this app.

1.Location :-
Location is fixed for now. There are 11 location A,B..J and special locaiton that is called
Transit , Transit is virtual location when vehcile is just arriving in, it will be Transit to location A or during 
Check Out will look like location B to Transit. 
Transit is just to track movement outside the parking during vehicle checkin and checkout.
It is automatically added during checkin and checkout. Similarly if vehicle a 
checks in Location A , Other vehicle cannot check in in same location, until vehicle is moved or 
check out.


2.CheckIn :-
User can check in vehicle to given location. A to J. If A is already filled then A option is not 
shown to user. User have to select type , brand ,number, location, and discount. If we try to 
save same checkin vehicle twice error is thrown. Same vehicle is combitnation of Brand and Number.
Report can be viewed in CheckIn Report.

3.Move :-
User can mvoe vehicle form one place to another. Eg from A to B, condition is B should be empty
and after moving A will be empty. Hope it makes sense. One user checkout any vehicle , it's 
location is auto emptied.
Report can be seen in Move Report.

4.CheckOut :-
As mentioned above after checkout vehicle current location will empty and it moves to transit.
Report can be seen in CheckOut Report.

5.Main Page(Index) :-
Here vehicle CheckIn, Checkout and move all take place. You cannot checkout or move if vehcile is
not arrived yet. Doesn't make sense. And here only vehicle that are in parking are shown. Not that 
are already checkout. It is like current status of our parking system.

Happy Coding!!


