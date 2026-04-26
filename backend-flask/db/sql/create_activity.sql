INSERT INTO public.activities (
    user_uuid,
    message,
    expires_at
)
VALUES (
    (SELECT uuid
    FROM public.users 
    WHERE users.cognito_user_id = %(handle)s::text
    LIMIT 1
    ),
    %(message)s::text,
    %(expires_at)s::timestamp
) RETURNING uuid;
