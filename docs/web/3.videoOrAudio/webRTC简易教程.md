# RTC简易demo














































常见问题
1.navigator.mediaDevices.getUserMedia 获取权限前，
navigator.mediaDevices.enumerateDevices 获取设备信息 label 为空字符串
2.mDNS可能导致外网不上传
chrome 隐藏 IP 打洞失败
ICE IP 为 4496c603-1ad2-45d3-abca-5826a7cd4f42.local
Anonymize local IPs exposed by WebRTC. (Chrome M75, Chrome M74 ?) 原因（规范）：
https://tools.ietf.org/html/draft-ietf-rtcweb-mdns-ice-candidates-03 使用多播DNS在暴露ICE候选对象时保护隐私
解决：
1.chrome://flags/ 内 Anonymize local IPs exposed by WebRTC. 设 为 Disabled
2.使 用 iceServers（** 已 测 试 没 啥 用 **， https://support.google.com/chrome/thread/9106174?hl=en）
3.内网无影响，外网不上传