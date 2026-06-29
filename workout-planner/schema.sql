pragma foreign_keys  = on;
drop table if exists users;
drop table if exists schedule;
drop table if exists workout;
drop table if exists forgot_pass;
drop table if exists workout_log;



create table users (
 id integer primary key autoincrement,
 username text not null,
 password text not null,
 email text not null,
 experience text,
 goals integer,
 frequency integer,
 part_of_the_day integer,
 body text,
 weight float,
 height float
);

create table forgot_pass (
    id integer primary key autoincrement,
    username text not null,
    email text not null,
    url text not null
);



create table schedule (
 id integer primary key autoincrement,
 username text not null,
 Monday text,
 Tuesday text,
 Wednesday text,
 Thursday text,
 Friday text,
 Saturday text,
 Sunday text
);



create table workout (
 id integer primary key autoincrement,
 workout_name text not null,
 muscle text not null,
 weighted bit default 0,
 goals integer default 0,
 experience integer not null,
 recommended_weight_kg INTEGER default NULL,
 video BLOB,
 user_id integer,
 is_current bit default 0,
 time_minutes integer,
 user_weight_kg float
);

create table workout_log (
 id integer primary key autoincrement,
 user_id integer not null,
 log_date text not null,
 day_name text,
 start_time integer,
 end_time integer,
 weight_kg float,
 notes text,
 UNIQUE(user_id, log_date)
);

INSERT INTO workout (workout_name, muscle, weighted, goals, experience, recommended_weight_kg, video) VALUES ('Dumbbell shoulder press','shoulder',1,1,1,10, ('static/videos/shoulders/shoulder_press'));
INSERT INTO workout (workout_name, muscle, weighted, goals, experience, recommended_weight_kg, video) VALUES ('Cable side raise','shoulder',1,4,1,5, ('static/videos/shoulders/cable_side_raise'));
INSERT INTO workout (workout_name, muscle, weighted, goals, experience, recommended_weight_kg, video) VALUES ('Cable front raise','shoulder',1,4,1,5, ('static/videos/shoulders/cable_front_raise'));
INSERT INTO workout (workout_name, muscle, weighted, goals, experience, recommended_weight_kg, video) VALUES ('Smith machine shoulder press','shoulder',1,1,2,30, ('static/videos/shoulders/smith_machine_shoulder_press'));
INSERT INTO workout (workout_name, muscle, weighted, goals, experience, recommended_weight_kg, video) VALUES ('Arnold press','shoulder',1,4,2,13.61, ('static/videos/shoulders/arnold_press'));
INSERT INTO workout (workout_name, muscle, weighted, goals, experience, recommended_weight_kg, video) VALUES ('Barbell front raise', 'shoulder',1,4,1,15, ('static/videos/shoulders/barbell_front_raise'));
INSERT INTO workout (workout_name, muscle, weighted, goals, experience, recommended_weight_kg, video) VALUES('Overhead barbell press','shoulder',1,4,1,20, ('static/videos/shoulders/overhead_barbell_press'));
INSERT INTO workout (workout_name, muscle, weighted, goals, experience, recommended_weight_kg, video) VALUES ('External rotater cuff','shoulder',1,1,1,5, ('static/videos/shoulders/external_rotation'));
INSERT INTO workout (workout_name, muscle, weighted, goals, experience, video) VALUES ('Plank_up_and_downs','shoulder',0,3,3, ('static/videos/shoulders/plank_up_and_downs'));
INSERT INTO workout (workout_name, muscle, weighted, goals, experience, video) VALUES ('Cable shoulder press','shoulder',1,1,1, ('static/videos/shoulders/cable_shoulder_press'));




