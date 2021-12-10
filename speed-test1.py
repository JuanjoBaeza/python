import speedtest

wifi  = speedtest.Speedtest()
wifi.get_best_server()

print(f"Your ping is: {wifi.results.ping} ms")
print(f"Wifi Download Speed is: {round(wifi.download()/ 1000 / 1000, 1)} Mbit/s")
print(f"Wifi Download Speed is: {round(wifi.upload()/ 1000 / 1000, 1)} Mbit/s")