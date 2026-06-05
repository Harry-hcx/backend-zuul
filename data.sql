CREATE DATABASE IF NOT EXISTS game_db
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE game_db;

DROP TABLE IF EXISTS room_item;
DROP TABLE IF EXISTS backpack_item;
DROP TABLE IF EXISTS save_record;
DROP TABLE IF EXISTS backpack;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS player;

CREATE TABLE player (
    player_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '玩家唯一标识',
    player_name VARCHAR(100) NOT NULL COMMENT '玩家名称',
    player_password VARCHAR(100) NOT NULL COMMENT '玩家密码',
    player_avatar_url VARCHAR(255) COMMENT '玩家头像URL',
    player_score INT DEFAULT 0 COMMENT '玩家得分',
    player_stamina INT DEFAULT 200 COMMENT '玩家体力值',
    player_backpack_id INT COMMENT '背包id',
    player_room_id INT COMMENT '当前所在房间ID'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='玩家信息表';

CREATE TABLE backpack (
    backpack_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '背包唯一标识',
    player_id INT NOT NULL COMMENT '所属玩家ID',
    backpack_size INT NOT NULL DEFAULT 100 COMMENT '背包最大容量'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='背包信息表';

CREATE TABLE item (
    item_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '物品唯一标识',
    item_name VARCHAR(100) NOT NULL COMMENT '物品名称',
    item_size INT NOT NULL DEFAULT 0 COMMENT '占用背包空间',
    item_value INT DEFAULT 0 COMMENT '物品价值'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='物品信息表';

CREATE TABLE backpack_item (
    backpack_id INT NOT NULL COMMENT '背包ID',
    item_id INT NOT NULL COMMENT '物品ID',
    PRIMARY KEY (backpack_id, item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='背包-物品关联表';

CREATE TABLE room (
    room_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '房间唯一标识',
    room_name VARCHAR(100) NOT NULL COMMENT '房间名称',
    room_up_id INT COMMENT '向上连接房间ID',
    room_down_id INT COMMENT '向下连接房间ID',
    room_left_id INT COMMENT '向左连接房间ID',
    room_right_id INT COMMENT '向右连接房间ID'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='房间信息表';

CREATE TABLE room_item (
    room_id INT NOT NULL COMMENT '房间ID',
    item_id INT NOT NULL COMMENT '物品ID',
    PRIMARY KEY (room_id, item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='房间-物品关联表';

CREATE TABLE save_record (
    save_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '存档ID',
    player_id INT NOT NULL COMMENT '所属玩家ID',
    save_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '存档时间',
    player_score INT COMMENT '存档时玩家得分',
    player_stamina INT COMMENT '存档时玩家体力',
    player_room_id INT COMMENT '存档时所在房间ID',
    player_backpack_id INT COMMENT '存档对应的背包id'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='玩家存档信息表';