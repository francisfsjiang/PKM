<?php
$url='http://127.0.0.1:8004/api/search';
if(array_key_exists('title', $_GET))
    $re=file_get_contents($url."?title=".$_GET['title']);
else
    $re=file_get_contents($url);
print_r($re);
?>
