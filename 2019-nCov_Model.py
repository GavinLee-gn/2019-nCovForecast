# coding=utf-8
# python 3.7

'''
参考网页：
https://zhuanlan.zhihu.com/p/104268573?night=1
'''
from pyecharts.charts import *
import pyecharts.options as opts


class nCov(object):
    def init(self, I: int,
             N: float, beta: float, r: int, days: int,
             mode: str, gamma: float = 0.0, deta: float = 0.0,
             control_day: int = 0, r0: int = 0, beta0: int = 0):

        '''
        初始化
        :param I:infectious_count
        :param N:总人数(万人)
        :param beta:infectious_rate:
        :param r:meet_person_count:
        :param days:天数
        :param mode:SI/SIS/SIR/SEIR
        :param gamma:(可选)SIS模型中 S 再次感染( I )的概率或SIR模型中 I 恢复健康( R )的概率
        :param deta:(可选)SEIR模型中潜伏者( E )转化为感染者( I )的概率
        :param control_day:(可选)从第几天开始做防御措施(感染率beta/接触人员r下降)
        :param r0:(可选)做好防御措施后，接触人数下降到原有的百分之几
        :param beta0:(可选)做好防御措施后，感染率下降到原有的百分之几
        :return:
        '''

        self.I = I
        self.N = N * 10000
        self.B = beta
        self.G = gamma
        self.D = deta
        self.r = r

        self.sub_title = ''
        self.sub_title += u'初始感染者 = ' + str(self.I) + '\n'


        self.days = days
        self.control_day = control_day
        if self.control_day == 0:
            self.r0 = self.r
            self.B0 = self.B
            self.sub_title += u'每天接触人数 = ' + str(self.r) + '\n'
        else:
            self.r0 = int(self.r * r0 / 100)
            self.B0 = self.B * beta0 / 100
            # self.sub_title += u'采取措施时间 = ' + str(self.control_day) + '\n'
            self.sub_title += u'采取措施前/后每天接触人数 = ' + str(self.r) + '/' + str(self.r0) + '\n'
            self.sub_title += u'采取措施前/后感染率 = ' + str(self.B * 100) + '%/' + str(self.B0 * 100) + '%\n'

        self.mode = mode
        self.S = self.N - self.I
        if self.mode == 'SIS':
            self.sub_title += u'健康者再次感染率 = ' + str(self.G * 100) + '%\n'
        elif self.mode == 'SIR':
            self.sub_title += u'康复概率(之后不再感染) = ' + str(self.G * 100) + '%\n'
            self.R = 0
        elif self.mode == 'SEIR':
            self.sub_title += u'康复概率(之后不再感染) = ' + str(self.G * 100) + '%\n'
            self.sub_title += u'潜伏者转换为感染者概率 = ' + str(self.D * 100) + '%\n'
            self.R = 0
            self.E = 0
        else:

            pass

    def draw_line(self):
        '''

        :return: grid 图案
        '''
        line = (
            Line()
                .set_global_opts(
                title_opts=opts.TitleOpts(title=self.mode + '模型',
                                          subtitle=self.sub_title,
                                          )

            )

                .add_xaxis(list(range(self.days)))
                .add_yaxis(u'未感者', self.S_list,
                           yaxis_index=0,
                           is_smooth=True,
                           label_opts=opts.LabelOpts(is_show=False)
                           )
                .add_yaxis(u'感染者', self.I_list,
                           yaxis_index=0,
                           is_smooth=True,
                           label_opts=opts.LabelOpts(is_show=False)
                           )

        )
        if self.mode == 'SIR':
            line.add_yaxis(u'康复者', self.R_list,
                           yaxis_index=0,
                           is_smooth=True,
                           label_opts=opts.LabelOpts(is_show=False)
                           )
        elif self.mode == 'SEIR':
            line.add_yaxis(u'康复者', self.R_list,
                           yaxis_index=0,
                           is_smooth=True,
                           label_opts=opts.LabelOpts(is_show=False)
                           )
            line.add_yaxis(u'潜伏者', self.E_list,
                           yaxis_index=0,
                           is_smooth=True,
                           label_opts=opts.LabelOpts(is_show=False)
                           )
        else:
            pass
        if self.control_day != 0:
            # line.add_yaxis(u'采取措施', list(range(self.N)),
            #                yaxis_index=0,
            #                is_smooth=True,
            #                label_opts=opts.LabelOpts(is_show=False)
            #                )
            pass
        grid = (Grid()
                .add(line, grid_opts=opts.GridOpts(pos_top='25%'))
                # .render()
                )

        print('draw')
        return grid

    def main(self):
        self.I_list = [self.I]
        self.S_list = [self.S]

        if self.mode == 'SI':
            '''
            SI模型：
            正常人 S ，有 beta 的概率变成感染者 I
            S->I
    
            健康人比例为  S/N ，乘积为每天新增感染病例
            方程：
            dI/dt=r*beta*I*S/N
            dS/dt=-r*beta*I*S/N
    
            第 n 天人数：
            I(n)=I(n-1)+r*beta*I(n-1)*S(n-1)/N
            S(n)=S(n-1)-r*beta*I(n-1)*S(n-1)/N
            '''
            for idx in range(1, self.days, 1):
                if idx > self.control_day:
                    temp_I = self.I_list[idx - 1] + self.r0 * self.B0 * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N
                    temp_S = self.S_list[idx - 1] - self.r0 * self.B0 * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N
                else:
                    temp_I = self.I_list[idx - 1] + self.r * self.B * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N
                    temp_S = self.S_list[idx - 1] - self.r * self.B * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N
                # 感染者 I 不能大于总数，健康人 S 不能小于1
                if temp_I > self.N - 1 or temp_S < 1:
                    self.I_list.append(self.N)
                    self.S_list.append(0)
                else:
                    self.I_list.append(temp_I)
                    self.S_list.append(temp_S)
        elif self.mode == 'SIS':
            '''
            SIS模型
            正常人 S ，有 beta 的概率变成感染者 I
            感染者 I ，有 gama 的概率变成正常人 S
            S->I->S
            健康人比例为  S/N ，乘积为每天新增感染病例
            N = S + I
            方程：
            dI/dt=r*beta*I*S/N-gamma*I 
            dS/dt=-r*beta*I*S/N+gamma*I

            第 n 天人数：
            I(n)=I(n-1)+r*beta*I(n-1)*S(n-1)/N-gamma*I(n-1)
            S(n)=S(n-1)-r*beta*I(n-1)*S(n-1)/N+gamma*I(n-1)
            '''
            for idx in range(1, self.days, 1):
                if idx > self.control_day:
                    temp_I = self.I_list[idx - 1] + self.r0 * self.B0 * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N - self.G * self.I_list[idx - 1]
                    temp_S = self.S_list[idx - 1] - self.r0 * self.B0 * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N + self.G * self.I_list[idx - 1]
                else:
                    temp_I = self.I_list[idx - 1] + self.r * self.B * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N - self.G * self.I_list[idx - 1]
                    temp_S = self.S_list[idx - 1] - self.r * self.B * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N + self.G * self.I_list[idx - 1]
                # 感染者 I 不能大于总数，健康人 S 不能小于1
                if temp_I > self.N - 1 or temp_S < 1:
                    self.I_list.append(self.N)
                    self.S_list.append(0)
                else:
                    self.I_list.append(temp_I)
                    self.S_list.append(temp_S)
        elif self.mode == 'SIR':
            '''
            SIR模型
            正常人 S ，有 beta 的概率变成感染者 I
            感染者 I ，有 gama 的概率变成正常人 R
            治好的 R ，无机会被感染成 I
            S->I->R
            N = S + I + R
            健康人比例为  S/N ，乘积为每天新增感染病例
            方程：
            dI/dt=r*beta*I*S/N-gamma*I 
            dS/dt=-r*beta*I*S/N
            dR/dt=gamma*I

            第 n 天人数：
            I(n)=I(n-1)+r*beta*I(n-1)*S(n-1)/N-gamma*I(n-1)
            S(n)=S(n-1)-r*beta*I(n-1)*S(n-1)/N
            R(n)=R(n-1)+gamma*I(n-1)
            '''
            self.R_list = [self.R]
            for idx in range(1, self.days, 1):
                if idx > control_day:
                    temp_I = self.I_list[idx - 1] + self.r0 * self.B0 * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N - self.G * self.I_list[idx - 1]
                    temp_S = self.S_list[idx - 1] - self.r0 * self.B0 * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N
                else:
                    temp_I = self.I_list[idx - 1] + self.r * self.B * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N - self.G * self.I_list[idx - 1]
                    temp_S = self.S_list[idx - 1] - self.r * self.B * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N
                temp_R = self.R_list[idx - 1] + self.G * self.I_list[idx - 1]
                # 感染者 I 不能大于总数，健康人 S 不能小于1
                # 康复者 R 不能大于总数
                if temp_I > self.N - 1 or temp_S < 1 or temp_R > self.N - 1:
                    self.I_list.append(self.N)
                    self.S_list.append(0)
                    self.R_list.append(self.N)
                else:
                    self.I_list.append(temp_I)
                    self.S_list.append(temp_S)
                    self.R_list.append(temp_R)
        elif self.mode == 'SEIR':
            '''
            SEIR模型
            
            正常人 S ，有 beta 的概率变成潜伏者 E
            潜伏者 E ，有 deta 的概率变成感染者 I
            感染者 I ，有 gama 的概率变成正常人 S
            治好的 S ，无机会被感染成 I
            S->E->I->R
            N = S + E + I + R
            健康人比例为  S/N ，乘积为每天新增感染病例
            方程：
            dE/dt=r*beta*I*S/N-deta*E
            dI/dt=deta*E-gamma*I 
            dS/dt=-r*beta*I*S/N
            dR/dt=gamma*I

            第 n 天人数：
            E(n)=E(n-1)+r*beta*I(n-1)*S(n-1)/N-deta*E(n-1)
            I(n)=I(n-1)+deta*E(n-1)-gamma*I(n-1)
            S(n)=S(n-1)-r*beta*I(n-1)*S(n-1)/N
            R(n)=R(n-1)+gamma*I(n-1)
            
            '''
            self.R_list = [self.R]
            self.E_list = [self.E]
            for idx in range(1, self.days, 1):
                if idx > self.control_day:
                    temp_S = self.S_list[idx - 1] - self.r0 * self.B0 * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N
                    temp_E = self.E_list[idx - 1] + self.r0 * self.B0 * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N - self.D * self.E_list[idx - 1]
                else:
                    temp_S = self.S_list[idx - 1] - self.r * self.B * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N
                    temp_E = self.E_list[idx - 1] + self.r * self.B * self.I_list[idx - 1] * self.S_list[
                        idx - 1] / self.N - self.D * self.E_list[idx - 1]
                temp_I = self.I_list[idx - 1] + self.D * self.E_list[idx - 1] - self.G * self.I_list[idx - 1]
                temp_R = self.R_list[idx - 1] + self.G * self.I_list[idx - 1]
                # 感染者 I 不能大于总数，健康人 S 不能小于1
                # 康复者 R 不能大于总数
                # 潜伏者 E 不能大于总数
                if temp_I > self.N - 1 or temp_S < 1 or temp_R > self.N - 1 or temp_E > self.N - 1:
                    self.I_list.append(0)
                    self.S_list.append(0)
                    self.R_list.append(self.N)
                    self.E_list.append(0)
                else:
                    self.I_list.append(temp_I)
                    self.S_list.append(temp_S)
                    self.R_list.append(temp_R)
                    self.E_list.append(temp_E)
        self.draw_line()


