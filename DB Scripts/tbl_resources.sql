use scheduler;

-- The column root_parent_resource_id should be nullable, or no row can be inserted due to the constraint.
-- The value of parent_resource_id and root_parent_resource_id should be null by default and updated after resource is created.
alter table tbl_resources alter root_parent_resource_id drop not null;

-- If the ID of the first resource is not 1 after batch insert, delete them and reset the auto increment to 1 with following statement if you like.
alter table tbl_resources auto_increment = 1;

insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (1, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (1, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (1, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (1, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (1, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (2, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (2, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (2, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (2, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (3, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (3, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (4, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (4, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (5, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (5, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (6, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (6, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (7, 'User_1', now(),null,null);
insert into tbl_resources (type_id, last_updated_by, last_updated_date, parent_resource_id, root_parent_resource_id) values (7, 'User_1', now(),null,null);

-- Update the parent resource ID and root parent resource ID
update tbl_resources set parent_resource_id = 1, root_parent_resource_id = 1 where id in (6, 10, 12, 14, 16, 18);
update tbl_resources set parent_resource_id = 2, root_parent_resource_id = 2 where id in (7, 11, 13, 15, 17, 19);
update tbl_resources set parent_resource_id = 3, root_parent_resource_id = 3 where id = 8;
update tbl_resources set parent_resource_id = 4, root_parent_resource_id = 4 where id = 9;