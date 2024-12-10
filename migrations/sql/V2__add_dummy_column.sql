-- 컬럼 추가
ALTER TABLE tbl_sl_deeplink_params
ADD COLUMN dummy_test VARCHAR(100) DEFAULT 'test' COMMENT '테스트용 더미 컬럼',
ALGORITHM=INSTANT;
