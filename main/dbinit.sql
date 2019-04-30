DROP TABLE IF  EXISTS fund_manager;
CREATE TABLE IF NOT EXISTS `fund_manager` (
	`manager_id` varchar(255) NOT NULL COMMENT '基金经理id',
  `manager_name` varchar(255) NOT NULL COMMENT '基金经理名称',
	`employment_date` varchar(255) DEFAULT NULL COMMENT '任职起始日期',
  `employment_time` varchar(255) DEFAULT NULL COMMENT '累计任职时间',
  `company_name` varchar(255) DEFAULT NULL COMMENT '现任基金公司',
  `management_scale` varchar(255) DEFAULT NULL COMMENT '资产总规模',
  `best_return` varchar(255) DEFAULT NULL COMMENT '最佳回报',
	`manager_url` varchar(255) NOT NULL COMMENT '基金经理主页',
  `created_date` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_date` datetime DEFAULT NULL COMMENT '更新日期',
	 `data_source` varchar(255) DEFAULT 'eastmoney' COMMENT '数据来源',
   PRIMARY KEY (`manager_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF  EXISTS previous_managed_info;
CREATE TABLE IF NOT EXISTS `previous_managed_info` (
	`manager_id` varchar(255) NOT NULL COMMENT '基金经理id',
  `fund_code` varchar(255) NOT NULL COMMENT '基金代码',
	`fund_name` varchar(255) NOT NULL COMMENT '基金名称',
	`fund_type` varchar(255) DEFAULT NULL COMMENT '基金类型',
  `fund_scale` varchar(255) DEFAULT NULL COMMENT '基金规模（亿元）',
  `employment_time` varchar(255) DEFAULT NULL COMMENT '任职时间',
  `employment_date` varchar(255) DEFAULT NULL COMMENT '任职天数',
  `employment_return` varchar(255) DEFAULT NULL COMMENT '任职回报',
  `created_date` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_date` datetime DEFAULT NULL COMMENT '更新日期',
	`data_source` varchar(255) DEFAULT 'eastmoney' COMMENT '数据来源',
   PRIMARY KEY (`manager_id`,`fund_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF  EXISTS current_managed_info;
CREATE TABLE IF NOT EXISTS `current_managed_info` (
	`manager_id` varchar(255) NOT NULL COMMENT '基金经理id',
  `fund_code` varchar(255) NOT NULL COMMENT '基金代码',
	`fund_name` varchar(255) NOT NULL COMMENT '基金名称',
	`fund_type` varchar(255) DEFAULT NULL COMMENT '基金类型',
  `three_months_income` varchar(255) DEFAULT NULL COMMENT '近三个月收益',
  `three_months_rank` varchar(255) DEFAULT NULL COMMENT '近三个月收益排名/总数',
  `six_months_income` varchar(255) DEFAULT NULL COMMENT '近六个月收益',
  `six_months_rank` varchar(255) DEFAULT NULL COMMENT '近六个月收益排名/总数',
	`one_year_income` varchar(255) DEFAULT NULL COMMENT '近一年收益',
  `one_year_rank` varchar(255) DEFAULT NULL COMMENT '近一年收益排名/总数',
	`two_years_income` varchar(255) DEFAULT NULL COMMENT '近两年收益',
  `two_years_rank` varchar(255) DEFAULT NULL COMMENT '近两年收益排名/总数',
	`this_year_income` varchar(255) DEFAULT NULL COMMENT '今年以来收益',
  `this_year_rank` varchar(255) DEFAULT NULL COMMENT '今年以来收益排名/总数',
  `created_date` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_date` datetime DEFAULT NULL COMMENT '更新日期',
	`data_source` varchar(255) DEFAULT 'eastmoney' COMMENT '数据来源',
   PRIMARY KEY (`manager_id`,`fund_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;