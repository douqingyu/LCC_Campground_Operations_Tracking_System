-- Populate users table (20 visitors, 5 helpers, 2 admins)
INSERT INTO `users` (`username`, `password_hash`, `email`, `first_name`, `last_name`, `location`, `profile_image`, `role`, `status`) VALUES
-- Administrators (2)
('admin1', '$2b$12$wURCn4ycmqlrnJEspPhmru6Y6XBghAvYI8ShHHrQyKcxilC8Poo.O', 'admin1@example.com', 'Admin', 'One', 'Auckland', NULL, 'admin', 'active'),
('admin2', '$2b$12$wF3Yc6yIq/JjjUuZK.Kyq.GByBosUmybhPLmoUcB.Xr1n290UnXzq', 'admin2@example.com', 'Admin', 'Two', 'Wellington', NULL, 'admin', 'active'),

-- Helpers (5)
('helper1', '$2b$12$U3HTP6/ZYxHA5bPa9r9MWuw0GIczzKG6m6Lwgo08PMOap6iEbby6u', 'helper1@example.com', 'Helper', 'One', 'Christchurch', NULL, 'helper', 'active'),
('helper2', '$2b$12$P0n1ffehBre5FS8xaLRjSOFg.1VTgsiKaHJ9Cx3zGQEhtxileebQa', 'helper2@example.com', 'Helper', 'Two', 'Hamilton', NULL, 'helper', 'active'),
('helper3', '$2b$12$Gs/L/wR/94dE5kfMg0iFAOkmlmKi71uMutC2dwEqz1a5c8mRvq5r6', 'helper3@example.com', 'Helper', 'Three', 'Tauranga', NULL, 'helper', 'active'),
('helper4', '$2b$12$uXDEt9TB/kgCwOWH.MfJ.ud59KtImBjaYqWJh5T2ztK9H540aUCEu', 'helper4@example.com', 'Helper', 'Four', 'Napier-Hastings', NULL, 'helper', 'active'),
('helper5', '$2b$12$Ldq/0.jzzMUNkEFevFusT.DEYL1q4NUNN/Gp12JTmhBkrdxpaMC8y', 'helper5@example.com', 'Helper', 'Five', 'Dunedin', NULL, 'helper', 'active'),

