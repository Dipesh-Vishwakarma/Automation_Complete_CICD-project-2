output "AppVM" {
description = "Public IP of Application VM"
value = aws_instance.AppVM.public_ip
}
output "MonitorVM" {
 description = "Public IP of Monitoring VM"
value = aws_instance.MonitorVM.public_ip
}
output "AppVM_Instance_ID" {
value = aws_instance.AppVM.id
}
output "MonitorVM_Instance_ID" {
value = aws_instance.MonitorVM.id
}
output "vpc_id" {
value = aws_vpc.main.id
}
