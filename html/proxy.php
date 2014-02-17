<?php
if(array_key_exists('url', $_GET))
{
    $re=file_get_contents($_GET['url']);
    print_r($re);
}
?>