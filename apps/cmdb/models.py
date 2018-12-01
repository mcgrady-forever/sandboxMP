from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AbstractCode(models.Model):
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.SET_NULL, related_name='child'
    )

    class Meta:
        abstract = True
        verbose_name = '字典'
        verbose_name_plural = verbose_name


class Code(AbstractCode):
    key = models.CharField(max_length=80, verbose_name='键')
    value = models.CharField(max_length=80, verbose_name='值')
    desc = models.BooleanField(default=True, verbose_name='备注')


class ConnectionInfo(models.Model):
    auth_method_choices = (
        ('rsa', '公钥认证'),
        ('password', '密码认证')
    )

    username = models.CharField(max_length=15, verbose_name='SSH用户名')
    password = models.CharField(max_length=15, verbose_name='SSH密码')
    ssh_ip = models.GenericIPAddressField(verbose_name='SSH远程IP')
    ssh_port = models.IntegerField(default=22, verbose_name='SSH端口')
    auth_method = models.CharField(max_length=10, choices=auth_method_choices, default='password')
    ssh_rsa = models.CharField(max_length=80, blank=True, null=True, verbose_name='ssh私钥')
    rsa_pass = models.CharField(max_length=15, blank=True, null=True, verbose_name='私钥密码')
    ssh_status = models.BooleanField(default=True, verbose_name='登陆状态')

    class Meta:
        verbose_name = 'SSH连接信息'
        verbose_name_plural = verbose_name


class Cabinet(models.Model):
    number = models.CharField(max_length=50, verbose_name='机柜编号')
    position = models.CharField(max_length=80, verbose_name='机柜位置')

    class Meta:
        verbose_name = '机柜信息'
        verbose_name_plural = verbose_name


class DeviceInfo(models.Model):
    number = models.CharField(max_length=50, verbose_name='设备编号')
    name = models.CharField(max_length=50, verbose_name='设备名称')
    ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    mac_address = models.CharField(max_length=20, blank=True, null=True, verbose_name='MAC地址')
    sn_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='SN编号')
    device_type = models.IntegerField(blank=True, verbose_name='设备类型')
    network_type = models.IntegerField(blank=True, verbose_name='网络类型')
    service_type = models.IntegerField(blank=True,  verbose_name='服务类型')
    operation_type = models.IntegerField(blank=True, verbose_name='业务类型')
    os_type = models.IntegerField(blank=True, verbose_name='系统类型')
    desc = models.TextField(blank=True, verbose_name='备注信息')
    leader = models.ForeignKey(
        User,
        related_name='leader',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='责任人'
    )
    dev_cabinet = models.ForeignKey(
        'Cabinet',
        related_name='dev_cabinet',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        verbose_name='设备位置'
    )
    dev_connection = models.ForeignKey(
        'ConnectionInfo',
        related_name='dev_connection',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='连接信息'
    )

    class Meta:
        verbose_name = '设备信息'
        verbose_name_plural = verbose_name