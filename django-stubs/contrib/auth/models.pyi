from collections.abc import Iterable
from typing import Any, ClassVar, Literal, TypeAlias, TypeVar

from django.contrib.auth.base_user import AbstractBaseUser as AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager as BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet
from django.db.models.base import Model
from django.db.models.manager import EmptyManager
from django.utils.functional import _StrOrPromise
from typing_extensions import Self

# This is our "placeholder" type the mypy plugin refines to configured 'AUTH_USER_MODEL'
# wherever it is used as a type. The most recognised example of this is (probably)
# `HttpRequest.user`
_User: TypeAlias = AbstractBaseUser

_UserModel: TypeAlias = type[_User]

_AnyUser: TypeAlias = _User | AnonymousUser

# These are only needed for generic classes in order to bind to a specific implementation
_AnyUserType = TypeVar("_AnyUserType", bound=_AnyUser)  # noqa: PYI018

# do not use the alias `_User` so the bound remains at `AbstractUser`
_UserType = TypeVar("_UserType", bound=AbstractUser)

def update_last_login(sender: _UserModel, user: _User, **kwargs: Any) -> None: ...

class PermissionManager(models.Manager[Permission]):
    def get_by_natural_key(self, codename: str, app_label: str, model: str) -> Permission: ...

class Permission(models.Model):
    content_type_id: int
    objects: ClassVar[PermissionManager]

    name = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    codename = models.CharField(max_length=100)
    def natural_key(self) -> tuple[str, str, str]: ...

class GroupManager(models.Manager[Group]):
    def get_by_natural_key(self, name: str) -> Group: ...

class Group(models.Model):
    objects: ClassVar[GroupManager]

    name = models.CharField(max_length=150)
    permissions = models.ManyToManyField(Permission)
    def natural_key(self) -> tuple[str]: ...

class UserManager(BaseUserManager[_UserType]):
    def create_user(
        self, username: str, email: str | None = ..., password: str | None = ..., **extra_fields: Any
    ) -> _UserType: ...
    def create_superuser(
        self, username: str, email: str | None = ..., password: str | None = ..., **extra_fields: Any
    ) -> _UserType: ...
    def with_perm(
        self,
        perm: str | Permission,
        is_active: bool = ...,
        include_superusers: bool = ...,
        backend: str | None = ...,
        obj: Model | None = ...,
    ) -> QuerySet[_UserType]: ...

class PermissionsMixin(models.Model):
    is_superuser = models.BooleanField()
    groups = models.ManyToManyField(Group)
    user_permissions = models.ManyToManyField(Permission)

    def get_user_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    async def aget_user_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    def get_group_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    async def aget_group_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    def get_all_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    async def aget_all_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    def has_perm(self, perm: str, obj: _AnyUser | None = ...) -> bool: ...
    async def ahas_perm(self, perm: str, obj: _AnyUser | None = ...) -> bool: ...
    def has_perms(self, perm_list: Iterable[str], obj: _AnyUser | None = ...) -> bool: ...
    async def ahas_perms(self, perm_list: Iterable[str], obj: _AnyUser | None = ...) -> bool: ...
    def has_module_perms(self, app_label: str) -> bool: ...
    async def ahas_module_perms(self, app_label: str) -> bool: ...

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    username_validator: UnicodeUsernameValidator

    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    objects: ClassVar[UserManager[Self]]

    EMAIL_FIELD: str
    USERNAME_FIELD: str

    def get_full_name(self) -> str: ...
    def get_short_name(self) -> str: ...
    def email_user(
        self, subject: _StrOrPromise, message: _StrOrPromise, from_email: str = ..., **kwargs: Any
    ) -> None: ...

class User(AbstractUser): ...

class AnonymousUser:
    id: None
    pk: None
    username: Literal[""]
    is_staff: Literal[False]
    is_active: Literal[False]
    is_superuser: Literal[False]
    def save(self) -> None: ...
    def delete(self) -> None: ...
    def set_password(self, raw_password: str) -> None: ...
    def check_password(self, raw_password: str) -> Any: ...
    @property
    def groups(self) -> EmptyManager[Group]: ...
    @property
    def user_permissions(self) -> EmptyManager[Permission]: ...
    def get_user_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    async def aget_user_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    def get_group_permissions(self, obj: _AnyUser | None = ...) -> set[Any]: ...
    async def aget_group_permissions(self, obj: _AnyUser | None = ...) -> set[Any]: ...
    def get_all_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    async def aget_all_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    def has_perm(self, perm: str, obj: _AnyUser | None = ...) -> bool: ...
    async def ahas_perm(self, perm: str, obj: _AnyUser | None = ...) -> bool: ...
    def has_perms(self, perm_list: Iterable[str], obj: _AnyUser | None = ...) -> bool: ...
    async def ahas_perms(self, perm_list: Iterable[str], obj: _AnyUser | None = ...) -> bool: ...
    def has_module_perms(self, module: str) -> bool: ...
    async def ahas_module_perms(self, module: str) -> bool: ...
    @property
    def is_anonymous(self) -> Literal[True]: ...
    @property
    def is_authenticated(self) -> Literal[False]: ...
    def get_username(self) -> str: ...
