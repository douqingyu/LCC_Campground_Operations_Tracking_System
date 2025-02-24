-- Populate users table with required number of users (20 visitors, 5 helpers, 2 admins)
INSERT INTO `users` (`username`, `password_hash`, `email`, `first_name`, `last_name`, `location`, `profile_image`, `role`, `status`) VALUES
-- Administrators (2)
('admin1', '$2b$12$TMZW44wzSX9lV6GLH.dT.eogY1fWqI.6WqRDD.thFEFwm45VJbuQK', 'admin1@example.com', 'Admin', 'One', 'New York', 'admin1.jpg', 'admin', 'active'),
('admin2', '$2b$12$pB7eB78VMuf1fUledgbunOdrzecp.YfJ7kXSHFSK9/y2guPghBQ/m', 'admin2@example.com', 'Admin', 'Two', 'Los Angeles', 'admin2.jpg', 'admin', 'active'),

-- Helpers (5)
('helper1', '$2b$12$wpRN0Z8q1bgs7GyaI3hP2O9YmEXmkIKLo08piK4JJv1cHNO/CGJNe', 'helper1@example.com', 'Helper', 'One', 'Chicago', 'helper1.jpg', 'helper', 'active'),
('helper2', '$2b$12$ccQc9exlc6EmVbTAifSPpeVH6QAyo9FXI21vFnW3wpVXyeSYjuXMS', 'helper2@example.com', 'Helper', 'Two', 'Houston', 'helper2.jpg', 'helper', 'active'),
('helper3', '$2b$12$Ve.3F3fmzAROz/4YJUpowuRGchMhMTHdlANkEOf5j6h.OconRUnLm', 'helper3@example.com', 'Helper', 'Three', 'Phoenix', 'helper3.jpg', 'helper', 'active'),
('helper4', '$2b$12$/gi.aItAcnWfLA5Q6wWkRu9wwpaUMDEunRDFDU725vLAzsLGf.SzS', 'helper4@example.com', 'Helper', 'Four', 'Philadelphia', 'helper4.jpg', 'helper', 'active'),
('helper5', '$2b$12$F861UGSjuwSqrFH0bfYLLenLi1bQNb93gtIEZTfAp8AqNfhJgkl7.', 'helper5@example.com', 'Helper', 'Five', 'San Antonio', 'helper5.jpg', 'helper', 'active'),

