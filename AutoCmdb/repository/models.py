from django.db import models
# from __future__ import unicode_literals
import django.utils.timezone as timezone
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户信息
    """
    phone = models.CharField(u'手机', max_length=32, unique=True)
    email = models.EmailField(null=False, default='***@163.com')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "用户表"
        db_table = 'UserProfile'


class AdminInfo(models.Model):
    """
    用户登陆相关信息
    """
    user_info = models.OneToOneField("UserProfile", on_delete=models.CASCADE)
    username = models.CharField(u'用户名', max_length=64)
    password = models.CharField(u'密码', max_length=64)

    class Meta:
        verbose_name_plural = "管理员表"
        db_table = 'AdminInfo'


class UserGroup(models.Model):
    """
    用户组
    """
    name = models.CharField(max_length=32, unique=True)
    users = models.ManyToManyField('UserProfile')

    class Meta:
        verbose_name_plural = "用户组表"
        db_table = 'UserGroup'

    def __str__(self):
        return self.name


class BusinessUnit(models.Model):
    """
    业务线
    """
    name = models.CharField('业务线', max_length=64, unique=True)
    contact = models.ForeignKey('UserGroup', verbose_name='业务联系人', related_name='c', on_delete=models.CASCADE)
    manager = models.ForeignKey('UserGroup', verbose_name='系统管理员', related_name='m', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "业务线表"
        db_table = 'BusinessUnit'

    def __str__(self):
        return self.name


class IDC(models.Model):
    """
    机房信息
    """
    name = models.CharField('机房', max_length=32)
    floor = models.IntegerField('楼层', default=1)

    class Meta:
        verbose_name_plural = "机房表"
        db_table = 'IDC'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    资产标签
    """
    name = models.CharField('标签', max_length=32, unique=True)

    class Meta:
        verbose_name_plural = "标签表"
        db_table = 'Tag'

    def __str__(self):
        return self.name


class Asset(models.Model):
    """
    资产信息表，所有资产公共信息（交换机，服务器，防火墙等）
    """
    device_type_choices = (
        (1, '服务器'),
        (2, '交换机'),
        (3, '防火墙'),
    )
    device_status_choices = (
        (1, '上架'),
        (2, '在线'),
        (3, '离线'),
        (4, '下架'),
    )

    device_type_id = models.IntegerField(choices=device_type_choices, default=1)
    device_status_id = models.IntegerField(choices=device_status_choices, default=1)

    cabinet_num = models.CharField('机柜号', max_length=30, null=True, blank=True)
    cabinet_order = models.CharField('机柜中序号', max_length=30, null=True, blank=True)

    idc = models.ForeignKey('IDC', verbose_name='IDC机房', null=True, blank=True, on_delete=models.CASCADE)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name='属于的业务线', null=True, blank=True,
                                      on_delete=models.CASCADE)

    tag = models.ManyToManyField('Tag')

    latest_date = models.DateField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "资产表"
        db_table = 'Asset'

    def __str__(self):
        return "%s-%s-%s" % (self.idc.name, self.cabinet_num, self.cabinet_order)


