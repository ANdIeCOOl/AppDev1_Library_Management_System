from werkzeug.security import generate_password_hash, check_password_hash
pass_hash = generate_password_hash("Andrew123")
pass_hash