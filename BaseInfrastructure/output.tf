output "Slave" {
description = "Public IP of Application VM"
value = aws_instance.Slave.public_ip
}
output "Slave_Instance_ID" {
value = aws_instance.Slave.id
}
output "Jenkins" {
description = "Public IP of Application VM"
value = aws_instance.Jenkins.public_ip
}
output "Jenkins_Instance_ID" {
value = aws_instance.Jenkins.id
}
output "vpc_id" {
value = aws_vpc.main.id
}
