#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Author :Yangky
# @TIME : 2019-06-27 11:10
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from repository import models

'''
BBS 用到的 form 类
'''


class RegForm(forms.Form):
    username = forms.CharField(max_length=32, label='用户名', error_messages={
        'max_length': '用户名最长32', 'required': '用户名不能为空'},
                               widget=forms.widgets.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=6, label='密码',
                               widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
                               error_messages={'min_length': '密码长度最小6位', 'required': '该字段不能为空'})

    re_password = forms.CharField(min_length=6, label='确认密码',
                                  widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'},
                                                                     render_value=True),
                                  error_messages={'min_length': '密码长度最小6位', 'required': '该字段不能为空'})

    email = forms.EmailField(label='邮箱', error_messages={'invalid': '邮箱不格式不正确'},
                             widget=forms.widgets.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=16, label='手机号', error_messages={
        'max_length': '手机号最长16', 'required': '手机号不能为空'},
                            widget=forms.widgets.TextInput(attrs={'class': 'form-control'}),
                            validators=[RegexValidator(r'^[0-9]+$', '请输入数字'),
                                        RegexValidator(r'^1[3-9][0-9]+$', '手机号格式不正确')])

    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_exists = models.UserProfile.objects.filter(username=username)
        if is_exists:
            # 用户名已被注册
            self.add_error('username', ValidationError('用户名已存在'))
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exists = models.UserProfile.objects.filter(email=email)
        if is_exists:
            # 邮箱已存在
            self.add_error('email', ValidationError('邮箱已注册'))
        else:
            return email

    # 重写全局勾子，对确认密码校验
    def clean(self):
        password_value = self.cleaned_data.get('password')
        re_password_value = self.cleaned_data.get('re_password')
        if password_value == re_password_value:
            return self.cleaned_data
        else:
            self.add_error('re_password', '两次密码不一致')
            print(self._errors)
            raise ValidationError('两次密码不一致')
