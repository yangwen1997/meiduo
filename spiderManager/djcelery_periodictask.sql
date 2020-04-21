INSERT INTO "djcelery_periodictask" VALUES (1, 'celery.backend_cleanup', 'celery.backend_cleanup', '[]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-03 20:00:00.013685', 38, '2018-09-03 20:00:15.094974', '', 1, NULL);
INSERT INTO "djcelery_periodictask" VALUES (2, 'qichahca', 'utils.celery_tasks.check_counter', '["qichacha_com","detail_results","企查查"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.012819', 957, '2018-09-04 07:02:15.035700', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (3, '工信', 'utils.celery_tasks.check_counter', '["gxzg_org_cn","detail_results","工信中国"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.014691', 914, '2018-09-04 07:02:15.009239', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (4, '建筑资产', 'utils.celery_tasks.check_counter', '["zcgl","company_info","建筑资质"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.017735', 909, '2018-09-04 07:02:15.045568', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (5, '企查查资产', 'utils.celery_tasks.check_counter', '["qichacha_com","zhichan","企查查资产"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.019939', 922, '2018-09-04 07:02:15.048886', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (6, '微猫', 'utils.celery_tasks.check_counter', '["weimao_xiaowang","report_results","微猫"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.021830', 872, '2018-09-04 07:02:15.025908', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (7, '名录', 'utils.celery_tasks.check_counter', '["all_com","all_results","名录"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.024432', 869, '2018-09-04 07:02:15.022496', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (8, '商标', 'utils.celery_tasks.check_counter', '["sbgg_cn","sb_detail","商标公告"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.026306', 813, '2018-09-04 07:02:15.005887', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (9, '裁判文书', 'utils.celery_tasks.check_counter', '["wenshu_cn","detail_wenshu","裁判文书"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.028186', 813, '2018-09-04 07:02:15.012568', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (10, '企查查 单页', 'utils.celery_tasks.check_counter', '["qichacha_com","temp_one_page_results","企查查基本信息"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.030088', 728, '2018-09-04 07:02:15.015868', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (11, '企查查名录', 'utils.celery_tasks.check_counter', '["qichacha_com","temp_list_info","企查查名录"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.031951', 659, '2018-09-04 07:02:15.042235', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (12, '启信宝名录', 'utils.celery_tasks.check_counter', '["qixin_com","list_names","启信名录"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.034590', 599, '2018-09-04 07:02:14.988909', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (13, '智高点商标', 'utils.celery_tasks.check_counter', '["shangbiao_db","zhigaodian_detail_results","智高点商标"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.036470', 533, '2018-09-04 07:02:15.032372', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (14, '无讼文书', 'utils.celery_tasks.check_counter', '["falv_db","wusong_wenshu_detail_results","无讼文书"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.038345', 527, '2018-09-04 07:02:14.992541', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (15, '企查猫', 'utils.celery_tasks.check_counter', '["qichamao_xiaowang","detail_results","企查猫基本信息"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.040222', 475, '2018-09-04 07:02:15.038986', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (16, 'news', 'utils.celery_tasks.chrome', '[]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 06:00:00.000435', 108, '2018-09-04 06:00:40.038884', '', 6, NULL);
INSERT INTO "djcelery_periodictask" VALUES (17, '工信中国名录', 'utils.celery_tasks.check_counter', '["gxzg_org_cn","list_results","工信中国名录"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.000470', 340, '2018-09-04 07:02:14.995881', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (18, '【清bad ip 库】', 'utils.celery_tasks.clear_ips', '[]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-03 16:00:00.004799', 8, '2018-09-03 16:00:05.081287', '', 8, NULL);
INSERT INTO "djcelery_periodictask" VALUES (19, '【修改ip状态】', 'utils.celery_tasks.change_ip_status', '[]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-03 01:30:59.230926', 5, '2018-09-03 01:36:24.535319', '', 9, NULL);
INSERT INTO "djcelery_periodictask" VALUES (20, '千慧网商标', 'utils.celery_tasks.check_counter', '["shangbiao_db","qianhui_detail_results","千慧网商标"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.003041', 172, '2018-09-04 07:02:15.019197', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (21, '水滴信用', 'utils.celery_tasks.check_counter', '["shuidi_com","detail_results","水滴信用详情"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.005898', 149, '2018-09-04 07:02:15.029131', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (22, '百度信用基本信息', 'utils.celery_tasks.check_counter', '["bdxy_com","detail_results","百度信用基本信息"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.008073', 146, '2018-09-04 07:02:14.999174', '', 2, NULL);
INSERT INTO "djcelery_periodictask" VALUES (23, '启信宝基本信息', 'utils.celery_tasks.check_counter', '["qixin_com","temp_one_results","启信宝基本信息"]', '{}', NULL, NULL, NULL, NULL, 1, '2018-09-04 07:00:00.009934', 96, '2018-09-04 07:02:15.002599', '', 2, NULL);