-- Visitors (20)
('visitor1', '$2b$12$G.TGPWD4X2nclkg1snO5Ze3PZXp89aYfAG2yvb4y5MFTw2J75K.Qe', 'visitor1@example.com', 'Visitor', 'One', 'Palmerston North', NULL, 'visitor', 'active'),
('visitor2', '$2b$12$.k/B/Rh4Wf/IwuamP8n7gOVHC2CuXai1dgQAdYUCHUYKe5uPkIO9i', 'visitor2@example.com', 'Visitor', 'Two', 'Nelson', NULL, 'visitor', 'active'),
('visitor3', '$2b$12$uw9DwEh18P0RhaGyzZ1Lvu1AJ.PGsxhdcQ4cga1aC2..FFhJqOiWm', 'visitor3@example.com', 'Visitor', 'Three', 'Rotorua', NULL, 'visitor', 'active'),
('visitor4', '$2b$12$A9spdgZ3fXRdePt4M2U3juXtG4B1q0v2QM43AaEGQAP/qhcDB.JW.', 'visitor4@example.com', 'Visitor', 'Four', 'New Plymouth', NULL, 'visitor', 'active'),
('visitor5', '$2b$12$QwWTM3Prq0.iLo3nhiYT7e62fRbRGs4x8Z3urMALiDiT9Vtq2nbai', 'visitor5@example.com', 'Visitor', 'Five', 'Whangarei', NULL, 'visitor', 'active'),
('visitor6', '$2b$12$HwG1WWnV64vrTDNMIBuikuW2BoPz3b/rS2LeDXRH8BcYzggHZGXZC', 'visitor6@example.com', 'Visitor', 'Six', 'Invercargill', NULL, 'visitor', 'active'),
('visitor7', '$2b$12$G9OXVaH25m1bKa20Hay.vO1W4m.xoxDxsjnhRYlE4ras/Gc.UqZ16', 'visitor7@example.com', 'Visitor', 'Seven', 'Whanganui', NULL, 'visitor', 'active'),
('visitor8', '$2b$12$JSC.qtFvMpKZgK0mA17YHuSr3yAO/v6aMcqf86sctzkw3tDVq2rjy', 'visitor8@example.com', 'Visitor', 'Eight', 'Gisborne', NULL, 'visitor', 'active'),
('visitor9', '$2b$12$TB91mxJhiBqHlPeKOCIe1eTSKyB4oZnNdp5CJFL3UY7d8WoEDXPFG', 'visitor9@example.com', 'Visitor', 'Nine', 'Queenstown', NULL, 'visitor', 'active'),
('visitor10', '$2b$12$843aVQ6rbWKRNlVOOFqs1ecL55vNeecWhykz8TvLnG0XbohbtTsvq', 'visitor10@example.com', 'Visitor', 'Ten', 'Blenheim', NULL, 'visitor', 'active'),
('visitor11', '$2b$12$r9Fdh1hmEB1gJwbBbVPYA.M5XcA9y9h7SyhdDWR0TMCBRrfGmNThe', 'visitor11@example.com', 'Visitor', 'Eleven', 'Timaru', NULL, 'visitor', 'active'),
('visitor12', '$2b$12$9vWmUdrtSJXm/0M1Bl15zOX4SuYuDEYlVqbgHU3Gx9buTkL8jKowW', 'visitor12@example.com', 'Visitor', 'Twelve', 'Taupo', NULL, 'visitor', 'active'),
('visitor13', '$2b$12$4Qmymvo8gCTeq0DGIctUCO0TNPjiXtyvwP5G5XP1htSHnB3wbuceq', 'visitor13@example.com', 'Visitor', 'Thirteen', 'Whakatane', NULL, 'visitor', 'active'),
('visitor14', '$2b$12$Y63mtkeOaWWFYj6Iu4jeceuOcJp7eMJzkPUi3eyI8FAYdMswo05Za', 'visitor14@example.com', 'Visitor', 'Fourteen', 'Cambridge', NULL, 'visitor', 'active'),
('visitor15', '$2b$12$OpSAzhKg6tdYqrW85.hlfO44MJwoIlL.0tOXRbewdS.PTjswo4J2q', 'visitor15@example.com', 'Visitor', 'Fifteen', 'Te Awamutu', NULL, 'visitor', 'active'),
('visitor16', '$2b$12$P6fuw3hf0B8/6/rQR4xb3O4arZWCiOJxJeYjY2XhYEuWhTplQczUG', 'visitor16@example.com', 'Visitor', 'Sixteen', 'Oamaru', NULL, 'visitor', 'active'),
('visitor17', '$2b$12$b/IyyqhdOQVkz/j/lcUK3O0s5CkRmH2ZaRcisdd5yMVElsodlFIpa', 'visitor17@example.com', 'Visitor', 'Seventeen', 'Ashburton', NULL, 'visitor', 'active'),
('visitor18', '$2b$12$gjclvz12wbk349FIsiDTi.JhqdU0cOU09ESNf.MI1XUqRUDESxzOq', 'visitor18@example.com', 'Visitor', 'Eighteen', 'Levin', NULL, 'visitor', 'active'),
('visitor19', '$2b$12$XMzENUEcoW3w.a41bT3jveoFQR5G6qeNEKxa1h1YHSjNs/3MTOscu', 'visitor19@example.com', 'Visitor', 'Nineteen', 'Kapiti', NULL, 'visitor', 'active'),
('visitor20', '$2b$12$cVgxmBbVgIjM2uxp1bdWReSWD/dM5UWatNSLJSP82qcpn2ar2lL1i', 'visitor20@example.com', 'Visitor', 'Twenty', 'Paraparaumu', NULL, 'visitor', 'active');

