from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import User
    from .models.tokens import (
        PasswordResetToken,
        EmailVerificationToken,
    )
    from .models.profile import Profile
    from .models.address import Address