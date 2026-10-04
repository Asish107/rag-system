DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_roles
        WHERE rolname = 'rag_reader'
    ) THEN
        CREATE ROLE rag_reader WITH LOGIN;
    END IF;
END
$$;

GRANT rds_iam TO rag_reader;

GRANT USAGE ON SCHEMA public TO rag_reader;

GRANT SELECT ON TABLE chunks TO rag_reader;