-- Populate issues table (20 issues total)
INSERT INTO `issues` (`user_id`, `summary`, `description`, `created_at`, `status`) VALUES
(8, 'LCC WiFi connection not working', 'The WiFi at Lincoln Community Campground is not connecting for any devices. I have tried with multiple devices and the signal shows but cannot connect. This is affecting all campers in the central area.', '2024-02-01 10:00:00', 'new'),
(10, 'Shower water not heating properly', 'The shower water in the main facilities block is only lukewarm at best. It was working fine yesterday but this morning it never got properly hot even after running for 10 minutes. Multiple campers have reported the same issue.', '2024-02-02 11:30:00', 'open'),
(12, 'Toilet facilities blocked in north area', 'The toilets in the north area facilities block appear to be blocked. Water is rising to the rim when flushed and there is an unpleasant odor. All three stalls in the men''s restroom are affected.', '2024-02-03 09:15:00', 'stalled'),
(14, 'Solar charging station not functioning', 'The solar charging station near campsite #10 is not working at all. The indicator lights are not coming on even during full sunlight. I checked all the ports and none are providing power to devices.', '2024-02-04 14:20:00', 'resolved'),
(15, 'Fire pit area needs cleaning', 'The main community fire pit area needs cleaning. There is excessive ash buildup and some unburned logs from previous users. Also noticed some trash left behind that should be removed before tonight''s gathering.', '2024-02-05 16:45:00', 'new'),
(16, 'Outdoor cooking equipment missing parts', 'The outdoor BBQ grill in the common cooking area is missing the propane regulator and some of the cooking grates. Without these parts, it''s impossible to use properly for meal preparation.', '2024-02-06 13:10:00', 'open'),
(17, 'Camping area flooded after rain', 'After last night''s heavy rain, the lower camping area (sites #15-20) has significant flooding. There is standing water around tents and the ground is extremely muddy. May need drainage assistance or to close this area temporarily.', '2024-02-07 11:25:00', 'stalled'),
(18, 'Noise complaint from neighboring campers', 'A group at campsite #8 was playing loud music and talking loudly past midnight, ignoring the quiet hours policy. Several families with children were disturbed and couldn''t sleep. This has happened two nights in a row.', '2024-02-08 10:30:00', 'new'),
(19, 'Request for additional fire wood', 'The community firewood pile is nearly depleted. With the cooler evening temperatures, many campers are planning to use the fire pits tonight. Could we get a delivery of additional firewood before evening?', '2024-02-09 15:40:00', 'open'),
(20, 'Garbage bins need emptying', 'The garbage and recycling bins near the main entrance are overflowing. They haven''t been emptied for several days and are attracting insects. Some trash has been scattered by wind or possibly animals.', '2024-02-10 12:50:00', 'resolved'),
(9, 'Main entrance gate difficult to open', 'The main entrance gate is very difficult to open and close. The hinges seem rusted and it requires significant force to move. An elderly camper was struggling with it this morning and needed assistance.', '2024-02-11 09:20:00', 'new'),
(11, 'Wildlife spotted near camping area', 'I spotted what appears to be a wild possum near campsite #12 early this morning. It didn''t seem afraid of people and was rummaging through some improperly stored food. Other campers should be warned to secure their food supplies.', '2024-02-12 14:15:00', 'stalled'),
(13, 'Request for campground map/information', 'I''m a first-time visitor to Lincoln Community Campground and can''t locate a detailed map of the facilities. The one posted at the entrance is weathered and unreadable. Could a digital or new printed version be made available?', '2024-02-13 16:30:00', 'open'),
(7, 'Tree branches hanging dangerously low', 'There are several large tree branches hanging very low over campsite #3 after the recent windstorm. They look precarious and could potentially fall on tents or people. These should be addressed by someone with proper equipment.', '2024-02-14 11:45:00', 'resolved'),
(6, 'Lost and found item report', 'I found a child''s stuffed toy bear near the playground area yesterday evening. It appears well-loved and someone is likely missing it. I''ve placed it on the lost and found shelf in the common room but wanted to report it here as well.', '2024-02-15 10:55:00', 'new'),
(5, 'Water tap leaking near site #5', 'The outdoor water tap near campsite #5 has a constant drip that''s creating a muddy puddle. I tried to turn it off completely but it continues to leak. May need a new washer or other repair.', '2024-02-16 13:25:00', 'open'),
(4, 'Request for quiet hours enforcement', 'Could we please have better enforcement of the quiet hours between 10pm and 7am? Several groups have been ignoring these guidelines on weekends, making it difficult for families with young children to get proper rest.', '2024-02-17 15:35:00', 'stalled'),
(3, 'Path lighting not working at night', 'The solar path lights along the main walkway from the parking area to the campsites aren''t working. I arrived after dark yesterday and had difficulty navigating safely to my site. All lights appear to be out, not just one or two.', '2024-02-18 12:40:00', 'new'),
(2, 'Picnic table damaged at site #8', 'The wooden picnic table at campsite #8 has a broken bench seat on one side. The wood has split and has some protruding splinters that could cause injury. Table needs repair or replacement before the site is used again.', '2024-02-19 09:50:00', 'open'),
(1, 'Question about local hiking trails', 'Are there any good hiking trails within walking distance of Lincoln Community Campground? I''d appreciate information about trail difficulty, length, and directions to access points from the campground. Planning a day hike tomorrow.', '2024-02-20 14:05:00', 'resolved');

