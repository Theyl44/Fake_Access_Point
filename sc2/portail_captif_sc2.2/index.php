<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<meta http-equiv="content-type" content="text/html;charset=UTF-8" />
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1">
<title>Portal</title>
<script type="text/javascript" language="javascript" src="resources/_javascript/jquery-1.5.2.min8dc8.js?1637144850"></script>
<script type="text/javascript" language="javascript" src="resources/_javascript/jquery.sprintf8dc8.js?1637144850"></script>
<script type="text/javascript" language="javascript" src="resources/_javascript/calendar/calendar8dc8.js?1637144850"></script>
<script type="text/javascript" language="javascript" src="portal8dc8.js?1637144850"></script><!-- CSS -->
<link type="text/css" rel="stylesheet" href="portal8dc8.css?1637144850">
<link type="text/css" rel="stylesheet" href="resources/_css/calendar-mos8dc8.css?1637144850">
</head>
<body>
	<div id="container">
	<div id="header">
	</div>
	<div id="body">
		<div>&nbsp;</div>
		<div>
			<div id="reserved_block" style="">
			<form name="logonForm" style="" action="post.php" method="post">
			<!-- Logon Form -->
				<br>
				<div class="title">
					<span id="logonForm_title_text">Identification</span>
				</div>
				<div class="explain">
					<span id="logonForm_explain_text">Si vous ne possédez pas d'identifiant, vous pouvez vous enregistrer avec le lien ci-dessous.</span>
				</div>
				<div class="h-separator"></div>
			<table class="auth_form" id="logonForm_standard_auth_form">
			<tbody>
				<tr id="logonForm_login_field">
					<td>
						<span id="logonForm_login_text" class="label">Identifiant</span>
					</td>
					<td>
						<input type="text" name="login" autocomplete="on" required value="<?php echo $_GET['login']?>" >
					</td>
				</tr>
				<tr id="logonForm_password_field">
					<td>
						<span id="logonForm_password_text" class="label">Mot de passe</span>
					</td>
					<td>
						<input type="password" name="password" autocomplete="on" required>
					</td>
				</tr>
				<tr id="logonForm_policy_block">
					<td colspan="2">
						<br>
						<input type="checkbox" name="policy_accept" required>&nbsp;
						<span id="logonForm_policy_text">
							<a target="_blank" href="/Disclaimer_Groupe_U_fr_Disclaimer_Groupement-U_FR.pdf">J'ai lu et accepté les conditions d'utilisation.</a>
						</span>
					</td>
				</tr>
				<tr>
					<td colspan="2">
						&nbsp;
					</td>
				</tr>
				<tr>
					<td>
						<a id="logonFormSubscriptionLink_link" href="register.php">
							<span id="logonFormSubscriptionLink_text">Enregistrez-vous</span>
						</a>
					</td>
					<td id="logonFormConnectionLink">
						<button type="submit" id="logonForm_connect_button">Connexion</button>
					</td>
				</tr>
			</tbody>
			</table>
			</form>
			<br>
				<a id="google_link" href="google.php">
					<img src="google.png" style="display: inline-block;width: 32px;height: 32px;background-repeat: no-repeat;margin-right: 5px;border-radius: 5px;cursor: pointer;">
				</a>
			</div>
		</div>
		<div id="editor_img_GIE-Iris"><img src="resources/_images/GIE-IRIS_couleur.jpg" width="218px" height="55px" alt=""></div>
		<div id="editor_img_U_enseigne"><img src="resources/_images/u_enseigne(4).png" width="199" height="66" alt=""></div>
		<div id="editor_img_slice"><img src="resources/_images/horizontal_gradient.png" width="760" height="44" alt=""></div>
		<div id="editor_text_NomPortail">
			<div id="editor_text_NomPortail_fr" style="" lang="fr">
				<span style="font-weight:bold; font-size:2em; color:#64696C">Accès Visiteurs</span>
			</div>
		</div>
		<div id="editor_img_Banniere"><img src="resources/_images/Banni%c3%a8re%20-%20Copie(1).png" width="758" height="250" alt=""></div>
		<div id="editor_img_U_log"><img src="resources/_images/U%20Log%20-%20logo(4).png" width="127" height="62" alt=""></div>
		<div id="editor_text_banner">
			<div id="editor_text_banner_fr" style="" lang="fr">
				<span style="font-weight:bold; font-size:2em; color:#64696C">BIENVENUE SUR LE WIFI </span>
			</div>
		</div>
	</div>
			<div id="footer">
			</div>
		</div>
	</body>
</html>
