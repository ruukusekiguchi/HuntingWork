<?php
$pdo = new PDO('mysql:host=localhost;dbname=dbname;charset=utf8','tablename','mypassword');

switch ($_SERVER['REQUEST_METHOD']) {
    case 'GET':
        $st = $pdo->query("SELECT * FROM sensorvalues");
        echo json_encode($st->fetchAll(PDO::FETCH_ASSOC));
        break;
    
    case 'POST':
        $in = json_decode(file_get_contents('php://input'), true);
        if (!isset($in['id']))
        {
                $st = $pdo->prepare("INSERT INTO sensorvalues(datetime,temp,hum,press) 　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　VALUES(:datetime,:temp,:hum,:press)");
        }
        $st->execute($in);
        
        echo json_encode("normal end");
        
        break;
}
?>