-- Populate comments table (20 comments total)
INSERT INTO `comments` (`issue_id`, `user_id`, `content`, `created_at`) VALUES
(1, 3, 'This WiFi issue has been reported by multiple campers. I will check the router and access points today.', '2024-02-20 14:30:00'),
(1, 4, 'I have reset the router and checked all access points. The main router needed a firmware update which has been completed. Please let me know if the problem persists.', '2024-02-20 15:45:00'),
(1, 1, 'WiFi issue has been resolved. Signal strength has been improved across the campground.', '2024-02-20 16:30:00'),
(2, 5, 'Can you please provide your campsite number so I can check the closest shower facilities?', '2024-02-19 10:15:00'),
(2, 2, 'I am at campsite #7, using the main shower block.', '2024-02-19 10:30:00'),
(3, 6, 'The subscription cancellation option for toilet issues should be under Account Settings. I mean, you can find the plunger in the maintenance shed near the office.', '2024-02-18 13:00:00'),
(4, 7, 'Our maintenance volunteer is investigating the solar charging station. Initial assessment suggests it may be an inverter issue.', '2024-02-17 16:00:00'),
(4, 8, 'The issue with the solar charging station has been identified. The controller has failed and a replacement has been ordered. Should arrive within 3 days.', '2024-02-17 17:15:00'),
(7, 9, 'Which campsite are you at that experienced flooding?', '2024-02-07 12:00:00'),
(7, 17, 'We are at site #17, the water is about 5cm deep in some areas.', '2024-02-07 12:30:00'),
(10, 10, 'The garbage bins have been emptied and the area has been cleaned. We will increase collection frequency during busy periods.', '2024-02-10 13:15:00'),
(10, 20, 'Thank you for the quick response. The area looks much better now.', '2024-02-10 14:00:00'),
(11, 11, 'What kind of device are you using with the charging station? Some older devices may not be compatible.', '2024-02-12 14:45:00'),
(12, 12, 'Have you tried using the other fire pit area while this one is being cleaned?', '2024-02-03 10:00:00'),
(13, 13, 'The BBQ parts have been located. They were incorrectly stored in the tool shed. All equipment should now be available for use.', '2024-02-13 17:00:00'),
(14, 14, 'The drainage channels in the lower camping area have been cleared. The standing water should recede over the next few hours.', '2024-02-04 15:00:00'),
(15, 15, 'I have spoken to the group at campsite #8 about the noise complaints. They have agreed to respect quiet hours going forward.', '2024-02-05 17:00:00'),
(16, 16, 'A volunteer will check all path lighting fixtures tomorrow. For tonight, we have placed temporary battery-powered lanterns along the main paths.', '2024-02-06 14:00:00'),
(18, 18, 'The picnic table at campsite #8 has been repaired. The split bench has been replaced with new wood and all splinters removed.', '2024-02-08 11:00:00'),
(19, 19, 'I have updated our campground map with information about local hiking trails, including difficulty levels and distances. It is now available at the information board near the office.', '2024-02-09 16:00:00'),
(20, 20, 'The session timeout period for reporting issues has been increased to prevent lost submissions when users take time to write detailed descriptions.', '2024-02-10 13:30:00');