INSERT INTO workout (workout_name, muscle, weighted, goals, experience, recommended_weight_kg, video) VALUES
('crunches', 'abs', 0, 0, 1, null, ('static/videos/abs/crunch')),
( 'russian twists', 'abs', 1, 0, 1, 5, ('static/videos/abs/russian_twist')),
( 'planks ups','abs', 0, 0, 1, null, ('static/videos/abs/plank_ups')),
( 'decline crunches', 'abs', 0, 0, 3, null, ('static/videos/abs/decline_crunch')),
( 'alternate_plank', 'abs', 0, 0, 2, null, ('static/videos/abs/alternate_plank')),
( 'knee tuck crunch', 'abs', 0, 0, 2, null, ('static/videos/abs/knee_tuck_crunch')),
( 'weighted_crunch', 'abs', 1, 0, 1, 10, ('static/videos/abs/weighted_crunch')),
( 'partner_crunch', 'abs', 0, 0, 3, null, ('static/videos/abs/partner_crunch')),
( 'alternating_leg_raise', 'abs', 0, 0, 2, null, ('static/videos/abs/alternating_leg_raise')),
( 'v-ups', 'abs', 0,0,2,null, ('static/videos/abs/v_crunch')),
( 'lying_leg_lift', 'abs', 0,0, 1, 0, ('static/videos/abs/lying_leg_lift')),
( 'mountain_climbers', 'abs', 1, 0, 3, 5, ('static/videos/abs/mountain_climbers')),
( 'oblique_crunch', 'abs', 1, 0, 3, 5, ('static/videos/abs/oblique_crunch')),
( 'toe_tap_crunch', 'abs', 0, 0, 2, null, ('static/videos/abs/toe_tap_crunch')),
( 'weighted starfish', 'abs', 0, 0 ,1, null, ('static/videos/abs/weighted_starfish_crunch')),
( 'spider plank', 'abs', 0, 0, 2, null, ('static/videos/abs/spider_plank')),
( 'unweighted_russian_twist', 'abs', 0, 0, 1, null, ('static/videos/abs/unweighted_russian_twist')),
( 'superman', 'abs', 0, 0, 3, null, ('static/videos/abs/superman')),
( 'plank pushup', 'abs', 0, 0, 2, null, ('static/videos/abs/plank_pushup')),
( 'dead bugs', 'abs', 0, 0, 2, null, ('static/videos/abs/deadbug'));



insert into workout (workout_name, muscle, weighted, goals, experience, recommended_weight_kg, video) values
('Decline Barbell Bench', 'Chest', 1, 1, 1, 60, ('static/videos/chest/decline_barbell_bench')),
('Flat Barbell Bench', 'Chest', 1, 1, 2, 55, ('static/videos/chest/flat_barbell_bench')),
('Incline Dumbbell Bench', 'Chest', 1, 1, 2, 30, ('static/videos/chest/incline_dumbbell_bench')),
('Decline Dumbbell Bench', 'Chest', 1, 1, 1, 40, ('static/videos/chest/decline_dumbbell_bench')),
('Band Pushup', 'Chest', 0, 1, 2, NULL, ('static/videos/chest/band_pushup')),
('Machine Pec Fly', 'Chest', 1, 1, 2, 25, ('static/videos/chest/machine_pec_fly')),
('Diamond Pushup', 'Chest', 0, 1, 1, NULL, ('static/videos/chest/diamond_pushup')),
('Band Flat Bench', 'Chest', 0, 1, 2, NULL, ('static/videos/chest/band_flat_bench')),
('Incline Smith Machine', 'Chest', 1, 1, 1, 35, ('static/videos/chest/incline_smith_machine')),
('Chest Dip', 'Chest', 0, 1, 1, NULL, ('static/videos/chest/chest_dip')),
('Band Chest Flys', 'Chest', 0, 1, 1, NULL, ('static/videos/chest/band_chest_flys')),
('Decline Smith Machine', 'Chest', 1, 1, 3, 45, ('static/videos/chest/decline_smith_machine')),
('Cable Crossover', 'Chest', 1, 1, 1, 20, ('static/videos/chest/cable_crossover')),
('Low Chest Flys', 'Chest', 1, 1, 2, 15, ('static/videos/chest/low_chest_flys')),
('Flat Smith Machine Bench', 'Chest', 1, 1, 45, 60, ('static/videos/chest/flat_smith_machine_bench')),
('Machine Chest Press', 'Chest', 1, 2, 3, 35, ('static/videos/chest/machine_chest_press')),
('Dumbbell Chest Flys', 'Chest', 1, 1, 1, 15, ('static/videos/chest/dumbbell_chest_flys')),
('Incline Machine Press', 'Chest', 1, 1, 1, 40, ('static/videos/chest/incline_machine_press')),
('Incline Barbell Bench', 'Chest', 1, 1, 0, 30, ('static/videos/chest/incline_barbell_bench')),
('Pushups', 'Chest', 0, 1, 2, NULL, ('static/videos/chest/pushup'));



