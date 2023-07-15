from user_management import UserManagement

# management methods
user_management = UserManagement()

print("\n################################## ADMIN DATABASE ##################################\n")
## clear admin database ##
user_management.clear_db(user_management.admin_db)
print("Database after clearing the content:\n")
user_management.print_db(database=user_management.admin_db)

## fill admin_db at the beginning without any checks ##
user_management.force_add_user_by_uid(database=user_management.admin_db,
                                      uid="04 2B 7B 2A 54 61 80")
print("Database after a forced insert:\n")
user_management.print_db(database=user_management.admin_db)

## add admin with checks ##
print("Database after a checked insert:\n")
user_management.add_user_by_uid(database=user_management.admin_db,
                                user_uid="11 22 33 44 55 66 77",
                                admin_uid="04 2B 7B 2A 54 61 80")
user_management.print_db(database=user_management.admin_db)

## delete admin_uid without any checks ##
user_management.force_delete_user(database=user_management.admin_db,
                                  uid="11 22 33 44 55 66 77")
print("Database after a forced deletion:\n")
user_management.print_db(database=user_management.admin_db)

## delete admin with checks ##
print("Database after a checked deletion:\n")
user_management.delete_user(database=user_management.admin_db,
                            user_uid="04 2B 7B 2A 54 61 80",
                            admin_uid="04 2B 7B 2A 54 61 80")
user_management.print_db(database=user_management.admin_db)

print("\n\n################################## ALL USERS DATABASE ##################################\n")
## fill admin_db at the beginning without any checks so users can be added to all_users_db ##
user_management.force_add_user_by_uid(database=user_management.admin_db,
                                      uid="04 2B 7B 2A 54 61 80")

## clear all_users database ##
user_management.clear_db(user_management.all_users_db)
print("Database after clearing the content:\n")
user_management.print_db(database=user_management.all_users_db)

## fill all_users_db at the beginning without any checks ##
user_management.force_add_user_by_uid(database=user_management.all_users_db,
                                      uid="22 22 55 55 77 88 33")
print("Database after a forced insert:\n")
user_management.print_db(database=user_management.all_users_db)

## add user with checks ##
print("Database after a checked insert:\n")
user_management.add_user_by_uid(database=user_management.all_users_db,
                                user_uid="11 22 33 33 78 63 42",
                                admin_uid="04 2B 7B 2A 54 61 80")
user_management.print_db(database=user_management.all_users_db)

## delete user_uid without any checks ##
user_management.force_delete_user(database=user_management.all_users_db,
                                  uid="11 22 33 33 78 63 42")
print("Database after a forced deletion:\n")
user_management.print_db(database=user_management.all_users_db)

## delete user with checks ##
print("Database after a checked deletion:\n")
user_management.delete_user(database=user_management.all_users_db,
                            user_uid="22 22 55 55 77 88 33",
                            admin_uid="04 2B 7B 2A 54 61 80")
user_management.print_db(database=user_management.all_users_db)


## clear admin database ##
user_management.clear_db(user_management.admin_db)
