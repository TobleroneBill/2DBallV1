# 2DBallV1
Initial Attempt at 2d ball physics
If you feel safe use the exe, but otherwise just copy paste the python code lol

This feels fun to mess around with so thought I'd upload

Controls:

<li>
  K - disables gravity
</li>
<li>
 Left Click - adds force to the ball in the direction of your mouse
</li>

<p>
  
</p>

<p>
Uploading as proof of trying, think I should do a blog, but this came up pretty out of nowhere as it was supposed to be for a games jam. 
Got too interested in vector maths and physics, so I basically spent the whole time just figuring out how to make realistic ball movement.
The main issue is that at certian angles, the ball doesn't move realistically due to how I made the velocity work 
These are 2 independant x and y velocity values which get added per tick, so to fix I basically need to get normalised angle to the mouse and a single velocity value,
then make the ball move in the normalised direction, by either using rotations or probably some Dot Product stuff that I haven't got to grips with yet.
</p>
  
Will hopefully be making a more in depth ball sim soon, so I can actually make a cool peggle clone with kill streaks and yellow fever upgrade =3
