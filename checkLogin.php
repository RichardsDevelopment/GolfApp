<?php
	function addCrypt($salt, $pass){
		$ind = strlen($salt);
		
		$temp = substr($salt, 0, $ind) . $pass . substr($salt, $ind);
		
		return hash('sha256', $temp);
	}
	
	$pass = $_GET["pass"];
	$login = $_GET["login"];
	
	$result = "NotFinishedError";
	
	$servername = "localhost";
	$username = "root";
	$password = "";
	$dbname = "golfapp";
	
	$conn = new mysqli($servername, $username, $password, $dbname);

	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	} 
	
	$sql = "SELECT * FROM users WHERE email='" . $login . "'";
	$queryresult = $conn->query($sql);
	
	if($queryresult->num_rows > 0){
		$salt = "";
		$pwd = "";
		
		while($row = $queryresult->fetch_assoc()){
			$salt = $row["salt"];
			$pwd = $row["pass"];
		}
		$checkpass = addCrypt($salt, $pass);
		
		if($checkpass == $pwd){
			$return = "success";
		}
		else{
			$return = "NoLoginFound";
		}
	}
	else{
		$result = "NoLoginFound";
	}
	
	echo($result);
?>