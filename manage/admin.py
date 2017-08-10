from django.contrib import admin
from manage import models
from django.contrib.auth import get_user_model, password_validation
# from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.forms import UsernameField
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext, ugettext_lazy as _
# admin.site.register(models.User)

models.UserInfo

# admin.site.register(models.Student2Class)
# admin.site.register(models.Class)
from django.contrib import admin

User = get_user_model()


class UserInline(admin.StackedInline):
    model = User


class UserClassInline(admin.StackedInline):
    model = User.user_class.through
    verbose_name = '学生'
    can_delete = False


class UserTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [UserInline]
    fields = ['name', 'path']
    ordering = ['id']

# admin.site.register(models.UserType, UserTypeAdmin)


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        # label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification. hhh"),
        # help_text="Enter the same password as before, for verification. hhhh",
    )
    password3 = forms.CharField(
        label=_("Password confirmation2"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    email = forms.EmailField(
        label='email..',
        widget=forms.EmailField,
        help_text='请输入邮箱',
    )

    class Meta:
        model = get_user_model()
        # fields = ("username", "email")
        fields = ("email",)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MyUserAdmin(UserAdmin):
    # form
    add_form = UserCreationForm
    # 显示的列
    list_display = ['id', 'username', 'upper_case_name', 'password', 'is_active', ]
    # 自定义显示字段
    def upper_case_name(self, obj):
        return ("%s %s" % (obj.username, obj.email)).upper()
    upper_case_name.short_description = 'Name'
    # 显示字段
    # fields = ('username', 'email', 'phone', 'qq', 'is_active', 'is_superuser', 'date_joined', 'user_class',)
    # 排序的列
    ordering = ['id']
    search_fields = ('id', 'username',)
    date_hierarchy = 'date_joined'
    # 绑定action
    actions = ['disabled_user', 'abled_user']

    # 定制active
    def disabled_user(self, request, queryset):
        try:
            rows_updated = queryset.update(is_active=False)
            self.message_user(request, "%s 条记录修改完成." % rows_updated)
        except Exception as e:
            self.message_user(request, "{}:修改失败".format(e))

    disabled_user.short_description = '禁用所选的 用户'

    def abled_user(self, request, queryset):
        try:
            rows_updated = queryset.update(is_active=True)
            self.message_user(request, "%s 条记录修改完成." % rows_updated)
        except Exception as e:
            self.message_user(request, "{}:修改失败".format(e))

    abled_user.short_description = '启用所选的 用户'


# 注册
admin.site.register(User, MyUserAdmin)
admin.site.register(models.Student2Class)
admin.site.register(models.Student)
# admin.site.register(models.Class)


class Class(admin.ModelAdmin):
    # 显示的列
    list_display = ['id', 'name', 'area', 'status', 'upper_case_name']

    def upper_case_name(self, obj):
        c = obj.user_set.all().count()
        return c
    inlines = [UserClassInline]
    upper_case_name.short_description = '学员数量'
    # 显示字段
    # fields = ('username',
    #           'email',
    #           'is_active',
    #           'is_superuser',
    #           'date_joined',
    #           'user_type',)
    # 排序的列
    ordering = ['id']
    search_fields = ('id', 'name', 'area', 'status')
    date_hierarchy = 'date'
    # 绑定action
    actions = ['action_class', 'over_class', 'start_school']

    # 定制active
    def start_school(self, request, queryset):
        try:
            rows_updated = queryset.update(status=2)
            self.message_user(request, "%s 条记录修改完成." % rows_updated)
        except Exception as e:
            self.message_user(request, "{}:修改失败".format(e))

    start_school.short_description = '开课'

    def over_class(self, request, queryset):
        try:
            rows_updated = queryset.update(status=3)
            self.message_user(request, "%s 条记录修改完成." % rows_updated)
        except Exception as e:
            self.message_user(request, "{}:修改失败".format(e))

    over_class.short_description = '结业'

    # 定制active
    def action_class(self, request, queryset):
        try:
            rows_updated = queryset.update(status=1)
            self.message_user(request, "%s 条记录修改完成." % rows_updated)
        except Exception as e:
            self.message_user(request, "{}:修改失败".format(e))

    action_class.short_description = '开始报名'


# 注册
admin.site.register(models.Class, Class)

# list_display = ('__str__',)
# list_display_links = ()
# list_filter = ()
# list_select_related = False
# list_per_page = 100
# list_max_show_all = 200
# list_editable = ()
# search_fields = ()
# date_hierarchy = None
# save_as = False
# save_as_continue = True
# save_on_top = False
# paginator = Paginator
# preserve_filters = True
# inlines = []
#
# # Custom templates (designed to be over-ridden in subclasses)
# add_form_template = None
# change_form_template = None
# change_list_template = None
# delete_confirmation_template = None
# delete_selected_confirmation_template = None
# object_history_template = None
# popup_response_template = None
#
# # Actions
# actions = []
# action_form = helpers.ActionForm
# actions_on_top = True
# actions_on_bottom = False
# actions_selection_counter = True
# checks_class = ModelAdminChecks
