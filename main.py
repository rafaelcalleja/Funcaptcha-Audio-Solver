from funcaptcha_solver import funcaptcha, WhisperWebService

#Replace public_key and site with your key/site
funcap = funcaptcha(

	public_key="0A1D34FC-659D-4E23-B17B-694DCFCF6A6C",
	site="https://tcr9i.chat.openai.com",
	transcriber=WhisperWebService(endpoint="http://localhost:9000/asr"),
	proxies={
		'http': 'http://10.10.16.2:5566',
		'https': 'http://10.10.16.2:5566',
	}
	
)

bad_captchas = 0

def solve_captcha():
	global bad_captchas
	while True:
		answer = funcap.solve()
		captcha_token = answer["token"]
		error = answer["error"]
		if error == None:
			answer["bad_captchas"] = bad_captchas
			return answer
		if "not_supported" in error:
			return "Site not supported / does not have audio challenges"
		if "too high" in error:
			print(answer)
			return "Ratelimited"
		else:
			bad_captchas += 1

captcha_token = solve_captcha()
print(captcha_token)
