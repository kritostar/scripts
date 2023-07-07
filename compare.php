<?php

// CSV file path
$csvFilePath = 'C:\\Users\\krito\\Desktop\\scripts\\tables.csv';

// MySQL database configuration
$mysqlHost = 'prod-mirror-database-bi.cd5wkjghztcq.us-east-1.rds.amazonaws.com';
$mysqlUsername = 'cifacchini';
$mysqlPassword = 'w1^2AMCrqF\~i&,/R/^;';
$mysqlDatabase = 'sfs_bi_analytics';

// MSSQL database configuration
$mssqlServer = 'prod-mirror-database-mssql.cd5wkjghztcq.us-east-1.rds.amazonaws.com';
$mssqlUsername = 'cifacchini';
$mssqlPassword = 'w1^2AMCrqF\~i&,/R/^;';
$mssqlDatabase = 'SFSDB';

// Load table and field mappings from CSV
$tableFieldMappings = [];
if (($handle = fopen($csvFilePath, 'r')) !== false) {
    while (($data = fgetcsv($handle)) !== false) {
        $tableFieldMappings[$data[0]] = explode(',', $data[1]);
    }
    fclose($handle);
} else {
    die('Failed to open CSV file.');
}

try {
    // Connect to MySQL database
    $mysqlConn = new PDO("mysql:host=$mysqlHost;dbname=$mysqlDatabase", $mysqlUsername, $mysqlPassword);
    $mysqlConn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Connect to MSSQL database
    $mssqlConn = new PDO("sqlsrv:Server=$mssqlServer;Database=$mssqlDatabase", $mssqlUsername, $mssqlPassword);
    $mssqlConn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Compare tables
    foreach ($tableFieldMappings as $tableName => $fields) {
        // Fetch data from MySQL table
        $mysqlQuery = "SELECT " . implode(', ', $fields) . " FROM $tableName";
        $mysqlStmt = $mysqlConn->query($mysqlQuery);
        $mysqlRows = $mysqlStmt->fetchAll(PDO::FETCH_ASSOC);

        // Fetch data from MSSQL table
        $mssqlQuery = "SELECT " . implode(', ', $fields) . " FROM $tableName";
        $mssqlStmt = $mssqlConn->query($mssqlQuery);
        $mssqlRows = $mssqlStmt->fetchAll(PDO::FETCH_ASSOC);

        // Compare the data from both tables
        if ($mysqlRows == $mssqlRows) {
            echo "The data in table $tableName is identical in both databases.\n";
        } else {
            echo "The data in table $tableName is not identical in both databases.\n";
        }
    }

    // Close the database connections
    $mysqlConn = null;
    $mssqlConn = null;
} catch (PDOException $e) {
    die('Error: ' . $e->getMessage());
}