if __name__ == '__main__':
    '''
    :param I:infectious_count
    :param N:总人数(万人)
    :param beta:infectious_rate:
    :param r:meet_person_count:
    :param days:天数
    :param mode:SI/SIS/SIR/SEIR
    :param gamma:(可选)SIS模型中 S 再次感染( I )的概率或SIR模型中 I 恢复健康( R )的概率
    :param deta:(可选)SEIR模型中潜伏者( E )转化为感染者( I )的概率
    :param control_day:(可选)从第几天开始做防御措施(感染率beta/接触人员r下降)
    :param r0:(可选)做好防御措施后，接触人数下降到原有的百分之几(写整数)
    :param beta0:(可选)做好防御措施后，感染率下降到原有的百分之几(写整数)
    '''
    page = Page()
    r_list = [10, 10, 10, 50]  # r:meet_person_count:
    beta_list = [0.05, 0.05, 0.05, 0.8]  # beta:infectious_rate:
    gamma_list = [0.0, 0.3, 0.3, 0.5]  # gamma:(可选)SIS模型中 S 再次感染( I )的概率或SIR/SEIR模型中 I 恢复健康( R )的概率
    deta_list = [0.0, 0.0, 0.0, 0.99]  # deta:(可选)SEIR模型中潜伏者( E )转化为感染者( I )的概率
    days_list = [300, 300, 300, 20]  # days:天数
    mode_list = ['SI', 'SIS', 'SIR', 'SEIR']  # mode:SI/SIS/SIR/SEIR
    control_day = 6  # (可选)从第几天开始做防御措施(感染率beta/接触人员r下降)
    beta_rate_after_control_day = 80  # (可选)做好防御措施后，感染率下降到原有的百分之几(写整数)
    r_rate_after_control_day = 80  # r0:(可选)做好防御措施后，接触人数下降到原有的百分之几(写整数)
    aa = nCov()
    for beta, gamma, deta, mod, r, d in zip(beta_list, gamma_list, deta_list, mode_list, r_list, days_list):
        aa.init(1,  # 第一次感染 人数
                14,  # 总人数 （万人）
                beta, r, d, mod, gamma, deta, control_day, r_rate_after_control_day, beta_rate_after_control_day)
        aa.main()
        g = aa.draw_line()
        page.add(g)
    page.render()