INSERT INTO workout (workout_name, muscle, weighted, goals, experience, recommended_weight_kg, video) VALUES
('Deadlift', 'Legs', 1, 1, 1, 80, ('static/videos/legs/deadlift')),
('Weighted Glute Bridge', 'Legs', 1, 1, 2, 15, ('static/videos/legs/weighted_glute_bridge')),
('Unweighted Glute Bridge', 'Legs', 0, 4, 3, NULL, ('static/videos/legs/unweighted_glute_bridge')),
('Sprinter Lunge', 'Legs', 0, 1, 1,NULL, ('static/videos/legs/sprinter_lunge')),
('Single Leg Raise', 'Legs', 0, 2, 2, NULL, ('static/videos/legs/single_leg_raise')),
('Band Single Leg Raise', 'Legs', 0, 1, 2, NULL, ('static/videos/legs/band_single_leg_raise')),
('Body Throws', 'Legs', 0, 1, 1, NULL, ('static/videos/legs/body_throws')),
('Goodmornings', 'Legs', 1, 4, 2, 35, ('static/videos/legs/goodmornings')),
('Barbell Split Squat', 'Legs', 1, 1, 1, 35, ('static/videos/legs/barbell_split_squat')),
('Barbell Jefferson Squat', 'Legs', 1, 3, 2, 35, ('static/videos/legs/barbell_jefferson_squat')),
('Front Squat', 'Legs', 1, 3, 3, 50, ('static/videos/legs/front_squat')),
('Back Squat', 'Legs', 1, 5, 3, 60, ('static/videos/legs/back_squat')),
('Barbell Jump Squat', 'Legs', 1, 1, 3, 35, ('static/videos/legs/barbell_jump_squat')),
('Clean and Jerk', 'Legs', 1, 5, 3, 30, ('static/videos/legs/clean_and_jerk')),
('Barbell Snatch', 'Legs', 1, 3, 3, 30, ('static/videos/legs/barbell_snatch')),
('Rack Deadlift', 'Legs', 1, 4, 3, 100, ('static/videos/legs/rack_deadlift')),
('Single Leg Unweighted Deadlift', 'Legs', 0, 3, 3, NULL, ('static/videos/legs/single_leg_unweighted_deadlift')),
('Skater Squat', 'Legs', 0, 5, 3, NULL, ('static/videos/legs/skater_squat')),
('Smith Machine Bulgarian Squat', 'Legs', 1, 5, 2, 30, ('static/videos/legs/smith_machine_bulgarian_squat')),
('Box Jumps', 'Legs', 0, 3, 3, NULL, ('static/videos/legs/box_jumps'));



