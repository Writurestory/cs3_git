<?php
	header('location:http://i.linuxtoy.org/docs/guide/');
?>
<html>
<head><h1 align="center"><em>welcome</em></h1></head>
<body>
<form action="index.php" method="post">
<div align="center">
login:<input type="email" name="email" /><br />
password:<input type="passwrod" name="password" /><br />
	<input type="submit" value="submit" /><br />
search:<input type="search" name="search" /><br />
<?php
	echo `date`;
?>
</div>
<>
<span>Visits </span>
</form>
</body>
</html>

