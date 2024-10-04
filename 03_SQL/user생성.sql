-- sql 주석
# sql 주석
/*
block 주석
*/
-- control + enter: 실행
-- 명령문 뒤에 ; 을 붙인다. 
-- sql문은 대소문자 구분하지 않는다
-- 사용자 계정 (localhost)

create user scott@localhost identified by 'tiger';
-- 사용자 계정 (원격 접속 계정)
create user scott@'%' identified by 'tiger';

-- 권한 지정.
grant all privileges on *.* to scott@localhost;
grant all privileges on *.* to scott@'%';

-- 계정들 조회
select host, user from mysql.user;

-- 계정 삭제
drop user scott@'%';
drop user scott@localhost;