class Server(models.Model):
    """
    服务器信息
    """
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)

    hostname = models.CharField(max_length=128, unique=True)
    sn = models.CharField('SN号', max_length=64, db_index=True)
    manufacturer = models.CharField(verbose_name='制造商', max_length=64, null=True, blank=True)
    model = models.CharField('型号', max_length=64, null=True, blank=True)

    manage_ip = models.GenericIPAddressField('管理IP', null=True, blank=True)

    os_platform = models.CharField('系统', max_length=16, null=True, blank=True)
    os_version = models.CharField('系统版本', max_length=16, null=True, blank=True)

    cpu_count = models.IntegerField('CPU个数', null=True, blank=True)
    cpu_physical_count = models.IntegerField('CPU物理个数', null=True, blank=True)
    cpu_model = models.CharField('CPU型号', max_length=128, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = "服务器表"
        db_table = 'Server'

    def __str__(self):
        return self.hostname


class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    management_ip = models.CharField('管理IP', max_length=64, blank=True, null=True)
    vlan_ip = models.CharField('VlanIP', max_length=64, blank=True, null=True)
    intranet_ip = models.CharField('内网IP', max_length=128, blank=True, null=True)
    sn = models.CharField('SN号', max_length=64, unique=True)
    manufacture = models.CharField(verbose_name=u'制造商', max_length=128, null=True, blank=True)
    model = models.CharField('型号', max_length=128, null=True, blank=True)
    port_num = models.SmallIntegerField('端口个数', null=True, blank=True)
    device_detail = models.CharField('设置详细配置', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "网络设备"
        db_table = 'NetworkDevice'


class Disk(models.Model):
    """
    硬盘信息
    """
    slot = models.CharField('插槽位', max_length=8)
    model = models.CharField('磁盘型号', max_length=32)
    capacity = models.FloatField('磁盘容量GB')
    pd_type = models.CharField('磁盘类型', max_length=32)
    server_obj = models.ForeignKey('Server', related_name='disk', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "硬盘表"
        db_table = 'Disk'

    def __str__(self):
        return self.slot


class NIC(models.Model):
    """
    网卡信息
    """
    name = models.CharField('网卡名称', max_length=128)
    hwaddr = models.CharField('网卡mac地址', max_length=64)
    netmask = models.CharField(max_length=64)
    ipaddrs = models.CharField('ip地址', max_length=256)
    up = models.BooleanField(default=False)
    server_obj = models.ForeignKey('Server', related_name='nic', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "网卡表"
        db_table = 'NIC'

    def __str__(self):
        return self.name


class Memory(models.Model):
    """
    内存信息
    """
    slot = models.CharField('插槽位', max_length=32)
    manufacturer = models.CharField('制造商', max_length=32, null=True, blank=True)
    model = models.CharField('型号', max_length=64)
    capacity = models.FloatField('容量', null=True, blank=True)
    sn = models.CharField('内存SN号', max_length=64, null=True, blank=True)
    speed = models.CharField('速度', max_length=16, null=True, blank=True)

    server_obj = models.ForeignKey('Server', related_name='memory', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "内存表"
        db_table = 'Memory'

    def __str__(self):
        return self.slot


class AssetRecord(models.Model):
    """
    资产变更记录,creator为空时，表示是资产汇报的数据。
    """
    asset_obj = models.ForeignKey('Asset', related_name='ar', on_delete=models.CASCADE)
    content = models.TextField(null=True)
    creator = models.ForeignKey('UserProfile', null=True, blank=True, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "资产记录表"
        db_table = 'AssetRecord'

    def __str__(self):
        return "%s-%s-%s" % (self.asset_obj.idc.name, self.asset_obj.cabinet_num, self.asset_obj.cabinet_order)


class ErrorLog(models.Model):
    """
    错误日志,如：agent采集数据错误 或 运行错误
    """
    asset_obj = models.ForeignKey('Asset', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=16)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "错误日志表"
        db_table = 'ErrorLog'

    def __str__(self):
        return self.title


class MysqlInitInfo(models.Model):
    # 显示信息 server里都有 初始化表
    server_ip = models.GenericIPAddressField()
    user = models.CharField(max_length=30)
    status = models.CharField(max_length=10)  # 主从信息
    version = models.CharField(max_length=10)  # 版本
    create_time = models.DateTimeField(auto_now_add=True)
    change_time = models.DateTimeField(auto_now=True)
    app_name = models.CharField(default='mysql', max_length=20)

    class Meta:
        unique_together = ("app_name", "server_ip")
        db_table = 'MysqlInitInfo'


class MysqlInfo(models.Model):
    # 数据库信息
    db_name = models.CharField(max_length=50)
    role = models.CharField(max_length=15)  # master or slave
    hostname = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    service_name = models.CharField(max_length=10)  # 业务名称
    port = models.IntegerField()
    description = models.CharField(max_length=50, null=True)
    root_pass = models.CharField(max_length=30)  # 密码
    backup_ip = models.GenericIPAddressField(null=True)  # 备份机器
    archive_ip = models.GenericIPAddressField(null=True)  # 归档机器
    version = models.CharField(max_length=15, default='5.7.23')  # 版本
    search_flag = models.CharField(max_length=10, default=0)  # 是否为线下查询
    realm_name = models.CharField(max_length=256, default='')  # 域名

    class Meta:
        unique_together = ("ip", "port", "db_name", "role")
        db_table = 'MysqlInfo'


class DBGrantHistory(models.Model):
    host_ip = models.GenericIPAddressField()  # 被授权主机
    database_ip = models.GenericIPAddressField()  # 从库or 主库ip
    port = models.IntegerField()  # 主库ip 和端口能确定唯一的数据库名字 进而查出业务名称。
    request_user = models.CharField(max_length=30)
    operation_user = models.CharField(max_length=30, null=True)  # 申请人
    db_username = models.CharField(max_length=30)
    db_password = models.CharField(max_length=100)
    status = models.CharField(default=0, max_length=10)
    description = models.CharField(max_length=100, null=True)
    db_permission = models.CharField(max_length=30)
    db_name = models.CharField(max_length=60)
    create_time = models.DateTimeField(auto_now_add=True)  # 申请时间
    judge_time = models.DateTimeField(auto_now=True)  # 审批时间

    class Meta:
        unique_together = ("database_ip", "db_username", "port", 'db_permission', 'host_ip')
        db_table = 'DBGrantHistory'
        # 同一账户同一库的同一状态的数据


class DatabaseInfo(models.Model):  # 数据机信息表
    db_ip = models.GenericIPAddressField()  # 从库or 主库ip
    port = models.IntegerField()
    IN_BP = models.CharField(max_length=32, default='')
    db_space = models.CharField(max_length=16, default='')
    db_username = models.CharField(max_length=30)
    max_tablename = models.CharField(max_length=32, default='')
    max_tablespace = models.CharField(max_length=32, default='')
    total_data_free = models.CharField(max_length=32, default='')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("max_tablename", "db_username", "db_ip", "port",)
        db_table = 'DatabaseInfo'


class BackupInfo(models.Model):
    db_ip = models.GenericIPAddressField()  # 从库or 主库ip
    port = models.IntegerField()
    db_name = models.CharField(max_length=32, default='')
    backup_host = models.GenericIPAddressField()
    backup_dir = models.CharField(max_length=64, default='/data/')
    create_time = models.DateTimeField(auto_now_add=True)
    backup_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("db_name", "db_ip", "port",)
        db_table = 'BackupInfo'


class ArchiveTableInfo(models.Model):
    meta_ip = models.GenericIPAddressField()  # 源IP
    meta_port = models.IntegerField()
    meta_dbname = models.CharField(max_length=64, default='')
    arch_ip = models.GenericIPAddressField()  # 源IP
    arch_port = models.IntegerField()
    arch_dbname = models.CharField(max_length=64, default='')
    tablename = models.CharField(max_length=64, default='')
    backup_crontab_time = models.DateTimeField()
    last_archive_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tablename", "meta_dbname", "meta_ip", "arch_ip", "meta_port",)
        db_table = 'ArchiveTableInfo'


class RestoreDB(models.Model):
    master_ip = models.GenericIPAddressField()  # master IP
    master_port = models.IntegerField()
    master_dbname = models.CharField(max_length=64, default='')
    role = models.CharField(max_length=16, default='master')  # 主从信息，从库或及联主库
    backup_list = models.CharField(max_length=256, default='')  # 备份
    slave_ip = models.GenericIPAddressField()  # master IP
    slave_port = models.IntegerField()
    slave_dbname = models.CharField(max_length=64, default='')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('master_ip',)
        db_table = 'RestoreDB'


class DBChangeLog(models.Model):
    db_id = models.IntegerField()
    username = models.CharField(max_length=32, default='')
    option = models.CharField(max_length=32, default='')
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=16, default='')
