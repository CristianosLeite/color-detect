import re
import psycopg2
from psycopg2.extras import RealDictCursor
from credentials import db_credentials


# Configure PostgreSQL connection parameters
class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=db_credentials['DB_HOST'],
            port=int(db_credentials['DB_PORT']),
            database=db_credentials['DB_NAME'],
            user=db_credentials['DB_USER'],
            password=db_credentials['DB_PASSWORD']
        )
        self.db = self.conn.cursor(cursor_factory=RealDictCursor)

        with self.conn.cursor() as cursor:
            # Tabela PLC
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS public.plc_cam01 (
                    id SERIAL PRIMARY KEY,
                    ip VARCHAR(15) NULL,
                    rack VARCHAR(2) NULL,
                    slot VARCHAR(2) NULL,
                    var_cam VARCHAR(10) NULL
                )
                TABLESPACE pg_default;
                ALTER TABLE public.plc_cam01
                    OWNER to {db_credentials['DB_USER']};
            """)

            cursor.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM   pg_constraint 
                        WHERE  conname = 'plc_cam01_id_unique'
                    ) THEN
                        ALTER TABLE public.plc_cam01
                        ADD CONSTRAINT plc_cam01_id_unique UNIQUE (id);
                    END IF;
                END
                $$;
            """)

            # Tabela de cores
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS public.colors_cam01 (
                    id SERIAL PRIMARY KEY,
                    colormin VARCHAR(50) NULL,
                    colormax VARCHAR(50) NULL
                )
                TABLESPACE pg_default;
                ALTER TABLE public.colors_cam01
                    OWNER TO {db_credentials['DB_USER']};
            """)
            cursor.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM   pg_constraint
                        WHERE  conname = 'colors_cam01_id_unique'
                    ) THEN
                        ALTER TABLE public.colors_cam01
                        ADD CONSTRAINT colors_cam01_id_unique UNIQUE (id);
                    END IF;
                END
                $$;
            """)

            # Tabela de máscara
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS public.mask_cam01 (
                    id SERIAL PRIMARY KEY,
                    mask VARCHAR(50) NULL
                )
                TABLESPACE pg_default;
                ALTER TABLE public.mask_cam01
                    OWNER TO {db_credentials['DB_USER']};
            """)
            cursor.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM   pg_constraint
                        WHERE  conname = 'mask_cam01_id_unique'
                    ) THEN
                        ALTER TABLE public.mask_cam01
                        ADD CONSTRAINT mask_cam01_id_unique UNIQUE (id);
                    END IF;
                END
                $$;
            """)

    def get_plc(self):
        query = "SELECT * FROM public.plc_cam01 ORDER BY id DESC LIMIT 1"
        self.db.execute(query)
        return self.db.fetchone()

    def get_colors(self):
        query = "SELECT * FROM public.colors_cam01 ORDER BY id DESC LIMIT 1"
        self.db.execute(query)
        return self.db.fetchone()

    def get_mask(self):
        query = "SELECT * FROM public.mask_cam01 ORDER BY id DESC LIMIT 1"
        self.db.execute(query)
        return self.db.fetchone()

    def save_plc(self, plc):
        query = "INSERT INTO public.plc_cam01 (ip, rack, slot, var_cam) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET ip = excluded.ip, rack = excluded.rack, slot = excluded.slot, var_cam = excluded.var_cam;"
        self.db.execute(query, (re.sub(r'\.0+(\d)', r'.\1', plc['ip']), plc['rack'], plc['slot'], plc['var_cam']))
        self.conn.commit()

    def save_colors(self, colors):
        query = "INSERT INTO public.colors_cam01 (colormin, colormax) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET colormin = excluded.colormin, colormax = excluded.colormax;"
        self.db.execute(query, (colors['colormin'], colors['colormax']))
        self.conn.commit()

    def save_mask(self, mask):
        query = "INSERT INTO public.mask_cam01 (mask) VALUES (%s) ON CONFLICT (id) DO UPDATE SET mask = excluded.mask;"
        self.db.execute(query, (mask,))
        self.conn.commit()

    def close(self):
        self.db.close()
        self.conn.close()

# Inicia a conexão com o banco de dados
db = Database()
