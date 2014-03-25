load data local infile '/home/ubuntu/database/lncrnadb_data/output/character.csv' into table cmsplugin_annotation fields terminated by ';' enclosed by '|' escaped by '\n' lines terminated by '\r\n';
load data local infile '/home/ubuntu/database/lncrnadb_data/output/literature.csv' into table cmsplugin_literature fields terminated by ';' enclosed by '|' escaped by "\n" lines terminated by '\r\n';
load data local infile '/home/ubuntu/database/lncrnadb_data/output/alias.csv' into table cmsplugin_nomenclature fields terminated by ';' enclosed by '|' escaped by "\n" lines terminated by '\r\n';
load data local infile '/home/ubuntu/database/lncrnadb_data/output/assoc.csv' into table cmsplugin_associatedcomp fields terminated by ';' enclosed by '|' escaped by "\n" lines terminated by '\r\n';
load data local infile '/home/ubuntu/database/lncrnadb_data/output/sequence.csv' into table cmsplugin_sequences fields terminated by ';' enclosed by '|' escaped by "\n" lines terminated by '\r\n';





set foreign_key_checks=0; truncate cms_page; Load data local infile '/home/ubuntu/database/lncrnadb_data/output/cms_page' into table cms_page fields terminated by ';' enclosed by '|' LINES TERMINATED by '\r\n'; show warnings;



set foreign_key_checks=0; truncate cms_title; Load data local infile '/home/ubuntu/database/lncrnadb_data/output/cms_title' into table cms_title fields terminated by ';' enclosed by '|' LINES TERMINATED by '\r\n'; show warnings;

set foreign_key_checks=0; truncate cms_page_placeholders; Load data local infile '/home/ubuntu/database/lncrnadb_data/output/cms_page_placeholders' into table cms_page_placeholders fields terminated by ';' enclosed by '|' LINES TERMINATED by '\r\n'; show warnings;
set foreign_key_checks=0;truncate cms_placeholder; Load data local infile '/home/ubuntu/database/lncrnadb_data/output/cms_placeholder' into table cms_placeholder fields terminated by ';' enclosed by '|' LINES TERMINATED by '\r\n'; show warnings;
set foreign_key_checks=0;truncate cms_cmsplugin; Load data local infile '/home/ubuntu/database/lncrnadb_data/output/cms_cmsplugins' into table cms_cmsplugin fields terminated by ';' enclosed by '|' LINES TERMINATED by '\r\n'; show warnings;

set foreign_key_checks=0;set foreign_key_checks=0; truncate cmsplugin_nomenclature; Load data local infile '/home/ubuntu/database/lncrnadb_data/output/alias.csv' into table cmsplugin_nomenclature fields terminated by ';' enclosed by '|' LINES TERMINATED by '\r\n'; show warnings;
