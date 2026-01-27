# Migration to reorder companyName column to be after userType

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_customeruser_companyname'),
    ]

    operations = [
        # PostgreSQL doesn't support reordering columns directly,
        # so we need to recreate the table with the correct column order
        migrations.RunSQL(
            # Forward SQL - Reorder columns by creating new table and copying data
            sql="""
                -- Create temporary table with correct column order
                CREATE TABLE "Users_new" (
                    "id" SERIAL PRIMARY KEY,
                    "empId" VARCHAR(100) UNIQUE NULL,
                    "username" VARCHAR(150) NULL,
                    "zoneTypeName" VARCHAR(100) NULL,
                    "userType" VARCHAR(20) NOT NULL DEFAULT 'customer',
                    "companyName" VARCHAR(200) NULL,
                    "firstName" VARCHAR(100) NULL,
                    "lastName" VARCHAR(100) NULL,
                    "telephone" VARCHAR(20) UNIQUE NULL,
                    "email" VARCHAR(254) UNIQUE NOT NULL,
                    "password" VARCHAR(128) NOT NULL,
                    "last_login" TIMESTAMP NULL,
                    "is_superuser" BOOLEAN NOT NULL DEFAULT FALSE,
                    "is_staff" BOOLEAN NOT NULL DEFAULT FALSE,
                    "is_active" BOOLEAN NOT NULL DEFAULT TRUE,
                    "date_joined" TIMESTAMP NOT NULL DEFAULT NOW()
                );
                
                -- Copy data from old table to new table
                INSERT INTO "Users_new" (
                    "id", "empId", "username", "zoneTypeName", "userType", "companyName",
                    "firstName", "lastName", "telephone", "email", "password", "last_login",
                    "is_superuser", "is_staff", "is_active", "date_joined"
                )
                SELECT 
                    "id", "empId", "username", "zoneTypeName", "userType", "companyName",
                    "firstName", "lastName", "telephone", "email", "password", "last_login",
                    "is_superuser", "is_staff", "is_active", "date_joined"
                FROM "Users";
                
                -- Drop old table
                DROP TABLE "Users" CASCADE;
                
                -- Rename new table to original name
                ALTER TABLE "Users_new" RENAME TO "Users";
                
                -- Recreate foreign key constraint for zoneTypeName
                ALTER TABLE "Users" 
                ADD CONSTRAINT "Users_zoneTypeName_fkey" 
                FOREIGN KEY ("zoneTypeName") 
                REFERENCES "ZoneType"("typeName") 
                ON DELETE SET NULL;
                
                -- Recreate sequence for id
                CREATE SEQUENCE IF NOT EXISTS "Users_id_seq";
                SELECT setval('"Users_id_seq"', COALESCE((SELECT MAX(id) FROM "Users"), 1));
                ALTER TABLE "Users" ALTER COLUMN "id" SET DEFAULT nextval('"Users_id_seq"');
                ALTER SEQUENCE "Users_id_seq" OWNED BY "Users"."id";
                
                -- Recreate indexes
                CREATE INDEX IF NOT EXISTS "Users_empId_idx" ON "Users"("empId");
                CREATE INDEX IF NOT EXISTS "Users_username_idx" ON "Users"("username");
                CREATE INDEX IF NOT EXISTS "Users_email_idx" ON "Users"("email");
                CREATE INDEX IF NOT EXISTS "Users_telephone_idx" ON "Users"("telephone");
                CREATE INDEX IF NOT EXISTS "Users_zoneTypeName_idx" ON "Users"("zoneTypeName");
            """,
            
            # Reverse SQL - This is complex, so we'll just make it non-reversible
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
