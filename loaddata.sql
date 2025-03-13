DELETE FROM Posts;
DROP TABLE IF EXISTS Posts;
DELETE FROM Tags;
DROP TABLE IF EXISTS Tags;
DELETE FROM Categories;
DROP TABLE IF EXISTS Categories;
DELETE FROM Users;
DROP TABLE IF EXISTS Users;
DELETE FROM Comments;
DROP TABLE IF EXISTS Comments;
CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" boolean
);
-- What is this?
CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);
CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);
CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" boolean,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`category_id`) REFERENCES `Categories`(`id`)
);
CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);
CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);
CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);
CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);
CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);
CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);
INSERT INTO Categories ('label')
VALUES ('News');
INSERT INTO Tags ('label')
VALUES ('JavaScript');
INSERT INTO Reactions ('label', 'image_url')
VALUES ('happy', 'https://pngtree.com/so/happy');
-- Dummy Data for Testing Database:
-- User Data
INSERT INTO Users (
    first_name,
    last_name,
    email,
    bio,
    username,
    password,
    profile_image_url,
    created_on,
    active
  )
VALUES (
    'Alice',
    'Smith',
    'alice@example.com',
    'Tech enthusiast and writer',
    'alices',
    'password123',
    'https://example.com/images/alice.jpg',
    '2025-03-01 13:31:41.384415',
    True
  ),
  (
    'Bob',
    'Johnson',
    'bob@example.com',
    'Lover of photography and film',
    'bobj',
    'password123',
    'https://example.com/images/bob.jpg',
    '2025-02-20 13:31:41.384415',
    True
  ),
  (
    'Charlie',
    'Brown',
    'charlie@example.com',
    'Passionate about regenerative farming',
    'charlieb',
    'password123',
    'https://example.com/images/charlie.jpg',
    '2025-02-15 13:31:41.384415',
    True
  ),
  (
    'Diana',
    'Miller',
    'diana@example.com',
    'Synthwave music creator',
    'diana_m',
    'password123',
    'https://example.com/images/diana.jpg',
    '2025-01-30 13:31:41.384415',
    True
  ),
  (
    'Ethan',
    'Williams',
    'ethan@example.com',
    'Game developer and indie creator',
    'ethan_w',
    'password123',
    'https://example.com/images/ethan.jpg',
    '2025-01-10 13:31:41.384415',
    True
  );
-- Categories
INSERT INTO Categories (label)
VALUES ('Technology'),
  ('Photography'),
  ('Sustainability'),
  ('Music'),
  ('Gaming');
-- Posts
INSERT INTO Posts (
    user_id,
    category_id,
    title,
    publication_date,
    image_url,
    content,
    approved
  )
VALUES (
    1,
    1,
    'The Future of AI',
    '2025-03-02',
    'https://example.com/images/ai.jpg',
    'Exploring the impact of AI in daily life.',
    True
  ),
  (
    2,
    2,
    'Darkroom Techniques',
    '2025-02-25',
    'https://example.com/images/darkroom.jpg',
    'Keeping film photography alive.',
    True
  ),
  (
    3,
    3,
    'Regenerative Farming Benefits',
    '2025-02-18',
    'https://example.com/images/farming.jpg',
    'How regenerative farming is changing agriculture.',
    True
  ),
  (
    4,
    4,
    'Synthwave Revival',
    '2025-02-05',
    'https://example.com/images/synthwave.jpg',
    'Why 80s-inspired music is making a comeback.',
    True
  ),
  (
    5,
    5,
    'Game Development Tips',
    '2025-01-15',
    'https://example.com/images/gamedev.jpg',
    'Advice for indie game developers.',
    True
  );
-- Tags
INSERT INTO Tags (label)
VALUES ('AI'),
  ('Film'),
  ('Farming'),
  ('Synthwave'),
  ('Indie Games');
-- Comments
INSERT INTO Comments (post_id, author_id, content)
VALUES (1, 2, 'Great insights on AI!'),
  (
    2,
    3,
    'Love film photography, thanks for sharing!'
  ),
  (3, 4, 'Regenerative farming is the future.'),
  (4, 5, 'Synthwave forever!'),
  (5, 1, 'Really helpful tips, thanks!');
-- Subscriptions
INSERT INTO Subscriptions (follower_id, author_id, created_on)
VALUES (1, 2, '2025-03-03'),
  (2, 3, '2025-03-02'),
  (3, 4, '2025-03-01'),
  (4, 5, '2025-02-28'),
  (5, 1, '2025-02-27');
-- Reactions
INSERT INTO Reactions (label, image_url)
VALUES ('Like', 'https://example.com/images/like.png'),
  ('Love', 'https://example.com/images/love.png'),
  ('Wow', 'https://example.com/images/wow.png'),
  ('Funny', 'https://example.com/images/funny.png'),
  ('Sad', 'https://example.com/images/sad.png');
-- Post Reactions
INSERT INTO PostReactions (user_id, reaction_id, post_id)
VALUES (1, 1, 1),
  -- Alice likes AI article
  (2, 2, 2),
  -- Bob loves Film article
  (3, 3, 3),
  -- Charlie is wowed by Farming
  (4, 4, 4),
  -- Diana finds Synthwave funny (maybe ironically!)
  (5, 5, 5);
-- Ethan is sad about game dev struggles
-- Post Tags
INSERT INTO PostTags (post_id, tag_id)
VALUES (1, 1),
  -- AI tag for AI article
  (2, 2),
  -- Film tag for photography article
  (3, 3),
  -- Farming tag for sustainability article
  (4, 4),
  -- Synthwave tag for music article
  (5, 5);
-- Indie Games tag for game dev article

INSERT INTO Subscriptions (follower_id, author_id, created_on)
VALUES (2, 1, '2025-03-11');