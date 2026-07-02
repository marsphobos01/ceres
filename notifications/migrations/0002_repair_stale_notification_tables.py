from django.db import migrations


def repair_stale_notification_tables(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            DO $$
            BEGIN
                IF to_regclass('public.notifications_notification') IS NOT NULL THEN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notification'
                          AND column_name = 'notification_id'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notification'
                          AND column_name = 'id'
                    ) THEN
                        ALTER TABLE notifications_notification
                            RENAME COLUMN notification_id TO id;
                    END IF;

                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notification'
                          AND column_name = 'notification_name'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notification'
                          AND column_name = 'title'
                    ) THEN
                        ALTER TABLE notifications_notification
                            RENAME COLUMN notification_name TO title;
                    END IF;

                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notification'
                          AND column_name = 'notification_content'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notification'
                          AND column_name = 'body'
                    ) THEN
                        ALTER TABLE notifications_notification
                            RENAME COLUMN notification_content TO body;
                    END IF;

                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notification'
                          AND column_name = 'user_id'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notification'
                          AND column_name = 'recipient_id'
                    ) THEN
                        ALTER TABLE notifications_notification
                            RENAME COLUMN user_id TO recipient_id;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notification'
                          AND column_name = 'actor_id'
                    ) THEN
                        ALTER TABLE notifications_notification
                            ADD COLUMN actor_id integer;
                        UPDATE notifications_notification
                            SET actor_id = recipient_id
                            WHERE actor_id IS NULL;
                        ALTER TABLE notifications_notification
                            ALTER COLUMN actor_id SET NOT NULL;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notification'
                          AND column_name = 'source_app'
                    ) THEN
                        ALTER TABLE notifications_notification
                            ADD COLUMN source_app varchar(120) NOT NULL DEFAULT 'notifications';
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notification'
                          AND column_name = 'source_object_type'
                    ) THEN
                        ALTER TABLE notifications_notification
                            ADD COLUMN source_object_type varchar(120) NOT NULL DEFAULT 'legacy_notification';
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notification'
                          AND column_name = 'source_object_id'
                    ) THEN
                        ALTER TABLE notifications_notification
                            ADD COLUMN source_object_id integer NOT NULL DEFAULT 0;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notification'
                          AND column_name = 'updated_at'
                    ) THEN
                        ALTER TABLE notifications_notification
                            ADD COLUMN updated_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;
                END IF;

                IF to_regclass('public.notifications_reminder') IS NOT NULL THEN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_reminder'
                          AND column_name = 'reminder_id'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_reminder'
                          AND column_name = 'id'
                    ) THEN
                        ALTER TABLE notifications_reminder
                            RENAME COLUMN reminder_id TO id;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_reminder'
                          AND column_name = 'source_app'
                    ) THEN
                        ALTER TABLE notifications_reminder
                            ADD COLUMN source_app varchar(120) NOT NULL DEFAULT 'notifications';
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_reminder'
                          AND column_name = 'source_object_type'
                    ) THEN
                        ALTER TABLE notifications_reminder
                            ADD COLUMN source_object_type varchar(120) NOT NULL DEFAULT 'legacy_reminder';
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_reminder'
                          AND column_name = 'source_object_id'
                    ) THEN
                        ALTER TABLE notifications_reminder
                            ADD COLUMN source_object_id integer NOT NULL DEFAULT 0;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_reminder'
                          AND column_name = 'updated_at'
                    ) THEN
                        ALTER TABLE notifications_reminder
                            ADD COLUMN updated_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;
                END IF;

                IF to_regclass('public.notifications_notificationpreferences') IS NOT NULL THEN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notificationpreferences'
                          AND column_name = 'created_at'
                    ) THEN
                        ALTER TABLE notifications_notificationpreferences
                            ADD COLUMN created_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notificationpreferences'
                          AND column_name = 'updated_at'
                    ) THEN
                        ALTER TABLE notifications_notificationpreferences
                            ADD COLUMN updated_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;
                END IF;

                IF to_regclass('public.notifications_notificationdelivery') IS NOT NULL THEN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notificationdelivery'
                          AND column_name = 'delivery_status'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notificationdelivery'
                          AND column_name = 'status'
                    ) THEN
                        ALTER TABLE notifications_notificationdelivery
                            RENAME COLUMN delivery_status TO status;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notificationdelivery'
                          AND column_name = 'created_at'
                    ) THEN
                        ALTER TABLE notifications_notificationdelivery
                            ADD COLUMN created_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_notificationdelivery'
                          AND column_name = 'updated_at'
                    ) THEN
                        ALTER TABLE notifications_notificationdelivery
                            ADD COLUMN updated_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;
                END IF;

                IF to_regclass('public.notifications_mutedcontent') IS NOT NULL THEN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_mutedcontent'
                          AND column_name = 'source_app'
                    ) THEN
                        ALTER TABLE notifications_mutedcontent
                            ADD COLUMN source_app varchar(120) NOT NULL DEFAULT 'notifications';
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_mutedcontent'
                          AND column_name = 'source_object_type'
                    ) THEN
                        ALTER TABLE notifications_mutedcontent
                            ADD COLUMN source_object_type varchar(120) NOT NULL DEFAULT 'legacy_muted_content';
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_mutedcontent'
                          AND column_name = 'source_object_id'
                    ) THEN
                        ALTER TABLE notifications_mutedcontent
                            ADD COLUMN source_object_id integer NOT NULL DEFAULT 0;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'notifications_mutedcontent'
                          AND column_name = 'created_at'
                    ) THEN
                        ALTER TABLE notifications_mutedcontent
                            ADD COLUMN created_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;
                END IF;
            END $$;
            """
        )


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(repair_stale_notification_tables, migrations.RunPython.noop),
    ]
