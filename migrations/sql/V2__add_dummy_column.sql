-- 컬럼 추가
ALTER TABLE tbl_sl_deeplink_params
ADD COLUMN dummy_test VARCHAR(100) DEFAULT 'test' COMMENT '테스트용 더미 컬럼';

-- 컬럼 삭제
ALTER TABLE tbl_sl_deeplink_params
DROP COLUMN dummy_test;
