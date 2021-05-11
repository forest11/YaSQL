# Generated by Django 2.2.16 on 2021-05-07 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TicketFlow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('creator', models.CharField(db_index=True, max_length=32, verbose_name='创建人')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('state', models.IntegerField(verbose_name='当前状态')),
                ('parent_ticket_id', models.IntegerField(default=0, verbose_name='父工单id')),
                ('participant', models.CharField(blank=True, max_length=32, null=True, verbose_name='当前处理人')),
                ('act_status', models.IntegerField(choices=[(0, '初始化'), (1, '进行中'), (2, '已通过'), (3, '已拒绝'), (4, '已完成'), (5, '已失败'), (6, '已关闭'), (7, '已中止')], default=1, verbose_name='操作状态')),
                ('multi_result', models.TextField(blank=True, help_text='当前状态处理人全部处理时实际的处理结果，json格式', null=True, verbose_name='所有处理结果')),
            ],
            options={
                'verbose_name': '工单',
                'verbose_name_plural': '工单',
                'db_table': 'yasql_workflow_tickflow',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='WorkflowGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
            ],
            options={
                'verbose_name': '流程组',
                'verbose_name_plural': '流程组',
                'db_table': 'yasql_workflow_group',
            },
        ),
        migrations.CreateModel(
            name='WorkflowTpl',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=64, verbose_name='流程名称')),
                ('description', models.CharField(max_length=128, verbose_name='描述')),
                ('all_view', models.BooleanField(default=True, help_text='只允许工单的关联人(创建人、需要处理人)查看工单,默认所有人可见', verbose_name='工单可见性')),
                ('display_form', models.CharField(default='[]', help_text='表单中可见字段,自定义字段中的field_key', max_length=1024, verbose_name='表单字段')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wf', to='workflow.WorkflowGroup', verbose_name='流程组')),
            ],
            options={
                'verbose_name': '流程模版',
                'verbose_name_plural': '流程模版',
                'db_table': 'yasql_workflow_tpl',
            },
        ),
        migrations.CreateModel(
            name='WorkflowCustomField',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('field_name', models.CharField(max_length=64, verbose_name='字段名称')),
                ('field_key', models.CharField(help_text='字段类型请尽量特殊，避免与系统中关键字冲突', max_length=64, verbose_name='字段key')),
                ('field_type', models.CharField(choices=[('string', '字符串'), ('integer', '整型'), ('boolean', '布尔值'), ('textarea', '文本框'), ('select', '单选下拉列表'), ('multiselect', '多选下拉列表'), ('file', '附件'), ('user', '用户')], max_length=32, verbose_name='类型')),
                ('required', models.BooleanField(default=False, verbose_name='字段值是否必填')),
                ('order_id', models.IntegerField(default=0, help_text='工单表单中排序:工单号0,标题20,状态id40,状态名41,创建人80,创建时间100,更新时间120.前端根据id顺序排列', verbose_name='字段顺序')),
                ('default_value', models.CharField(blank=True, help_text='作为表单中的该字段的默认值', max_length=128, null=True, verbose_name='默认值')),
                ('placeholder', models.CharField(blank=True, help_text='用户工单详情表单中作为字段的占位符显示', max_length=128, null=True, verbose_name='占位符')),
                ('field_value', models.TextField(blank=True, help_text='select/multiselect提供选项，格式为json如:{"1":"需要","0":"不需要"},{"1":"中国", "2":"美国"}', null=True, verbose_name='字段数据')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wf_field', to='workflow.WorkflowTpl', verbose_name='关联流程')),
            ],
            options={
                'verbose_name': '流程字段',
                'verbose_name_plural': '流程字段',
                'db_table': 'yasql_workflow_field',
            },
        ),
        migrations.CreateModel(
            name='TicketFlowUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('state', models.IntegerField(verbose_name='当前状态')),
                ('username', models.CharField(max_length=64, verbose_name='处理人')),
                ('process', models.BooleanField(default=False, verbose_name='是否处理')),
                ('action', models.CharField(default='', max_length=64, verbose_name='执行操作')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tf_user', to='workflow.TicketFlow', verbose_name='工单')),
            ],
            options={
                'verbose_name': '工单处理人',
                'verbose_name_plural': '工单处理人',
                'db_table': 'yasql_workflow_tickflowuser',
            },
        ),
        migrations.CreateModel(
            name='TicketFlowLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('participant', models.CharField(max_length=64, verbose_name='处理人')),
                ('state', models.CharField(max_length=64, verbose_name='当前状态')),
                ('suggestion', models.CharField(blank=True, max_length=2048, null=True, verbose_name='处理意见')),
                ('act_status', models.IntegerField(choices=[(0, '初始化'), (1, '进行中'), (2, '已通过'), (3, '已拒绝'), (4, '已完成'), (5, '已失败'), (6, '已关闭'), (7, '已中止')], default=1, help_text='constant中定义：拒绝/通过/中止/超时', verbose_name='操作状态')),
                ('ticket_data', models.TextField(blank=True, help_text='可以用于记录当前表单数据，json格式', null=True, verbose_name='工单数据')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tf_log', to='workflow.TicketFlow', verbose_name='工单')),
            ],
            options={
                'verbose_name': '工单流转日志',
                'verbose_name_plural': '工单流转日志',
                'db_table': 'yasql_workflow_tickflowlog',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='TicketFlowField',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('field_name', models.CharField(max_length=64, verbose_name='字段名称')),
                ('field_type', models.CharField(max_length=32, verbose_name='字段类型')),
                ('field_key', models.CharField(max_length=64, verbose_name='字段key')),
                ('field_value', models.CharField(blank=True, max_length=2048, null=True, verbose_name='字符串值')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tf_field', to='workflow.TicketFlow', verbose_name='工单')),
            ],
            options={
                'verbose_name': '工单字段',
                'verbose_name_plural': '工单字段',
                'db_table': 'yasql_workflow_tickflowfiled',
            },
        ),
        migrations.AddField(
            model_name='ticketflow',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wf_tickflow', to='workflow.WorkflowTpl', verbose_name='关联流程'),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=64, verbose_name='状态名称')),
                ('order_id', models.IntegerField(default=0, help_text='用于工单步骤接口时，step上状态的顺序，值越小越靠前', verbose_name='状态顺序')),
                ('state_type', models.IntegerField(choices=[(0, '普通类型'), (1, '初始状态'), (2, '结束状态')], default=0, help_text='初始状态:新建工单时,获取必填字段及状态流转，结束状态：此状态下的工单不再处理，没有对应的状态流转', verbose_name='状态类型')),
                ('is_hidden', models.BooleanField(default=False, help_text='设置为True时,获取工单步骤api中不显示此状态(当前处于此状态时除外)', verbose_name='是否隐藏')),
                ('participant_type', models.IntegerField(blank=True, choices=[(1, '个人'), (2, '角色'), (3, '机器人'), (4, '工单字段'), (5, 'Hook')], null=True, verbose_name='操作人类型')),
                ('participant_data', models.CharField(blank=True, help_text='可以为空、多用户/部门/角色/变量等，包含子工作流的需要设置处理人为bot', max_length=1024, null=True, verbose_name='操作人参数')),
                ('distribute_type', models.CharField(blank=True, choices=[('any', 'any'), ('all', 'all')], help_text='any其中一人处理即可，all所有人都要处理', max_length=32, null=True, verbose_name='流转方式')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wf_state', to='workflow.WorkflowTpl', verbose_name='关联流程')),
            ],
            options={
                'verbose_name': '流程状态',
                'verbose_name_plural': '流程状态',
                'db_table': 'yasql_workflow_state',
                'ordering': ('-workflow__id', 'order_id'),
            },
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('action', models.CharField(max_length=64, verbose_name='流转名称')),
                ('transition_type', models.IntegerField(choices=[(1, '常规'), (2, '其他')], help_text='1.常规流转，2.其他', verbose_name='流转类型')),
                ('attribute_type', models.IntegerField(default=1, help_text='1.同意，2.拒绝，3.其他', verbose_name='属性类型')),
                ('condition_expression', models.CharField(blank=True, help_text='流转条件表达式，根据表达式中的条件来确定流转的下个状态', max_length=2048, null=True, verbose_name='条件表达式')),
                ('field_require_check', models.BooleanField(default=True, help_text='提交工单时需要校验数据。如"退回"属性的操作，表单不需要提交数据', verbose_name='是否校验参数')),
                ('destination_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state_destination', to='workflow.State', verbose_name='目标状态')),
                ('source_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state_source', to='workflow.State', verbose_name='源状态')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wf_transition', to='workflow.WorkflowTpl', verbose_name='关联流程')),
            ],
            options={
                'verbose_name': '流程状态流转',
                'verbose_name_plural': '流程状态流转',
                'db_table': 'yasql_workflow_transition',
                'ordering': ('-workflow__id', 'destination_state'),
                'unique_together': {('source_state', 'destination_state', 'attribute_type')},
            },
        ),
    ]
