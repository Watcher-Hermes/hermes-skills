# 3. SQL string interpolation
$dbh->do("DELETE FROM users WHERE id = $id");  # SQLi