-- Visitors (20)
('visitor1', '$2b$12$lkQXcXEQJDCwPVWxcvkWDuSKqIYv09mazHpDkkBaAY.oQYroXANYG', 'visitor1@example.com', 'Visitor', 'One', 'San Diego', 'visitor1.jpg', 'visitor', 'active'),
('visitor2', '$2b$12$WabCu9ux4mdxgxmgdMsKaee4PwwSlOMf4jtPmF0Mp1j.I6nqgKRA2', 'visitor2@example.com', 'Visitor', 'Two', 'Dallas', 'visitor2.jpg', 'visitor', 'active'),
('visitor3', '$2b$12$E/vPsO/OYJgfivrHcGI74.RWMO6lh8LPZOvCEgM0CyXE6/Ft6bQJ.', 'visitor3@example.com', 'Visitor', 'Three', 'San Jose', 'visitor3.jpg', 'visitor', 'active'),
('visitor4', '$2b$12$zRjIuIZ21sCvwftZr7fLE.YRmlbWJhKzrLToAkEklTFJrH2HPe9nm', 'visitor4@example.com', 'Visitor', 'Four', 'Austin', 'visitor4.jpg', 'visitor', 'active'),
('visitor5', '$2b$12$aCz1ztS4OWgeNlNKQEgNLecz7KqrboRz4Pw8qG6yAQnvUQ2HQHVrK', 'visitor5@example.com', 'Visitor', 'Five', 'Jacksonville', 'visitor5.jpg', 'visitor', 'active'),
('visitor6', '$2b$12$8QHHMpe8DkyXGswi.KRES.QYmCcXrcTqKwm8GWP4OiAc2PE5nbY3q', 'visitor6@example.com', 'Visitor', 'Six', 'Fort Worth', 'visitor6.jpg', 'visitor', 'active'),
('visitor7', '$2b$12$TJ973YRt7eFNNTy9iGuMiuUsDGxISV9vRuqnsuKCHRw0lJOW/nlQO', 'visitor7@example.com', 'Visitor', 'Seven', 'Columbus', 'visitor7.jpg', 'visitor', 'active'),
('visitor8', '$2b$12$U1vmG9tR73IsYxwXQa0xbOMQFveelNNJCRk0kcMOZKTiEB8ThLbbC', 'visitor8@example.com', 'Visitor', 'Eight', 'San Francisco', 'visitor8.jpg', 'visitor', 'active'),
('visitor9', '$2b$12$A4L7X8gZa7elVUe.mKL4a.KembH4/INpOcx05PMedqpWi56jXBzAe', 'visitor9@example.com', 'Visitor', 'Nine', 'Charlotte', 'visitor9.jpg', 'visitor', 'active'),
('visitor10', '$2b$12$yQ/AnwwKBvkKGMQ7pGpHZ.4hd8Um8WjpelBVKCr8UF.f99.O/B3x6', 'visitor10@example.com', 'Visitor', 'Ten', 'Indianapolis', 'visitor10.jpg', 'visitor', 'active'),
('visitor11', '$2b$12$KT6FjEOfhCsS8e1SrhQGnBvVL5cBCT2', 'visitor11@example.com', 'Visitor', 'Eleven', 'Seattle', 'visitor11.jpg', 'visitor', 'active'),
('visitor12', '$2b$12$KT6FjEOfhCsS8e1SrhQGnBvVL5cBCT2', 'visitor12@example.com', 'Visitor', 'Twelve', 'Denver', 'visitor12.jpg', 'visitor', 'active'),
('visitor13', '$2b$12$KT6FjEOfhCsS8e1SrhQGnBvVL5cBCT2', 'visitor13@example.com', 'Visitor', 'Thirteen', 'Washington', 'visitor13.jpg', 'visitor', 'active'),
('visitor14', '$2b$12$KT6FjEOfhCsS8e1SrhQGnBvVL5cBCT2', 'visitor14@example.com', 'Visitor', 'Fourteen', 'Boston', 'visitor14.jpg', 'visitor', 'active'),
('visitor15', '$2b$12$KT6FjEOfhCsS8e1SrhQGnBvVL5cBCT2', 'visitor15@example.com', 'Visitor', 'Fifteen', 'El Paso', 'visitor15.jpg', 'visitor', 'active'),
('visitor16', '$2b$12$KT6FjEOfhCsS8e1SrhQGnBvVL5cBCT2', 'visitor16@example.com', 'Visitor', 'Sixteen', 'Portland', 'visitor16.jpg', 'visitor', 'active'),
('visitor17', '$2b$12$KT6FjEOfhCsS8e1SrhQGnBvVL5cBCT2', 'visitor17@example.com', 'Visitor', 'Seventeen', 'Detroit', 'visitor17.jpg', 'visitor', 'active'),
('visitor18', '$2b$12$KT6FjEOfhCsS8e1SrhQGnBvVL5cBCT2', 'visitor18@example.com', 'Visitor', 'Eighteen', 'Memphis', 'visitor18.jpg', 'visitor', 'active'),
('visitor19', '$2b$12$KT6FjEOfhCsS8e1SrhQGnBvVL5cBCT2', 'visitor19@example.com', 'Visitor', 'Nineteen', 'Nashville', 'visitor19.jpg', 'visitor', 'active'),
('visitor20', '$2b$12$dM1qd.TEFMmExwVBqYvDde03Tx8sxIriU6CuCCRbiXM7PhjECvZ6W', 'visitor20@example.com', 'Visitor', 'Twenty', 'Oklahoma City', 'visitor20.jpg', 'visitor', 'active');

