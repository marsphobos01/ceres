from django.db import migrations


def repair_stale_planning_tables(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            DO $$
            BEGIN
                IF to_regclass('public.planning_calendarevent') IS NOT NULL THEN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_calendarevent'
                          AND column_name = 'user_id'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_calendarevent'
                          AND column_name = 'owner_id'
                    ) THEN
                        ALTER TABLE planning_calendarevent
                            RENAME COLUMN user_id TO owner_id;
                    END IF;

                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_calendarevent'
                          AND column_name = 'recurrence'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_calendarevent'
                          AND column_name = 'recurrence_type'
                    ) THEN
                        ALTER TABLE planning_calendarevent
                            RENAME COLUMN recurrence TO recurrence_type;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_calendarevent'
                          AND column_name = 'colour'
                    ) THEN
                        ALTER TABLE planning_calendarevent
                            ADD COLUMN colour varchar(6);
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_calendarevent'
                          AND column_name = 'created_at'
                    ) THEN
                        ALTER TABLE planning_calendarevent
                            ADD COLUMN created_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_calendarevent'
                          AND column_name = 'updated_at'
                    ) THEN
                        ALTER TABLE planning_calendarevent
                            ADD COLUMN updated_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;
                END IF;

                IF to_regclass('public.planning_task') IS NOT NULL THEN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_task'
                          AND column_name = 'user_id'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_task'
                          AND column_name = 'owner_id'
                    ) THEN
                        ALTER TABLE planning_task
                            RENAME COLUMN user_id TO owner_id;
                    END IF;

                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_task'
                          AND column_name = 'due'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_task'
                          AND column_name = 'due_date'
                    ) THEN
                        ALTER TABLE planning_task
                            RENAME COLUMN due TO due_date;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_task'
                          AND column_name = 'parent_task_id'
                    ) THEN
                        ALTER TABLE planning_task
                            ADD COLUMN parent_task_id bigint;
                    END IF;
                END IF;

                IF to_regclass('public.planning_taskassignment') IS NOT NULL THEN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_taskassignment'
                          AND column_name = 'assigned_to_id'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_taskassignment'
                          AND column_name = 'user_id'
                    ) THEN
                        ALTER TABLE planning_taskassignment
                            RENAME COLUMN assigned_to_id TO user_id;
                    END IF;
                END IF;

                IF to_regclass('public.planning_tasklink') IS NOT NULL THEN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_tasklink'
                          AND column_name = 'content_type_id'
                    ) THEN
                        ALTER TABLE planning_tasklink
                            ADD COLUMN content_type_id integer;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_tasklink'
                          AND column_name = 'object_id'
                    ) THEN
                        ALTER TABLE planning_tasklink
                            ADD COLUMN object_id integer;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_tasklink'
                          AND column_name = 'created_at'
                    ) THEN
                        ALTER TABLE planning_tasklink
                            ADD COLUMN created_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;
                END IF;

                IF to_regclass('public.planning_studysession') IS NOT NULL THEN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_studysession'
                          AND column_name = 'start_time'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_studysession'
                          AND column_name = 'start'
                    ) THEN
                        ALTER TABLE planning_studysession
                            RENAME COLUMN start_time TO start;
                    END IF;

                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_studysession'
                          AND column_name = 'end_time'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_studysession'
                          AND column_name = 'end'
                    ) THEN
                        ALTER TABLE planning_studysession
                            RENAME COLUMN end_time TO "end";
                    END IF;

                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_studysession'
                          AND column_name = 'note_summary'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_studysession'
                          AND column_name = 'notes'
                    ) THEN
                        ALTER TABLE planning_studysession
                            RENAME COLUMN note_summary TO notes;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_studysession'
                          AND column_name = 'notes'
                    ) THEN
                        ALTER TABLE planning_studysession
                            ADD COLUMN notes text NOT NULL DEFAULT '';
                    END IF;

                    UPDATE planning_studysession
                        SET notes = ''
                        WHERE notes IS NULL;
                    ALTER TABLE planning_studysession
                        ALTER COLUMN notes SET DEFAULT '',
                        ALTER COLUMN notes SET NOT NULL;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_studysession'
                          AND column_name = 'created_at'
                    ) THEN
                        ALTER TABLE planning_studysession
                            ADD COLUMN created_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_studysession'
                          AND column_name = 'updated_at'
                    ) THEN
                        ALTER TABLE planning_studysession
                            ADD COLUMN updated_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;
                END IF;

                IF to_regclass('public.planning_studysessionsparticipant') IS NOT NULL THEN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_studysessionsparticipant'
                          AND column_name = 'participant_id'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_studysessionsparticipant'
                          AND column_name = 'user_id'
                    ) THEN
                        ALTER TABLE planning_studysessionsparticipant
                            RENAME COLUMN participant_id TO user_id;
                    END IF;

                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_studysessionsparticipant'
                          AND column_name = 'invited_at'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_studysessionsparticipant'
                          AND column_name = 'created_at'
                    ) THEN
                        ALTER TABLE planning_studysessionsparticipant
                            RENAME COLUMN invited_at TO created_at;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_studysessionsparticipant'
                          AND column_name = 'created_at'
                    ) THEN
                        ALTER TABLE planning_studysessionsparticipant
                            ADD COLUMN created_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;
                END IF;

                IF to_regclass('public.planning_deadline') IS NOT NULL THEN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_deadline'
                          AND column_name = 'content_type_id'
                    ) THEN
                        ALTER TABLE planning_deadline
                            ADD COLUMN content_type_id integer;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_deadline'
                          AND column_name = 'object_id'
                    ) THEN
                        ALTER TABLE planning_deadline
                            ADD COLUMN object_id integer;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_deadline'
                          AND column_name = 'is_dismissed'
                    ) THEN
                        ALTER TABLE planning_deadline
                            ADD COLUMN is_dismissed boolean NOT NULL DEFAULT false;
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_deadline'
                          AND column_name = 'created_at'
                    ) THEN
                        ALTER TABLE planning_deadline
                            ADD COLUMN created_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;

                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'planning_deadline'
                          AND column_name = 'updated_at'
                    ) THEN
                        ALTER TABLE planning_deadline
                            ADD COLUMN updated_at timestamp with time zone NOT NULL DEFAULT now();
                    END IF;
                END IF;
            END $$;
            """
        )


class Migration(migrations.Migration):

    dependencies = [
        ("planning", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(repair_stale_planning_tables, migrations.RunPython.noop),
    ]
