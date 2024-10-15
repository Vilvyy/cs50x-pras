-- Keep a log of any SQL queries you execute as you solve the mystery.

select * from crime_scene_reports where month = 7 and day = 28 and street = "Humphrey Street"; -- witness said something about bakery so lets check it
-- 10.15 AM

select * from bakery_security_logs where month = 7 and day = 28 and hour >= 8; -- check for a few hours before the incident

select  from interviews where month = 7 and day = 28; -- ruth said after around 10 minutes they took off from the bakery
-- eugene recognized one of the thief's, they took out some money from the ATM at "Leggett Street"
-- raymond said they planned to leave at the earliest flight tommorow, and tell the person at the other end of the phone to book a ticket. the call took less than a minute

select * from bakery_security_logs where month = 7 and day = 28 and hour >= 8;
-- | 264 | 2023 | 7     | 28  | 10   | 20     | exit     | G412CB7       |
-- | 265 | 2023 | 7     | 28  | 10   | 21     | exit     | L93JTIZ       |
-- | 266 | 2023 | 7     | 28  | 10   | 23     | exit     | 322W7JE       |
-- | 267 | 2023 | 7     | 28  | 10   | 23     | exit     | 0NTHK55       |
-- | 268 | 2023 | 7     | 28  | 10   | 35     | exit     | 1106N58       |
-- should be around 10.25 AM

select * from phone_calls where month = 7 and day = 28 and duration < 60;
-- +-----+----------------+----------------+------+-------+-----+----------+
-- | id  |     caller     |    receiver    | year | month | day | duration |
-- +-----+----------------+----------------+------+-------+-----+----------+
-- | 221 | (130) 555-0289 | (996) 555-8899 | 2023 | 7     | 28  | 51       |
-- | 224 | (499) 555-9472 | (892) 555-8872 | 2023 | 7     | 28  | 36       |
-- | 233 | (367) 555-5533 | (375) 555-8161 | 2023 | 7     | 28  | 45       |
-- | 251 | (499) 555-9472 | (717) 555-1342 | 2023 | 7     | 28  | 50       |
| 254 | (286) 555-6063 | (676) 555-6554 | 2023 | 7     | 28  | 43       |
| 255 | (770) 555-1861 | (725) 555-3243 | 2023 | 7     | 28  | 49       |
-- | 261 | (031) 555-6622 | (910) 555-3251 | 2023 | 7     | 28  | 38       |
-- | 279 | (826) 555-1652 | (066) 555-9701 | 2023 | 7     | 28  | 55       |
-- | 281 | (338) 555-6650 | (704) 555-2131 | 2023 | 7     | 28  | 54       |
-- +-----+----------------+----------------+------+-------+-----+----------+


select * from atm_transactions where month = 7 and day = 28 and atm_location = "Leggett Street";
-- +-----+----------------+------+-------+-----+----------------+------------------+--------+
-- | id  | account_number | year | month | day |  atm_location  | transaction_type | amount |
-- +-----+----------------+------+-------+-----+----------------+------------------+--------+
-- | 246 | 28500762       | 2023 | 7     | 28  | Leggett Street | withdraw         | 48     |
-- | 264 | 28296815       | 2023 | 7     | 28  | Leggett Street | withdraw         | 20     |
-- | 266 | 76054385       | 2023 | 7     | 28  | Leggett Street | withdraw         | 60     |
-- | 267 | 49610011       | 2023 | 7     | 28  | Leggett Street | withdraw         | 50     |
-- | 269 | 16153065       | 2023 | 7     | 28  | Leggett Street | withdraw         | 80     |
-- | 275 | 86363979       | 2023 | 7     | 28  | Leggett Street | deposit          | 10     |
-- | 288 | 25506511       | 2023 | 7     | 28  | Leggett Street | withdraw         | 20     |
-- | 313 | 81061156       | 2023 | 7     | 28  | Leggett Street | withdraw         | 30     |
-- | 336 | 26013199       | 2023 | 7     | 28  | Leggett Street | withdraw         | 35     |
-- +-----+----------------+------+-------+-----+----------------+------------------+--------+


SELECT people.name
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.account_number IN (26013199, 81061156, 25506511, 16153065, 49610011, 76054385, 28296815, 28500762) AND atm_transactions.month = 7;
-- get the name for the transactions at 28 July
-- +---------+
-- |  name   |
-- +---------+
-- | Bruce   |
-- | Diana   |
-- | Brooke  |
-- | Kenny   |
-- | Iman    |
-- | Luca    |
-- | Taylor  |
-- | Benista |
-- +---------+

SELECT name, license_plate, phone_number FROM people WHERE name IN ("Bruce", "Diana", "Brooke", "Kenny", "Iman", "Luca", "Taylor", "Benista")
AND license_plate IN ("G412CB7", "L93JTIZ", "322W7JE", "0NTHK55", "1106N58");
-- get the name for the driver and potential caller
-- +--------+---------------+----------------+
-- |  name  | license_plate |  phone_number  |
-- +--------+---------------+----------------+
-- | Iman   | L93JTIZ       | (829) 555-5269 |
-- | Taylor | 1106N58       | (286) 555-6063 |
-- | Diana  | 322W7JE       | (770) 555-1861 |
-- +--------+---------------+----------------+

sqlite> SELECT * FROM people WHERE phone_number IN ("(676) 555-6554", "(725) 555-3243");
-- getting the receiver
-- +--------+--------+----------------+-----------------+---------------+
-- |   id   |  name  |  phone_number  | passport_number | license_plate |
-- +--------+--------+----------------+-----------------+---------------+
-- | 250277 | James  | (676) 555-6554 | 2438825627      | Q13SVG6       |
-- | 847116 | Philip | (725) 555-3243 | 3391710505      | GW362R6       |
-- +--------+--------+----------------+-----------------+---------------+

SELECT people.name
FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN airports ON flights.origin_airport_id = airports.id
JOIN flights ON passengers.flight_id = flights.id
WHERE passengers.passport_number IN (7049073643, 1988161715, 3592750733) AND flights.id IN (36);