-- Populate issues table (20 issues total)
INSERT INTO `issues` (`user_id`, `summary`, `description`, `created_at`, `status`) VALUES
(8, 'Login page not responding', 'When I try to access the login page, it takes too long to load', '2024-02-01 10:00:00', 'new'),
(10, 'Cannot reset password', 'The reset password link in my email is not working', '2024-02-02 11:30:00', 'open'),
(12, 'Profile picture upload fails', 'Getting an error when trying to upload a new profile picture', '2024-02-03 09:15:00', 'stalled'),
(14, 'Error 404 on checkout', 'Receiving 404 error when trying to complete purchase', '2024-02-04 14:20:00', 'resolved'),
(15, 'Missing order confirmation', 'Did not receive order confirmation email', '2024-02-05 16:45:00', 'new'),
(16, 'Account verification issue', 'Cannot verify my email address', '2024-02-06 13:10:00', 'open'),
(17, 'Payment declined error', 'Valid credit card being declined', '2024-02-07 11:25:00', 'stalled'),
(18, 'Cannot update shipping address', 'Address update form not saving changes', '2024-02-08 10:30:00', 'new'),
(19, 'Product search not working', 'Search results not displaying correctly', '2024-02-09 15:40:00', 'open'),
(20, 'Cart items disappeared', 'Items in cart vanished after session timeout', '2024-02-10 12:50:00', 'resolved'),
(9, 'Invoice PDF not generating', 'Cannot download invoice in PDF format', '2024-02-11 09:20:00', 'new'),
(11, 'Mobile app crashes on startup', 'App crashes immediately after launch on iPhone', '2024-02-12 14:15:00', 'stalled'),
(13, 'Cannot apply discount code', 'Valid promotion code showing as invalid', '2024-02-13 16:30:00', 'open'),
(7, 'Newsletter subscription failed', 'Getting error when trying to subscribe to newsletter', '2024-02-14 11:45:00', 'resolved'),
(6, 'Account locked message', 'Cannot access account due to security lock', '2024-02-15 10:55:00', 'new'),
(5, 'Product images not loading', 'Product page shows broken image icons', '2024-02-16 13:25:00', 'open'),
(4, 'Shipping calculation error', 'Incorrect shipping costs being displayed', '2024-02-17 15:35:00', 'stalled'),
(3, 'Cannot cancel subscription', 'No option to cancel recurring subscription', '2024-02-18 12:40:00', 'new'),
(2, 'Wrong order delivered', 'Received incorrect items in my order', '2024-02-19 09:50:00', 'open'),
(1, 'Site not mobile responsive', 'Website layout broken on mobile devices', '2024-02-20 14:05:00', 'resolved');

-- Populate comments table (20 comments total, some issues with multiple comments, some with none)
INSERT INTO `comments` (`issue_id`, `user_id`, `content`, `created_at`) VALUES
(1, 3, 'This issue has been reported by multiple users. Looking into it.', '2024-02-20 14:30:00'),
(1, 4, 'Mobile responsiveness fix deployed to testing environment.', '2024-02-20 15:45:00'),
(1, 1, 'Fix has been verified and pushed to production.', '2024-02-20 16:30:00'),
(2, 5, 'Can you provide your order number for reference?', '2024-02-19 10:15:00'),
(2, 2, 'Order number is #12345', '2024-02-19 10:30:00'),
(3, 6, 'Subscription cancellation option should be under Account Settings.', '2024-02-18 13:00:00'),
(4, 7, 'Engineering team is investigating the calculation logic.', '2024-02-17 16:00:00'),
(4, 8, 'Fix identified, will be deployed in next release.', '2024-02-17 17:15:00'),
(7, 9, 'Which payment method are you using?', '2024-02-07 12:00:00'),
(7, 17, 'Using Visa card ending in 4321', '2024-02-07 12:30:00'),
(10, 10, 'This has been fixed in the latest update', '2024-02-10 13:15:00'),
(10, 20, 'Can confirm the fix is working now', '2024-02-10 14:00:00'),
(11, 11, 'What iOS version are you using?', '2024-02-12 14:45:00'),
(12, 12, 'Have you cleared your browser cache?', '2024-02-03 10:00:00'),
(13, 13, 'The promotion code expired yesterday', '2024-02-13 17:00:00'),
(14, 14, 'Issue resolved - server restored', '2024-02-04 15:00:00'),
(15, 15, 'Please check your spam folder', '2024-02-05 17:00:00'),
(16, 16, 'Verification email resent to your address', '2024-02-06 14:00:00'),
(18, 18, 'This is a known issue being worked on', '2024-02-08 11:00:00'),
(19, 19, 'Search functionality has been restored', '2024-02-09 16:00:00'),
(20, 20, 'Session timeout period has been increased', '2024-02-10 13:30:00');