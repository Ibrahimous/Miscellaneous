<?php
    //REFERENCE: https://zestedesavoir.com/tutoriels/945/les-injections-sql-le-tutoriel/les-injections-sql-en-aveugle/total-blind-sql-injection/
    $host = "localhost";
    $user_mysql = "root";
    $password_mysql = "";
    $database = "injectable";

    $db = mysqli_connect($host, $user_mysql, $password_mysql, $database);
    mysqli_set_charset($db, "utf8");

?>

<!DOCTYPE html>
<html lang="fr">
    <head>
        <title></title>
        <meta charset="UTF-8" />
    </head>
    <body>
        <?php
            if(!empty($_GET['id']))
            {
                $id = mysqli_real_escape_string($db, $_GET['id']);
                $query = "SELECT id, username FROM users WHERE id = ".$id;
                $rs_article = mysqli_query($db, $query);
            }
        ?>
    </body>
</html>
