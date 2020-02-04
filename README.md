# 2019-nCovForecast
2019新型冠状病毒走势预测

修改以下参数即可查看走势图
    r_list = [10, 10, 10, 50]  # r:meet_person_count:
    beta_list = [0.05, 0.05, 0.05, 0.8]  # beta:infectious_rate:
    gamma_list = [0.0, 0.3, 0.3, 0.5]  # gamma:(可选)SIS模型中 S 再次感染( I )的概率或SIR/SEIR模型中 I 恢复健康( R )的概率
    deta_list = [0.0, 0.0, 0.0, 0.99]  # deta:(可选)SEIR模型中潜伏者( E )转化为感染者( I )的概率
    days_list = [300, 300, 300, 20]  # days:天数
    mode_list = ['SI', 'SIS', 'SIR', 'SEIR']  # mode:SI/SIS/SIR/SEIR
    control_day = 6  # (可选)从第几天开始做防御措施(感染率beta/接触人员r下降)
    beta_rate_after_control_day = 80  # (可选)做好防御措施后，感染率下降到原有的百分之几(写整数)
    r_rate_after_control_day = 80  # r0:(可选)做好防御措施后，接触人数下降到原有的百分之几(写整数)
 
