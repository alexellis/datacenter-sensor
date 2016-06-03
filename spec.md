Monitor polls redis set for members.

Member reads temp as member.temp kvp
Member reads motion level as member.motion kvp

Sensor on load sets itself into set.
Sensor updates member.temp and member.motion and member.temp.baseline

Sensor submits onto channel "update", sensor name.
