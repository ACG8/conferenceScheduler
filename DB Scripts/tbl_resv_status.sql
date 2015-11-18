use scheduler;

insert into tbl_resv_status (name, description) values ('Successful','Successfully reserved');
insert into tbl_resv_status (name, description) values ('Rejected','Rejected by manager');
insert into tbl_resv_status (name, description) values ('Error', 'Happens when technical issue occurs');
insert into tbl_resv_status (name, description) values ('Waiting', 'In the waiting list');