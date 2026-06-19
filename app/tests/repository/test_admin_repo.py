from app.repository.auth_repo import admin_authentication_with_email, admin_save_in_database
from app.database_models.admins_table import Admins

async def test_admin_exist_in_database(db_session):
    admin = await admin_authentication_with_email(
        db_session,
        "mirha@gmail.com"
    )

    assert admin.email == "mirha@gmail.com"
    assert admin is not None

async def test_admin_save_in_database(db_session):
    new_admin = Admins(
        name = "Mirha",
        age = 23,
        phone_number = "03625252555",
        email = "mirha@gmail.com",
        password = "Beauty"
    )

    await admin_save_in_database(
        db_session,
        new_admin
    )

    result = await admin_authentication_with_email(
        db_session,
        "mirha@gmail.com"
    )

    assert result is not None
    assert result.email == "mirha@gmail.com"


