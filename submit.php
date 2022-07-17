<?php

$FileName=$_FILES['filename']['name'];
$TmpName=$_FILES['filename']['tmp_name'];

$target_dir="Resume Folder/";
$target_file = $target_dir . basename($_FILES["filename"]["name"]);

move_uploaded_file($_FILES["filename"]["tmp_name"], $target_file);
echo '<script>alert("File Uploaded Successful"); window.location="Resultpage.html"</script>';
exit();
?>
