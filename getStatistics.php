<?php

	function createDict($first, $second){
		$total = array();
		$orderedString = "";
		
		foreach ($second as $key => $value){
			if(array_key_exists($key, $first)){
				$total[$key] = ($value + $first[$key]);
			}
		}
		
		$flippedTotal = array_flip($total);
		ksort($flippedTotal);
		$returned = array_flip($flippedTotal);
		
		foreach(array_keys($returned) as $key){
			$orderedString = $orderedString . "" . $key . "," . $returned[$key]. "," . $first[$key] . "," . $second[$key] . "|";
		}
			
		return $orderedString;
	}

	$stat1 = $_GET['stat1'];
	$stat2 = $_GET['stat2'];
	$servername = "localhost";
	$username = "root";
	$password = "";
	$dbname = "golfapp";
	$firstRes = array();
	$secondRes = array();
	$return = array();
	
	$conn = new mysqli($servername, $username, $password, $dbname);

	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	} 
	
	$sql = "SELECT name, rank FROM " . $stat1;
	$result = $conn->query($sql);
	
	if($result->num_rows > 0){
		while($row = $result->fetch_assoc()){
			$return1[$row['name']] = $row['rank'];
		}
		
		$sql = "SELECT name, rank FROM " . $stat2;
		$result = $conn->query($sql);
		
		if($result->num_rows > 0){
			$i = 0;
			while($row = $result->fetch_assoc()){
				$return2[$row['name']] = $row['rank'];
			}
		
			$returnString = createDict($return1, $return2);
		}
		else{
			echo(0);
		}
	}
	else{
		echo(0);
	}

	echo $returnString;
	
?>