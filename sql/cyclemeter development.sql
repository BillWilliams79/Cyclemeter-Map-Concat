

select * from route

select * FROM run WHERE routeID=56 OR routeID=10 ORDER BY startTime;

select
	* 
from
	run 
where 
	routeID = 10 OR routeID=56
ORDER BY startTime ASC;

                        SELECT
                            run.runID,
                            run.routeID,
                            activityID,
                            route.name,
                            startTime,
                            runTime,
                            stoppedTime,
                            distance,
                            ascent,
                            descent,
                            calories,
                            maxSpeed,
                            notes
                        FROM
                            run
                        JOIN
                            route USING(routeID)
                        WHERE
                            run.routeID=56 OR run.routeID=10
                        ORDER BY
                            run.startTime ASC;
