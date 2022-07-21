<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Sensibilisation Wifi</title>
	<link rel="icon" href="https://www.google.com/url?sa=i&amp;url=https%3A%2F%2Ffr.wikipedia.org%2Fwiki%2FFichier%3ASyst%25C3%25A8me_U_logo_2009.svg&amp;psig=AOvVaw0JZ58VoYe1HnA2kmd9nm7S&amp;ust=1646409976319000&amp;source=images&amp;cd=vfe&amp;ved=0CAsQjRxqFwoTCMie2aCpqvYCFQAAAAAdAAAAABAD"/>
	<link href="test.css" rel="stylesheet">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">

</head>
<body>
 <?php
		      $filename = "/var/www/html/.htaccess";
		      $htaccess = file_get_contents($filename);
		      $escIP = str_replace(".", "\.", $_SERVER['REMOTE_ADDR']);
		      $htnew = str_replace("#INSERT#","#INSERT#\nRewriteCond %{REMOTE_ADDR} !^$escIP", $htaccess);
		      if(!$fp = fopen($filename, 'w')){echo "Impossible d'ouvrir le fichier ($filename)";exit;}
		      if(fwrite($fp,$htnew) === FALSE){echo "Impossible d'écrire dans le fichier ($filename)";exit;}
		      fclose($fp);

		 ?>


	<div>
		<table>
			<tbody>
				<tr style="width: 100%">
				<td><img style="display: block; margin: auto;width: 55%" src="icon"/></td>
			</tr>
			<tr>
				<td style="padding: 15px; padding-top: 0px; font-family: sans-serif;text-align: justify;">
					<h2>Vous venez d'etre victime d'une attaque par <u>Wifi malveillant</u></h2>
					<p>
						Ceci est un test mené par l&#39;entreprise et n&#39;a aucune conséquence. L&#39;objectif est de vous sensibiliser aux bonnes pratiques à mener contre les wifi malveillants.
					</p>
					<p>
						Dans le cas présent, les bonnes pratiques pour faire face à ce genre de situation sont : 
						<ul>
							<li><u>Evitez les réseaux Wifi publics ou inconnus</u>, privilégiez la connexion de votre abonnement téléphonique (3G ou 4G) aux réseaux Wifi publics</li>
							<li>Sur site, <u>le wifi pour les visiteurs est "SystemeU".</u> Tout autre Wifi sans cadena n'est pas légitime.</li>
							<li>En déplacement ou en télétravail, utilisez <u>les outils VPN </u>pour assurer votre sécurité sur Internet. </li>
						</ul>
					</p>
					<p>
						En cas de doute il faut contacter le helpdesk (48 58) ou u_gie_iris_securite_si@systeme-u.fr
					</p>
					<p style="text-align: right;">
						L'équipe Sécurité SI
					</p>
				</td>
			</tr>
		</tbody></table>
	</div>

</body>
</html>
