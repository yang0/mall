/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2014-3-13 11:01:00                           */
/*==============================================================*/


drop table if exists brand;

drop table if exists eav_enum_group;

drop table if exists eav_enum_group_value;

drop table if exists eav_enum_value;

drop table if exists eav_prop;

drop table if exists eav_value;

drop table if exists pic;

drop table if exists product_category;

drop table if exists product_category_prop;

drop table if exists product_item;

drop table if exists product_item_prop;

drop table if exists product_item_room;

drop table if exists product_sell_prop_group;

drop table if exists product_sell_prop_value;

drop table if exists product_sku;

drop table if exists room;

/*==============================================================*/
/* Table: brand                                                 */
/*==============================================================*/
create table brand
(
   id                   integer not null auto_increment,
   name                 varchar(15) not null comment 'Ʒ������',
   primary key (id)
);

/*==============================================================*/
/* Table: eav_enum_group                                        */
/*==============================================================*/
create table eav_enum_group
(
   id                   integer not null auto_increment,
   name                 varchar(10) not null,
   primary key (id)
);

alter table eav_enum_group comment '����ȫ��ö������';

/*==============================================================*/
/* Table: eav_enum_group_value                                  */
/*==============================================================*/
create table eav_enum_group_value
(
   id                   integer not null auto_increment,
   eav_enum_group_id    integer not null,
   eav_enum_value_id    integer not null,
   create_time          datetime not null,
   primary key (id)
);

/*==============================================================*/
/* Table: eav_enum_value                                        */
/*==============================================================*/
create table eav_enum_value
(
   id                   integer not null auto_increment,
   value                varchar(50) not null,
   primary key (id)
);

/*==============================================================*/
/* Table: eav_prop                                              */
/*==============================================================*/
create table eav_prop
(
   id                   integer not null auto_increment,
   name                 varchar(10) not null comment '��������',
   description          varchar(50) not null comment '����',
   eav_group_id         integer comment '���Թ�����enumgroup',
   datatype             integer not null comment '1int 2float 3txt 4date 5bool 6enum',
   create_time          datetime not null,
   update_time          datetime not null,
   creator_id           integer not null,
   prop_type            integer not null comment '1=�ؼ����� 2=�ǹؼ����� 3=��������',
   required             tinyint not null default false comment '�Ƿ����',
   primary key (id)
);

alter table eav_prop comment '��Ʒ��̬���Ա�';

/*==============================================================*/
/* Table: eav_value                                             */
/*==============================================================*/
create table eav_value
(
   id                   integer not null auto_increment,
   eav_prop_id          integer not null,
   product_item_id      integer not null,
   value_text           varchar(50),
   value_float          float,
   value_int            integer,
   value_date           datetime,
   value_bool           tinyint,
   value_enum_id        integer,
   value_sell_prop_group_id integer comment 'ö���飬�����������õ�',
   create_time          datetime not null default CURRENT_TIMESTAMP,
   update_time          datetime not null default CURRENT_TIMESTAMP,
   primary key (id)
);

/*==============================================================*/
/* Table: pic                                                   */
/*==============================================================*/
create table pic
(
   id                   integer not null auto_increment,
   pic                  varchar(100) not null,
   content_type_id      integer not null,
   object_id            integer not null,
   create_time          datetime not null,
   update_time          datetime not null,
   creator_id           integer not null,
   description          varchar(5000) not null,
   primary key (id)
);

/*==============================================================*/
/* Table: product_category                                      */
/*==============================================================*/
create table product_category
(
   id                   integer not null auto_increment,
   name                 varchar(15) not null,
   parent_id            integer,
   lft                  integer not null,
   rght                 integer not null,
   tree_id              integer not null,
   level                integer not null,
   primary key (id)
);

alter table product_category comment '��Ʒ��̨����';

/*==============================================================*/
/* Table: product_category_prop                                 */
/*==============================================================*/
create table product_category_prop
(
   id                   integer not null auto_increment,
   product_category_id  integer not null,
   eav_prop_id          integer not null,
   create_time          datetime not null default CURRENT_TIMESTAMP,
   primary key (id)
);

alter table product_category_prop comment '��Ʒ�������Щ����';

/*==============================================================*/
/* Table: product_item                                          */
/*==============================================================*/
create table product_item
(
   id                   integer not null auto_increment,
   num                  integer not null comment '��Ʒ����',
   price                integer not null comment '�۸�',
   title                varchar(20) comment '����',
   description          varchar(5000) not null comment '����',
   state_id             integer not null comment '��Ʒ����ʡ��',
   city_id              integer not null comment '��Ʒ���ڳ���',
   approve_status       tinyint not null default 0 comment '����״̬ 0=������  1=�ֿ���',
   product_category_id  integer not null comment 'Ҷ����Ŀid',
   pic                  varchar(100) not null comment '��ͼ',
   have_3d              tinyint not null default 0 comment '�Ƿ���3Dģ�� 0=�� 1=��',
   brand_id             integer not null comment '����Ʒ��',
   weight               decimal not null comment '��Ʒ���� ��λ������',
   bulk                 decimal not null comment '��Ʒ��� ��λ��������',
   sell_point           varchar(20) comment '��������',
   packing_num          integer not null comment '����',
   create_time          datetime not null,
   update_time          datetime not null,
   creator_id           integer not null,
   item_rank            integer not null default 0 comment '�Ƽ�ָ��',
   sold_num             integer not null default 0 comment '����',
   primary key (id)
);

/*==============================================================*/
/* Table: product_item_prop                                     */
/*==============================================================*/
create table product_item_prop
(
   id                   integer not null auto_increment,
   product_item_id      integer not null,
   eav_prop_id          integer not null,
   enum_group_id        integer not null default 0 comment '������������ԣ�����ֶβ�Ϊ0',
   create_time          datetime not null default CURRENT_TIMESTAMP,
   primary key (id)
);

alter table product_item_prop comment '��Ʒ�����Զ���';

/*==============================================================*/
/* Table: product_item_room                                     */
/*==============================================================*/
create table product_item_room
(
   id                   integer not null auto_increment,
   product_item_id      integer not null,
   room_id              integer not null,
   primary key (id)
);

/*==============================================================*/
/* Table: product_sell_prop_group                               */
/*==============================================================*/
create table product_sell_prop_group
(
   id                   integer not null auto_increment,
   name                 varchar(15) not null,
   create_time          datetime not null,
   product_item_id      integer not null,
   primary key (id)
);

alter table product_sell_prop_group comment '����һ����������';

/*==============================================================*/
/* Table: product_sell_prop_value                               */
/*==============================================================*/
create table product_sell_prop_value
(
   id                   integer not null auto_increment,
   product_sell_prop_group_id integer not null,
   eav_enum_value_id    integer not null,
   create_time          datetime not null,
   primary key (id)
);

alter table product_sell_prop_value comment '��������������Щֵ
';

/*==============================================================*/
/* Table: product_sku                                           */
/*==============================================================*/
create table product_sku
(
   id                   integer not null auto_increment,
   eav_value_id         integer not null,
   eav_enum_value_id    integer not null,
   price                decimal not null,
   primary key (id)
);

/*==============================================================*/
/* Table: room                                                  */
/*==============================================================*/
create table room
(
   id                   integer not null auto_increment,
   name                 varchar(10) not null comment '�ռ�����',
   primary key (id)
);

