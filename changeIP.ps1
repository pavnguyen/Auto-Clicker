
########################################
# Nhập số máy để chạy chương trình
########################################
if ($args.length -gt 0)
{
    Write-Host "May $($args[0])" -ForegroundColor YELLOW -BackgroundColor RED
}else{
    Write-Host "Vui long nhap so may vo !!!"  -ForegroundColor Red
}


for ($i=0 ; $i -lt $args.length ; $i++)
{

    $numberMachine = $args[0]
    $ip=Get-Content 'Z:\Project Python\Auto Clicker\ressources\config_ip.txt' | Select -index ($args[0] - 1)  ### IMPORTANT ###
 
    ####################################
    # Cấu hình thông số chạy FakeIP
    #################################### 
    $exeFakeIP = "C:\Program Files\OpenVPN\bin\openvpn.exe"             ### IMPORTANT ###
    $params ="--status C:\status.log --log C:\logChangeIP.txt --tls-client --client --dev tun --remote $ip --proto udp --port 1197 --lport 53 --persist-key --persist-tun --ca data\ca.crt --comp-lzo --mute 3 --tun-mtu 1400 --mssfix 1360 --auth-user-pass data\auth.txt --reneg-sec 0 --keepalive 10 120 --route-method exe --route-delay 2 --verb 3 --auth-nocache --crl-verify data\crl.pem --remote-cert-tls server --block-outside-dns --cipher aes-256-cbc --auth sha256"
	Write-Host $exeFakeIP $params
    start-process  $exeFakeIP $params -NoNewWindow 
 
}

