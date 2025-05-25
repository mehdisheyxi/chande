import fake_useragent

ua = fake_useragent.UserAgent()
headers = {"User-Agent": ua.random}  # هر بار یک مقدار متفاوت!
print(headers)