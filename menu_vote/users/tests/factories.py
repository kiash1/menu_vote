from typing import Sequence, Any

from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, post_generation

User = get_user_model()


class UserFactory(DjangoModelFactory):
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    username = Faker("name")
    is_active = True

    class Meta:
        model = User
        django_get_or_create = ["username"]

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        if not isinstance(self, dict):
            password = (
                extracted
                if extracted
                else Faker(
                    "password",
                    length=42,
                    special_chars=True,
                    digits=True,
                    upper_case=True,
                    lower_case=True,
                ).generate(extra_kwargs={})
            )
            self.set_password(password)
            self.save()
