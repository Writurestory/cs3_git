<?php
	header('location:http://docs.redhat.com/docs/en-US/Red_Hat_Enterprise_Linux/4/html/Reference_Guide/index.html');
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

