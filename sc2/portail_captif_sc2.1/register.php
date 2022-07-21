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
	<div id="header"></div>
	<div id="body">
		<div>&nbsp;</div>
		<div>
			<div id="reserved_block" style="">
			<form name="directSubscriptionForm" style="" action="registration.php" method="post">	
				<div class="title">
					<span id="directSubscriptionForm_title_text">Enregistrement</span>
				</div>
				<div class="explain">
					<span id="directSubscriptionForm_explain_text">Renseignez l'ensemble des champs obligatoires pour vous enregistrer.</span>
					<br>
				</div>
				<div class="h-separator"></div>
				<div id="direct_common_subscription_fields">
				<table id="common_subscription_fields" style="display: table;">
				<tbody>
					<tr id="subscriptionForm_last_name_block">
						<td>
							<span id="subscriptionForm_last_name_text" class="label">Nom</span>
							<span id="subscriptionForm_last_name_state" class="field-state">*</span>
						</td>
						<td>
							<input type="text" name="last_name" id="subscriptionForm_last_name">
						</td>
					</tr>
					<tr id="subscriptionForm_first_name_block">
						<td>
							<span id="subscriptionForm_first_name_text" class="label">Prénom</span>
							<span id="subscriptionForm_first_name_state" class="field-state">*</span>
						</td>
						<td>
							<input type="text" name="first_name" id="subscriptionForm_first_name">
						</td>
					</tr>
					<tr id="subscriptionForm_email_block">
						<td>
							<span id="subscriptionForm_email_text" class="label">Adresse email</span>
							<span id="subscriptionForm_email_state" class="field-state" style="visibility: visible;">*</span>
						</td>
						<td>
							<input type="email" name="login" id="subscriptionForm_email">
						</td>
					</tr>		
					<tr id="subscriptionForm_personal_field_1_block">
						<td>
							<span id="subscriptionForm_personal_field_1_text" class="label">Mot de passe</span>
							<span id="subscriptionForm_personal_field_1_state" class="field-state">*</span>
						</td>
						<td>
							<input type="password" name="password" id="subscriptionForm_personal_field_1">
						</td>
					</tr>
					<tr id="subscriptionForm_fields_state_block">
						<td colspan="2" class="field-state">
							<span id="subscriptionForm_fields_state_text" class="field-state">* Champs obligatoires</span>
						</td>
					</tr>
				</tbody>
				</table>
				</div>
				<table id="direct_specific_subscription_fields"><tbody>
				<tr>
					<td colspan="2">
						<button type="button" id="directSubscriptionForm_back_button" onclick="window.location.href='index.php'">Retour</button>
							&nbsp;
						<button type="submit" name="envoie" id="directSubscriptionForm_subscribe_button">S'enregistrer</button>
					</td>
				</tr>
				</tbody></table>
			</form>
			</div>
		</div>
		<div id="editor_img_GIE-Iris"></div>
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
