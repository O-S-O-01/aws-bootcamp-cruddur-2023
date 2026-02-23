--this was manually cr
INSERT INTO public.users (display_name, handle, cognito_user_id) 
VALUES
    ('paul ohajekwe', 'paulooh', 'MOCK'),
    ('Andrew Bayko', 'Bayko', 'MOCK'),
    ('John Doe', 'johndoe', 'MOCK'),
    ('Jane Smith', 'janesmith', 'MOCK'),
    ('Alice Johnson', 'alicejohnson', 'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at) 
VALUES
    (
        (SELECT uuid FROM public.users WHERE users.handle = 'paulooh' LIMIT 1), 
        'this was imported as seed data',
        current_timestamp + interval '10 days'
    );