insert into workout (workout_name, muscle, weighted, goals, experience, recommended_weight_kg, video) values
('Machine Dips', 'Arm', 1, 1, 2, 35, ('static/videos/arms/machine_dips')),
('Skull Crusher', 'Arm', 1, 1, 1, 20, ('static/videos/arms/skullcrushers')),
('Dumbbell Kickbacks', 'Arm', 1, 2, 2, 15, ('static/videos/arms/dumbbell_kickbacks')),
('Diamond Push Up', 'Arm', 0, 1, 3, null, ('static/videos/chest/diamond_pushup')),
('Tricep Kickback', 'Arm', 1, 1, 1, 10, ('static/videos/arms/tricep_kickbacks')),
('Tricep Pushdown', 'Arm', 1, 1, 1, 25, ('static/videos/arms/tricep_pushdown')),
('Single Arm Tricep Pushdown', 'Arm', 1, 1, 1, 10, ('static/videos/arms/cable_kickbacks')),
('Cable Kickbacks', 'Arm', 1, 1, 1, 10, ('static/videos/arms/band_pushups')),
('Dumbbell Curls', 'Arm', 1, 1, 1, 10, ('static/videos/arms/dumbbell_curls')),
('Hammer Curls', 'Arm', 1, 1, 2, 10, ('static/videos/arms/hammer_curls')),
('Concentration Curls', 'Arm', 1, 1, 1, 10, ('static/videos/arms/concentration_curls')),
('Dead Hangs', 'Arm', 0, 1, 1, null, ('static/videos/arms/deadhangs')),
('Dumbbell Overhead Extension', 'Arm', 1, 1, 2, 10, ('static/videos/arms/dumbbell_overhead_extension')),
('Preacher Curls', 'Arm', 1, 1, 1, 10, ('static/videos/arms/preacher_curls')),
('Forearm curls Curls', 'Arm', 1, 1, 1, 10, ('static/videos/arms/forearm_curls')),
('Reverse Forearm Curls', 'Arm', 1, 1, 1, 10, ('static/videos/arms/reverse_forearm_curls')),
('Farmers Walk', 'Arm', 1, 1, 1, 35, ('static/videos/arms/farmer_walk')),
('Bench Supported Tricep Dip', 'Arm', 0, 1, 1, null, ('static/videos/arms/bench_supported_tricep_dips')),
('Wrist Roller', 'Arm', 1, 1, 1, 5, ('static/videos/arms/wrist_roller')),
('Reverse Curls', 'Arm', 1, 1, 2, 15, ('static/videos/arms/reverse_curls'));



insert into workout (workout_name, muscle, weighted, goals, experience, recommended_weight_kg, video) values

('Assisted Chinup','Back', 0, 1, 2, null, ('static/videos/back/assisted_chinup')),
('Assisted Pullup','Back', 0, 1, 2, null, ('static/videos/back/assisted_pullup')),
('Back Extension','Back', 0, 1, 1, null, ('static/videos/back/back_extension')),
('Barbell Row','Back', 1, 1, 1, 35, ('static/videos/back/barbell_row')),
('Barbell Shrugs','Back', 1, 1, 2, 50, ('static/videos/back/barbell_shrugs')),
('Behind Neck Lat Pulldown','Back', 1, 1, 1, 25, ('static/videos/back/behind_neck_lat_pulldown')),
('Bench Assisted Barbell Row','Back', 1, 1, 3, 40, ('static/videos/back/bench_barbell_row')),
('Bench Assisted Dumbbell Row','Back', 1, 1, 2, 25, ('static/videos/back/bench_dumbbell_row')),
('Dumbbell Row','Back', 1, 1, 1, 30, ('static/videos/back/dumbbell_row')),
('Dumbbell Shrugs','Back', 1, 1, 2, 35, ('static/videos/back/dumbbell_shrug')),
('Lat Pulldown','Back', 1, 1, 1, 50, ('static/videos/back/lat_pulldown')),
('Reverse Grip Lat Pulldown','Back', 1, 1, 40, 40, ('static/videos/back/reverse_grip_lat_pulldown')),
('Straight Arm Pulldown','Back', 1, 1, 2, 20, ('static/videos/back/straight_arm_pulldown')),
('Wide Upright Row','Back', 1, 1, 2, 35, ('static/videos/back/wide_upright_row')),
('Pullup','Back', 0, 1, 1, null, ('static/videos/back/pullup')),
('Chinup','Back', 0, 1, 2, null, ('static/videos/back/chinup')),
('Seated Row','Back', 1, 1, 3, 30, ('static/videos/back/seated_row')),
('Cable One Arm Lat Pulldown','Back', 1, 1, 1, 25, ('static/videos/back/cable_one_arm_lat_pulldown')),
('Close Grip Cable Row','Back', 1, 1, 3, 40, ('static/videos/back/close_grip_cable_row')),
('One Arm Cable Row','Back', 1, 1, 1, 25, ('static/videos/back/one_arm_cable_row'));

UPDATE workout SET is_current = 1 WHERE id IN (1, 2, 3);
